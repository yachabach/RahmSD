"""
Thermal Image Data Collection App - Hybrid Functional/OOP Approach
Uses functions for pure operations, classes for stateful objects
"""

import json
import time
import base64
import sys
import argparse
import re
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import logging


# ============================================================================
# DATA STRUCTURES
# ============================================================================

@dataclass
class CameraConfig:
    """Configuration for a single camera"""
    camera_id: str
    url: str
    video_selector: str = '.video-control'
    field_selectors: Dict[str, str] = None
    wait_time: int = 5
    
    def __post_init__(self):
        if self.field_selectors is None:
            self.field_selectors = {}


@dataclass
class Sample:
    """Captured sample data"""
    timestamp: datetime
    camera_id: str
    url: str
    image_filename: str
    image_path: Path
    fields: Dict
    label: Optional[str] = None
    labeled_at: Optional[datetime] = None
    
    def to_dict(self) -> Dict:
        """Convert to dictionary for JSON serialization"""
        return {
            'timestamp': self.timestamp.isoformat(),
            'camera_id': self.camera_id,
            'url': self.url,
            'image_filename': self.image_filename,
            'image_path': str(self.image_path),
            'fields': self.fields,
            'label': self.label,
            'labeled_at': self.labeled_at.isoformat() if self.labeled_at else None
        }


# ============================================================================
# LOGGING (FUNCTIONAL)
# ============================================================================

def setup_logging(log_dir: Path, log_file: Optional[str] = None) -> logging.Logger:
    """Setup logging to file and console"""
    if log_file is None:
        log_file = log_dir / f"collector_{datetime.now().strftime('%Y%m')}.log"
    
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    logger.handlers = []
    
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    
    file_handler = logging.FileHandler(log_file)
    file_handler.setFormatter(formatter)
    
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger


# ============================================================================
# DIRECTORY MANAGEMENT (FUNCTIONAL)
# ============================================================================

def create_directory_structure(output_dir: Path) -> Dict[str, Path]:
    """Create and return all necessary directories"""
    directories = {
        'root': output_dir,
        'images': output_dir / "images",
        'metadata': output_dir / "metadata",
        'labeled': output_dir / "labeled",
        'logs': output_dir / "logs",
        'person': output_dir / "labeled" / "person",
        'no_person': output_dir / "labeled" / "no_person",
        'uncertain': output_dir / "labeled" / "uncertain"
    }
    
    for path in directories.values():
        path.mkdir(parents=True, exist_ok=True)
    
    return directories


# ============================================================================
# IMAGE OPERATIONS (FUNCTIONAL)
# ============================================================================

def capture_video_frame(driver, video_selector: str) -> Optional[str]:
    """
    Capture current frame from video element
    
    Args:
        driver: Selenium WebDriver instance
        video_selector: CSS selector for video element
        
    Returns:
        Base64 encoded image string or None if failed
    """
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
        return driver.execute_script(script, video_selector)
    except Exception as e:
        logging.error(f"Failed to capture frame: {e}")
        return None


def save_base64_image(img_base64: str, output_path: Path) -> bool:
    """Save base64 encoded image to file"""
    try:
        with open(output_path, 'wb') as f:
            f.write(base64.b64decode(img_base64))
        return True
    except Exception as e:
        logging.error(f"Failed to save image: {e}")
        return False


# ============================================================================
# FIELD EXTRACTION (FUNCTIONAL)
# ============================================================================

def parse_numbers_from_text(text: str) -> List[str]:
    """Extract all numbers from text string"""
    return re.findall(r'\d+\.?\d*', text)


def extract_field_value(driver, selector: str) -> Tuple[Optional[str], List[str]]:
    """
    Extract value from a single HTML field
    
    Returns:
        Tuple of (raw_text, parsed_numbers)
    """
    try:
        element = driver.find_element(By.CSS_SELECTOR, selector)
        text = element.text.strip()
        numbers = parse_numbers_from_text(text)
        return text, numbers
    except NoSuchElementException:
        return None, []
    except Exception as e:
        logging.warning(f"Error extracting field: {e}")
        return None, []


def extract_all_fields(driver, field_selectors: Dict[str, str]) -> Dict:
    """
    Extract all field values with auto-parsing
    
    Args:
        driver: Selenium WebDriver
        field_selectors: Dict mapping field names to CSS selectors
        
    Returns:
        Dict with raw values and parsed numbers
    """
    fields = {}
    
    for field_name, selector in field_selectors.items():
        text, numbers = extract_field_value(driver, selector)
        
        fields[field_name] = text
        
        # Add parsed values
        if len(numbers) > 1:
            fields[f'{field_name}_values'] = numbers
            fields[f'{field_name}_min'] = numbers[0]
            fields[f'{field_name}_max'] = numbers[-1]
        elif len(numbers) == 1:
            fields[f'{field_name}_value'] = numbers[0]
    
    return fields


# ============================================================================
# METADATA OPERATIONS (FUNCTIONAL)
# ============================================================================

def save_metadata(sample: Sample, metadata_dir: Path) -> Path:
    """Save sample metadata to JSON file"""
    timestamp_str = sample.timestamp.strftime("%Y%m%d_%H%M%S_%f")
    filename = f"{sample.camera_id}_{timestamp_str}.json"
    filepath = metadata_dir / filename
    
    with open(filepath, 'w') as f:
        json.dump(sample.to_dict(), f, indent=2)
    
    return filepath


def load_metadata(filepath: Path) -> Dict:
    """Load metadata from JSON file"""
    with open(filepath, 'r') as f:
        return json.load(f)


def get_unlabeled_metadata_files(metadata_dir: Path) -> List[Path]:
    """Get all metadata files that haven't been labeled yet"""
    metadata_files = sorted(metadata_dir.glob("*.json"))
    return [f for f in metadata_files if load_metadata(f).get('label') is None]


def update_metadata_label(metadata_file: Path, label: str) -> Dict:
    """Update metadata file with label"""
    metadata = load_metadata(metadata_file)
    metadata['label'] = label
    metadata['labeled_at'] = datetime.now().isoformat()
    
    with open(metadata_file, 'w') as f:
        json.dump(metadata, f, indent=2)
    
    return metadata


# ============================================================================
# STATISTICS (FUNCTIONAL)
# ============================================================================

def calculate_collection_stats(directories: Dict[str, Path]) -> Dict:
    """Calculate statistics about collected data"""
    total_images = len(list(directories['images'].glob("*.png")))
    
    labeled_counts = {
        'person': len(list(directories['person'].glob("*.png"))),
        'no_person': len(list(directories['no_person'].glob("*.png"))),
        'uncertain': len(list(directories['uncertain'].glob("*.png")))
    }
    
    total_labeled = sum(labeled_counts.values())
    
    return {
        'total_samples': total_images,
        'total_labeled': total_labeled,
        'unlabeled': total_images - total_labeled,
        'label_breakdown': labeled_counts
    }


def print_stats(stats: Dict):
    """Pretty print statistics"""
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


# ============================================================================
# DATASET GENERATION (FUNCTIONAL)
# ============================================================================

def generate_training_dataset(metadata_dir: Path, labeled_dir: Path, output_path: Path):
    """Generate CSV dataset from labeled samples"""
    metadata_files = metadata_dir.glob("*.json")
    labeled_samples = []
    
    for metadata_file in metadata_files:
        metadata = load_metadata(metadata_file)
        
        if metadata.get('label'):
            row = {
                'timestamp': metadata['timestamp'],
                'camera_id': metadata['camera_id'],
                'image_path': str(labeled_dir / metadata['label'] / Path(metadata['image_path']).name),
                'label': metadata['label'],
                'labeled_at': metadata['labeled_at']
            }
            
            # Flatten field values
            for field_name, field_value in metadata.get('fields', {}).items():
                row[f'field_{field_name}'] = field_value
            
            labeled_samples.append(row)
    
    if labeled_samples:
        df = pd.DataFrame(labeled_samples)
        df.to_csv(output_path, index=False)
        logging.info(f"Training dataset: {output_path} ({len(labeled_samples)} samples)")
        logging.info(f"Label distribution:\n{df['label'].value_counts()}")
    else:
        logging.warning("No labeled samples found")


# ============================================================================
# BROWSER DRIVER (CLASS - manages state/resources)
# ============================================================================

class BrowserDriver:
    """Manages Selenium WebDriver lifecycle"""
    
    def __init__(self, headless: bool = True):
        self.headless = headless
        self.driver = None
    
    def __enter__(self):
        """Context manager entry"""
        self.start()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        self.close()
    
    def start(self) -> bool:
        """Initialize and start the browser"""
        try:
            options = webdriver.ChromeOptions()
            if self.headless:
                options.add_argument('--headless')
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            options.add_argument('--disable-blink-features=AutomationControlled')
            options.add_argument('--disable-gpu')
            options.add_argument('--window-size=1920,1080')
            options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')
            
            self.driver = webdriver.Chrome(options=options)
            self.driver.set_page_load_timeout(30)
            return True
        except Exception as e:
            logging.error(f"Failed to start browser: {e}")
            return False
    
    def login(self, url: str, username: str, password: str, 
              username_selector: str, password_selector: str, submit_selector: str) -> bool:
        """Perform login"""
        try:
            self.driver.get(url)
            time.sleep(2)
            
            self.driver.find_element(By.CSS_SELECTOR, username_selector).send_keys(username)
            self.driver.find_element(By.CSS_SELECTOR, password_selector).send_keys(password)
            self.driver.find_element(By.CSS_SELECTOR, submit_selector).click()
            
            time.sleep(3)
            return True
        except Exception as e:
            logging.warning(f"Login failed: {e}")
            return False
    
    def close(self):
        """Close the browser"""
        if self.driver:
            try:
                self.driver.quit()
            except Exception as e:
                logging.error(f"Error closing browser: {e}")


# ============================================================================
# SAMPLE COLLECTION (FUNCTIONAL with driver passed in)
# ============================================================================

def collect_sample(driver, config: CameraConfig, directories: Dict[str, Path]) -> Optional[Sample]:
    """
    Collect a single sample from a camera
    
    Args:
        driver: Selenium WebDriver instance
        config: Camera configuration
        directories: Directory paths dict
        
    Returns:
        Sample object or None if failed
    """
    try:
        logging.info(f"Navigating to {config.url}")
        driver.get(config.url)
        
        # Wait for video
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, config.video_selector))
        )
        
        logging.info(f"Waiting {config.wait_time}s for video...")
        time.sleep(config.wait_time)
        
        # Capture
        timestamp = datetime.now()
        timestamp_str = timestamp.strftime("%Y%m%d_%H%M%S_%f")
        
        img_base64 = capture_video_frame(driver, config.video_selector)
        if not img_base64:
            return None
        
        # Save image
        img_filename = f"{config.camera_id}_{timestamp_str}.png"
        img_path = directories['images'] / img_filename
        
        if not save_base64_image(img_base64, img_path):
            return None
        
        logging.info(f"Image saved: {img_filename}")
        
        # Extract fields
        fields = extract_all_fields(driver, config.field_selectors)
        
        # Create sample
        sample = Sample(
            timestamp=timestamp,
            camera_id=config.camera_id,
            url=config.url,
            image_filename=img_filename,
            image_path=img_path,
            fields=fields
        )
        
        # Save metadata
        save_metadata(sample, directories['metadata'])
        
        logging.info(f"✓ Sample captured: {img_filename}")
        return sample
        
    except TimeoutException:
        logging.error("Timeout waiting for video")
        return None
    except Exception as e:
        logging.error(f"Error collecting sample: {e}", exc_info=True)
        return None


def collect_from_all_cameras(camera_configs: List[CameraConfig], 
                            directories: Dict[str, Path],
                            login_config: Optional[Dict] = None) -> Tuple[int, int]:
    """
    Collect samples from all cameras
    
    Returns:
        Tuple of (successful_count, failed_count)
    """
    logging.info("="*60)
    logging.info("Starting collection cycle")
    logging.info("="*60)
    
    successful = 0
    failed = 0
    
    with BrowserDriver(headless=True) as browser:
        if not browser.driver:
            return 0, len(camera_configs)
        
        # Login once if needed
        if login_config:
            browser.login(
                camera_configs[0].url,
                login_config['username'],
                login_config['password'],
                login_config['username_field'],
                login_config['password_field'],
                login_config['submit_button']
            )
        
        # Collect from each camera
        for i, config in enumerate(camera_configs, 1):
            logging.info(f"\nCamera {i}/{len(camera_configs)}: {config.camera_id}")
            
            sample = collect_sample(browser.driver, config, directories)
            if sample:
                successful += 1
            else:
                failed += 1
            
            if i < len(camera_configs):
                time.sleep(2)
    
    logging.info("="*60)
    logging.info(f"Complete: {successful} successful, {failed} failed")
    logging.info("="*60)
    
    return successful, failed


# ============================================================================
# INTERACTIVE LABELING (FUNCTIONAL)
# ============================================================================

def label_sample_interactive(metadata_file: Path) -> Optional[str]:
    """
    Interactively label a single sample
    
    Returns:
        Label string or None if skipped/quit
    """
    metadata = load_metadata(metadata_file)
    
    print(f"\n{'='*60}")
    print(f"Camera: {metadata['camera_id']}")
    print(f"Time: {metadata['timestamp']}")
    print(f"Fields: {json.dumps(metadata['fields'], indent=2)}")
    print(f"Image: {metadata['image_filename']}")
    print(f"{'='*60}")
    
    while True:
        choice = input("Label (p=person, n=no_person, u=uncertain, s=skip, q=quit): ").lower()
        if choice in ['p', 'n', 'u', 's', 'q']:
            break
        print("Invalid input")
    
    if choice == 'q':
        return 'quit'
    if choice == 's':
        return None
    
    label_map = {'p': 'person', 'n': 'no_person', 'u': 'uncertain'}
    return label_map[choice]


def label_batch(directories: Dict[str, Path], batch_size: int = 50):
    """Label a batch of samples"""
    import shutil
    
    unlabeled = get_unlabeled_metadata_files(directories['metadata'])
    
    if not unlabeled:
        logging.info("No unlabeled data found!")
        return
    
    logging.info(f"Found {len(unlabeled)} unlabeled samples")
    
    for i, metadata_file in enumerate(unlabeled[:batch_size], 1):
        print(f"\nSample {i}/{min(batch_size, len(unlabeled))}")
        
        label = label_sample_interactive(metadata_file)
        
        if label == 'quit':
            break
        if label is None:
            continue
        
        # Update metadata
        metadata = update_metadata_label(metadata_file, label)
        
        # Copy image to labeled directory
        src_img = Path(metadata['image_path'])
        dst_img = directories[label] / src_img.name
        shutil.copy(src_img, dst_img)
        
        logging.info(f"Labeled as '{label}': {src_img.name}")
    
    # Generate dataset
    dataset_path = directories['root'] / "training_dataset.csv"
    generate_training_dataset(directories['metadata'], directories['labeled'], dataset_path)


# ============================================================================
# CONFIGURATION LOADING (FUNCTIONAL)
# ============================================================================

def load_config_file(config_path: str) -> Dict:
    """Load configuration from JSON file"""
    with open(config_path, 'r') as f:
        return json.load(f)


def parse_camera_configs(config_data: Dict) -> List[CameraConfig]:
    """Parse camera configurations from config dict"""
    return [CameraConfig(**cam) for cam in config_data['cameras']]


# ============================================================================
# MAIN ENTRY POINT
# ============================================================================

def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(description='Thermal Data Collector')
    parser.add_argument('--config', type=str, required=True, help='Config JSON path')
    parser.add_argument('--output-dir', type=str, default='thermal_data', help='Output directory')
    parser.add_argument('--label', action='store_true', help='Run labeling mode')
    parser.add_argument('--stats', action='store_true', help='Show statistics')
    
    args = parser.parse_args()
    
    # Setup
    output_dir = Path(args.output_dir)
    directories = create_directory_structure(output_dir)
    logger = setup_logging(directories['logs'])
    
    # Load config
    config_data = load_config_file(args.config)
    camera_configs = parse_camera_configs(config_data)
    
    try:
        if args.stats:
            stats = calculate_collection_stats(directories)
            print_stats(stats)
            
        elif args.label:
            label_batch(directories, batch_size=100)
            
        else:
            successful, failed = collect_from_all_cameras(
                camera_configs,
                directories,
                config_data.get('login')
            )
            sys.exit(0 if successful > 0 else 1)
            
    except Exception as e:
        logger.error(f"Fatal error: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
