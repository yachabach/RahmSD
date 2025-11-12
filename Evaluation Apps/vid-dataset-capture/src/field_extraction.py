# ============================================================================
# FIELD EXTRACTION (FUNCTIONAL)
# ============================================================================
import re
import logging
from typing import List, Dict, Tuple, Optional
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

logger = logging.getLogger(__name__)

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
        logger.warning(f"Error extracting field: {e}")
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

