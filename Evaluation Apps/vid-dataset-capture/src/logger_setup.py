# ============================================================================
# LOGGING (FUNCTIONAL)
# ============================================================================
import logging
import sys
from pathlib import Path
from datetime import datetime

def setup_logging(log_dir: Path, level=logging.INFO):
    """
    Configure root logger - affects ALL module loggers
    Call this ONCE in main()
    """
    log_file = log_dir / f"collector_{datetime.now().strftime('%Y%m')}.log"
    
    # Configure root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(level)
    root_logger.handlers = []  # Clear existing
    
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # File handler
    file_handler = logging.FileHandler(log_file)
    file_handler.setFormatter(formatter)
    root_logger.addHandler(file_handler)
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    root_logger.addHandler(console_handler)
