"""Logging configuration for the application"""

import logging
import sys
from pathlib import Path
from logging.handlers import RotatingFileHandler

# Create logger
app_logger = logging.getLogger('android-autoclicker')
app_logger.setLevel(logging.INFO)

def setup_logging(debug: bool = False):
    """Set up logging configuration"""
    # Clear any existing handlers
    app_logger.handlers.clear()
    
    # Set log level
    app_logger.setLevel(logging.DEBUG if debug else logging.INFO)
    
    # Create console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.DEBUG if debug else logging.INFO)
    
    # Create formatter
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    console_handler.setFormatter(formatter)
    
    # Add handler to logger
    app_logger.addHandler(console_handler)
    
    # Create log directory if it doesn't exist
    log_dir = Path('logs')
    log_dir.mkdir(exist_ok=True)
    
    # Create rotating file handler (10MB per file, keep 5 backup files)
    file_handler = RotatingFileHandler(
        log_dir / 'android-autoclicker.log',
        maxBytes=10*1024*1024,  # 10MB
        backupCount=5
    )
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    
    # Add file handler to logger
    app_logger.addHandler(file_handler) 