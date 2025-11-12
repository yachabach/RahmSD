"""
Thermal Image Data Collection App - Cron Version
Captures a single sample from thermal cameras - designed to run via cron
"""

import json
import time
import base64
import sys
import argparse
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import logging


class ThermalDataCollector:
    """Collects thermal images and metadata from web-based thermal cameras"""
    
    def __init__(self, output_dir: str = "thermal_data", log_file: Optional[str] = None):
        self.output_dir = Path(output_dir)
        self.setup_directories()
        self.setup_logging(log_file)
        self.driver = None
        
    def setup_directories(self):
        """Create directory structure for organized data storage"""
        self.images_dir = self.output_dir / "images"
        self.metadata_dir = self.output_dir / "metadata"
        self.labeled_dir = self.output_dir / "labeled"
        self.logs_dir = self.output_dir / "logs"
        
        for directory in [self.images_dir, self.metadata_dir, self.labeled_dir, self.logs_dir]:
            directory.mkdir(parents=True, exist_ok=True)
        
        # Create subdirectories for labeled data
        (self.labeled_dir / "person").mkdir(exist_ok=True)
        (self.labeled_dir / "no_person").mkdir(exist_ok=True)
        (self.labeled_dir / "uncertain").mkdir(exist_ok=True)
    
    def setup_logging(self, log_file: Optional[str] = None):
        """Setup logging to file and console"""
        if log_file is None:
            log_file = self.logs_dir / f"collector_{datetime.now().strftime('%Y%m')}.log"
        
        # Create logger
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)
        
        # Remove existing handlers
        self.logger.handlers = []
        
        # File handler
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(logging.INFO)
        
        # Console handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.INFO)
        
        # Formatter
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)
        
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)
        
        self.logger.info(f"Logging initialized - {log_file}")
    
    def init_driver(self, headless: bool = True):
        """Initialize Selenium WebDriver with error handling"""
        try:
            options = webdriver.ChromeOptions()
            if headless:
                options.add_argument('--headless')
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            options.add_argument('--disable-blink-features=AutomationControlled')
            options.add_argument('--disable-gpu')
            options.add_argument('--window-size=1920,1080')
            
            # Add user agent to avoid detection
            options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')
            
            self.driver = webdriver.Chrome(options=options)
            self.driver.set_page_load_timeout(30)
            self.logger.info("WebDriver initialized successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to initialize WebDriver: {e}")
            return False
    
    def login_if_needed(self, url: str, login_config: Optional[Dict] = None):
        """Handle login if the site requires authentication"""
        if not login_config:
            return True
        
        try:
            self.driver.get(url)
            time.sleep(2)
            
            # Check if login page
            if login_config.get('username_field'):
                username_field = self.driver.find_element(
                    By.CSS_SELECTOR, login_config['username_field']
                )
                password_field = self.driver.find_element(
                    By.CSS_SELECTOR, login_config['password_field']
                )
                
                username_field.send_keys(login_config['username'])
                password_field.send_keys(login_config['password'])
                
                submit_button = self.driver.find_element(
                    By.CSS_SELECTOR, login_config['submit_button']
                )
                submit_button.click()
                
                time.sleep(3)
                self.logger.info(f"Logged in to {url}")
                return True
                
        except Exception as e:
            self.logger.warning(f"Login attempt failed or not needed: {e}")
            return False
    
    def capture_frame_from_video(self, video_selector: str = '.video-control') -> Optional[str]:
        """Capture current frame from video element as base64"""
        script = """
        const video = document.querySelector(arguments[0]);
        if (!video) return null;
        
        const canvas = document.createElement('canvas');
        canvas.width = video.videoWidth || 640;
        canvas.height = video.videoHeight || 480;
        
        const ctx = canvas.getContext('2d');
        ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
        
        return canvas.toDataURL('image/png').split(',')[1];
        """
        
        try:
            img_base64 = self.driver.execute_script(script, video_selector)
            return img_base64
        except Exception as e:
            self.logger.error(f"Failed to capture frame: {e}")
            return None
    
    def extract_field_values(self, field_selectors: Dict[str, str]) -> Dict[str, str]:
        """Extract values from HTML fields"""
        values = {}
        
        for field_name, selector in field_selectors.items():
            try:
                element = self.driver.find_element(By.CSS_SELECTOR, selector)
                # Try to get value, text, or innerHTML
                value = (element.get_attribute('value') or 
                        element.text or 
                        element.get_attribute('innerHTML'))
                values[field_name] = value.strip()
            except NoSuchElementException:
                self.logger.warning(f"Field '{field_name}' not found with selector '{selector}'")
                values[field_name] = None
            except Exception as e:
                self.logger.warning(f"Error extracting field '{field_name}': {e}")
                values[field_name] = None
        
        return values
    
    def capture_single_sample(self, 
                            url: str, 
                            camera_id: str,
                            video_selector: str = '.video-control',
                            field_selectors: Dict[str, str] = None,
                            wait_time: int = 5) -> Optional[Dict]:
        """Capture a single data sample from a URL"""
        
        try:
            # Navigate to URL
            self.logger.info(f"Navigating to {url}")
            self.driver.get(url)
            
            # Wait for video to load
            WebDriverWait(self.driver, 15).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, video_selector))
            )
            
            # Extra wait for video to stabilize
            self.logger.info(f"Waiting {wait_time}s for video to stabilize...")
            time.sleep(wait_time)
            
            # Capture timestamp
            timestamp = datetime.now()
            timestamp_str = timestamp.strftime("%Y%m%d_%H%M%S_%f")
            
            # Capture image
            self.logger.info("Capturing frame...")
            img_base64 = self.capture_frame_from_video(video_selector)
            if not img_base64:
                self.logger.error(f"Failed to capture image from {url}")
                return None
            
            # Save image
            img_filename = f"{camera_id}_{timestamp_str}.png"
            img_path = self.images_dir / img_filename
            
            with open(img_path, 'wb') as f:
                f.write(base64.b64decode(img_base64))
            
            self.logger.info(f"Image saved: {img_filename}")
            
            # Extract field values
            field_values = {}
            if field_selectors:
                self.logger.info("Extracting field values...")
                field_values = self.extract_field_values(field_selectors)
            
            # Create metadata
            metadata = {
                'timestamp': timestamp.isoformat(),
                'camera_id': camera_id,
                'url': url,
                'image_filename': img_filename,
                'image_path': str(img_path),
                'fields': field_values,
                'label': None,
                'labeled_at': None
            }
            
            # Save metadata
            metadata_filename = f"{camera_id}_{timestamp_str}.json"
            metadata_path = self.metadata_dir / metadata_filename
            
            with open(metadata_path, 'w') as f:
                json.dump(metadata, f, indent=2)
            
            self.logger.info(f"✓ Successfully captured sample: {img_filename}")
            return metadata
            
        except TimeoutException:
            self.logger.error(f"Timeout waiting for video element at {url}")
            return None
        except Exception as e:
            self.logger.error(f"Error capturing from {url}: {e}", exc_info=True)
            return None
    
    def run_single_collection(self, 
                             camera_configs: List[Dict],
                             login_config: Optional[Dict] = None):
        """
        Run a single collection cycle from all cameras
        Designed to be called by cron
        """
        
        self.logger.info("="*60)
        self.logger.info("Starting collection cycle")
        self.logger.info("="*60)
        
        if not self.init_driver(headless=True):
            self.logger.error("Failed to initialize driver. Exiting.")
            return False
        
        successful_captures = 0
        failed_captures = 0
        
        try:
            # Login if needed (once for all cameras if same domain)
            if login_config:
                self.login_if_needed(camera_configs[0]['url'], login_config)
            
            # Capture from each camera
            for i, config in enumerate(camera_configs, 1):
                self.logger.info(f"\nProcessing camera {i}/{len(camera_configs)}: {config['camera_id']}")
                
                sample = self.capture_single_sample(
                    url=config['url'],
                    camera_id=config['camera_id'],
                    video_selector=config.get('video_selector', '.video-control'),
                    field_selectors=config.get('field_selectors', {}),
                    wait_time=config.get('wait_time', 5)
                )
                
                if sample:
                    successful_captures += 1
                else:
                    failed_captures += 1
                
                # Small delay between cameras
                if i < len(camera_configs):
                    time.sleep(2)
        
        except Exception as e:
            self.logger.error(f"Collection cycle failed: {e}", exc_info=True)
            return False
        
        finally:
            self.close()
        
        self.logger.info("="*60)
        self.logger.info(f"Collection cycle complete: {successful_captures} successful, {failed_captures} failed")
        self.logger.info("="*60)
        
        return successful_captures > 0
    
    def label_data(self, batch_size: int = 50):
        """Interactive labeling tool for collected images"""
        metadata_files = sorted(self.metadata_dir.glob("*.json"))
        unlabeled = [f for f in metadata_files 
                    if json.load(open(f)).get('label') is None]
        
        if not unlabeled:
            self.logger.info("No unlabeled data found!")
            return
        
        self.logger.info(f"Found {len(unlabeled)} unlabeled samples")
        
        for i, metadata_file in enumerate(unlabeled[:batch_size]):
            with open(metadata_file, 'r') as f:
                metadata = json.load(f)
            
            print(f"\n{'='*60}")
            print(f"Sample {i+1}/{min(batch_size, len(unlabeled))}")
            print(f"Camera: {metadata['camera_id']}")
            print(f"Time: {metadata['timestamp']}")
            print(f"Fields: {json.dumps(metadata['fields'], indent=2)}")
            print(f"Image: {metadata['image_filename']}")
            print(f"{'='*60}")
            
            # Get label
            while True:
                label = input("Label (p=person, n=no_person, u=uncertain, s=skip, q=quit): ").lower()
                if label in ['p', 'n', 'u', 's', 'q']:
                    break
                print("Invalid input. Please use p, n, u, s, or q")
            
            if label == 'q':
                break
            
            if label == 's':
                continue
            
            # Map label
            label_map = {'p': 'person', 'n': 'no_person', 'u': 'uncertain'}
            label_str = label_map[label]
            
            # Update metadata
            metadata['label'] = label_str
            metadata['labeled_at'] = datetime.now().isoformat()
            
            with open(metadata_file, 'w') as f:
                json.dump(metadata, f, indent=2)
            
            # Copy to labeled directory
            src_img = Path(metadata['image_path'])
            dst_img = self.labeled_dir / label_str / src_img.name
            
            import shutil
            shutil.copy(src_img, dst_img)
            
            self.logger.info(f"Labeled as '{label_str}': {src_img.name}")
        
        self.generate_training_dataset()
    
    def generate_training_dataset(self):
        """Generate CSV dataset for AI training"""
        metadata_files = self.metadata_dir.glob("*.json")
        labeled_samples = []
        
        for metadata_file in metadata_files:
            with open(metadata_file, 'r') as f:
                metadata = json.load(f)
            
            if metadata.get('label'):
                # Flatten for CSV
                row = {
                    'timestamp': metadata['timestamp'],
                    'camera_id': metadata['camera_id'],
                    'image_path': str(self.labeled_dir / metadata['label'] / Path(metadata['image_path']).name),
                    'label': metadata['label'],
                    'labeled_at': metadata['labeled_at']
                }
                
                # Add field values
                for field_name, field_value in metadata.get('fields', {}).items():
                    row[f'field_{field_name}'] = field_value
                
                labeled_samples.append(row)
        
        if labeled_samples:
            df = pd.DataFrame(labeled_samples)
            dataset_path = self.output_dir / "training_dataset.csv"
            df.to_csv(dataset_path, index=False)
            self.logger.info(f"Training dataset generated: {dataset_path}")
            self.logger.info(f"Total labeled samples: {len(labeled_samples)}")
            self.logger.info(f"Label distribution:\n{df['label'].value_counts()}")
        else:
            self.logger.warning("No labeled samples found")
    
    def get_collection_stats(self):
        """Get statistics about collected data"""
        total_images = len(list(self.images_dir.glob("*.png")))
        total_metadata = len(list(self.metadata_dir.glob("*.json")))
        
        # Count labeled
        labeled_counts = {}
        for label_dir in ['person', 'no_person', 'uncertain']:
            count = len(list((self.labeled_dir / label_dir).glob("*.png")))
            labeled_counts[label_dir] = count
        
        total_labeled = sum(labeled_counts.values())
        
        stats = {
            'total_samples': total_images,
            'total_metadata': total_metadata,
            'total_labeled': total_labeled,
            'unlabeled': total_images - total_labeled,
            'label_breakdown': labeled_counts
        }
        
        return stats
    
    def close(self):
        """Clean up resources"""
        if self.driver:
            try:
                self.driver.quit()
                self.logger.info("WebDriver closed")
            except Exception as e:
                self.logger.error(f"Error closing WebDriver: {e}")


def load_config(config_file: str) -> Dict:
    """Load configuration from JSON file"""
    with open(config_file, 'r') as f:
        return json.load(f)


def main():
    """Main entry point for cron job"""
    parser = argparse.ArgumentParser(description='Thermal Data Collector - Cron Version')
    parser.add_argument('--config', type=str, required=True, help='Path to config JSON file')
    parser.add_argument('--output-dir', type=str, default='thermal_data', help='Output directory')
    parser.add_argument('--label', action='store_true', help='Run labeling mode')
    parser.add_argument('--stats', action='store_true', help='Show collection statistics')
    
    args = parser.parse_args()
    
    # Load configuration
    config = load_config(args.config)
    
    # Create collector
    collector = ThermalDataCollector(output_dir=args.output_dir)
    
    try:
        if args.stats:
            # Show statistics
            stats = collector.get_collection_stats()
            print("\n" + "="*60)
            print("COLLECTION STATISTICS")
            print("="*60)
            print(f"Total samples collected: {stats['total_samples']}")
            print(f"Total labeled: {stats['total_labeled']}")
            print(f"Unlabeled: {stats['unlabeled']}")
            print("\nLabel breakdown:")
            for label, count in stats['label_breakdown'].items():
                print(f"  {label}: {count}")
            print("="*60)
            
        elif args.label:
            # Run labeling
            collector.label_data(batch_size=100)
            
        else:
            # Run collection
            success = collector.run_single_collection(
                camera_configs=config['cameras'],
                login_config=config.get('login')
            )
            sys.exit(0 if success else 1)
            
    except Exception as e:
        collector.logger.error(f"Fatal error: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
