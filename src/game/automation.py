"""Game automation module"""

import random
import time
import sys

from src.core.image_processing import find_template
from src.utils.logging import app_logger
from src.utils.helpers import clean_up
from src.core.adb import tap_screen

def run_automation(device_id: str, template_path: str = "images/default.png"):
    """Full secretary automation including initial navigation
    
    Args:
        device_id: ADB device ID to control
        template_path: Path to the template image to search for (ignored in coordinate mode)
    """
    from src.utils.config import config
    
    # Get configuration values
    scan_interval = config.get('automation.scan_interval', 30)
    random_offset = config.get('automation.random_offset', 2)
    min_delay = config.get('click_speed.min_delay', 0.1)
    max_delay = config.get('click_speed.max_delay', 0.2)
    click_mode = config.get('click_mode.mode', 'template')
    
    try:
        if click_mode == 'coordinates':
            # Coordinate-based clicking mode
            x = config.get('coordinates.x')
            y = config.get('coordinates.y')
            
            if x is None or y is None:
                app_logger.error("Coordinates mode requires both x and y coordinates to be set in config")
                sys.exit(1)
            
            app_logger.info(f"Starting automation in coordinate mode at ({x}, {y})")
            location = (x, y)
            
        else:
            # Template-based clicking mode
            app_logger.info(f"Starting automation with template: {template_path}")
            location = find_template(device_id, template_path)
            
            if location is None:
                app_logger.error(f"Template not found on initial scan: {template_path}")
                app_logger.error("Please ensure the template image is visible on screen")
                sys.exit(1)
            
            app_logger.info(f"Template found at initial location: {location}")
        
        update_time = time.time()
        last_location = location

        while True:
            # Check every scan_interval seconds (if scan_interval is not null)
            if scan_interval is not None and (time.time() - update_time) > scan_interval:
                # Update update time
                update_time = time.time()
                
                # Clean up temp files
                clean_up(device_id)
                
                if click_mode == 'template':
                    # Re-scan for template location
                    time.sleep(0.2)
                    location = find_template(device_id, template_path)
                    if location is None:
                        app_logger.error(f"Template not found during periodic check: {template_path}")
                        app_logger.error("Stopping automation - template may have moved or disappeared")
                        clean_up(device_id)
                        sys.exit(1)
                    
                    app_logger.debug(f"Template relocated to: {location}")
                    last_location = location
                # In coordinate mode, we don't need to rescan - use fixed coordinates
            
            # Use last known location (either from template or fixed coordinates)
            current_location = last_location if click_mode == 'template' else location
            
            # Add randomization to click position
            random_x = random.randint(current_location[0] - random_offset, current_location[0] + random_offset)
            random_y = random.randint(current_location[1] - random_offset, current_location[1] + random_offset)
            
            tap_screen(device_id, random_x, random_y)

            # Random delay between min_delay and max_delay seconds
            time.sleep(random.uniform(min_delay, max_delay))
        
    except KeyboardInterrupt:
        app_logger.info("Received keyboard interrupt, cleaning up...")
        clean_up(device_id)
        app_logger.info("Cleanup complete, exiting...")