# ============================================================================
# BROWSER DRIVER (CLASS - manages state/resources)
# ============================================================================
import logging
import time
from selenium import webdriver
from selenium.webdriver.common.by import By

logger = logging.getLogger(__name__)

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
            logger.error(f"Failed to start browser: {e}")
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
            logger.warning(f"Login failed: {e}")
            return False
    
    def close(self):
        """Close the browser"""
        if self.driver:
            try:
                self.driver.quit()
            except Exception as e:
                logger.error(f"Error closing browser: {e}")

