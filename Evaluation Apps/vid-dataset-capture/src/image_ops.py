# ============================================================================
# IMAGE OPERATIONS (FUNCTIONAL)
# ============================================================================
import base64
import logging
from pathlib import Path
from typing import Optional

logger = logging.getLogger(__name__)

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
        logger.error(f"Failed to capture frame: {e}")
        return None


def save_base64_image(img_base64: str, output_path: Path) -> bool:
    """Save base64 encoded image to file"""
    try:
        with open(output_path, 'wb') as f:
            f.write(base64.b64decode(img_base64))
        return True
    except Exception as e:
        logger.error(f"Failed to save image: {e}")
        return False
