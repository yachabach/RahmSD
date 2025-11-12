# ============================================================================
# SAMPLE COLLECTION (FUNCTIONAL with driver passed in)
# ============================================================================
import logging
import time
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from data_structures import CameraConfig, Sample
from image_ops import capture_video_frame, save_base64_image
from metadata_ops import save_metadata, extract_all_fields
from browser_driver import BrowserDriver

logger = logging.getLogger(__name__)

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
        logger.info(f"Navigating to {config.url}")
        driver.get(config.url)
        
        # Wait for video
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, config.video_selector))
        )
        
        logger.info(f"Waiting {config.wait_time}s for video...")
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
        
        logger.info(f"Image saved: {img_filename}")
        
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
        
        logger.info(f"✓ Sample captured: {img_filename}")
        return sample
        
    except TimeoutException:
        logger.error("Timeout waiting for video")
        return None
    except Exception as e:
        logger.error(f"Error collecting sample: {e}", exc_info=True)
        return None

def collect_from_all_cameras(camera_configs: List[CameraConfig], 
                            directories: Dict[str, Path],
                            login_config: Optional[Dict] = None) -> Tuple[int, int]:
    """
    Collect samples from all cameras
    
    Returns:
        Tuple of (successful_count, failed_count)
    """
    logger.info("="*60)
    logger.info("Starting collection cycle")
    logger.info("="*60)
    
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
            logger.info(f"\nCamera {i}/{len(camera_configs)}: {config.camera_id}")
            
            sample = collect_sample(browser.driver, config, directories)
            if sample:
                successful += 1
            else:
                failed += 1
            
            if i < len(camera_configs):
                time.sleep(2)
    
    logger.info("="*60)
    logger.info(f"Complete: {successful} successful, {failed} failed")
    logger.info("="*60)
    
    return successful, failed
