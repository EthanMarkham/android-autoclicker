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
        template_path: Path to the template image to search for
    """
    try:
        app_logger.info(f"Starting automation with template: {template_path}")
        location = find_template(device_id, template_path)
        
        if location is None:
            app_logger.error(f"Template not found on initial scan: {template_path}")
            app_logger.error("Please ensure the template image is visible on screen")
            sys.exit(1)
        
        app_logger.info(f"Template found at initial location: {location}")
        update_time = time.time()

        while True:
           # Check every 30 seconds
            if (time.time() - update_time) > 30:
                # Update update time
                update_time = time.time()
                
                #Clean up temp files
                clean_up(device_id)
                
                # Grab location / exit if not found
                time.sleep(0.2);
                location = find_template(device_id, template_path)
                if location is None:
                    app_logger.error(f"Template not found during periodic check: {template_path}")
                    app_logger.error("Stopping automation - template may have moved or disappeared")
                    clean_up(device_id)
                    sys.exit(1)
                
                app_logger.debug(f"Template relocated to: {location}")

            random_x = random.randint(location[0] - 2, location[0] + 2)
            random_y = random.randint(location[1] - 2, location[1] + 2)
            tap_screen(device_id, random_x, random_y)

            #random delay between 0.1 and 0.2 seconds
            time.sleep(random.uniform(0.1, 0.2))
        
    except KeyboardInterrupt:
        app_logger.info("Received keyboard interrupt, cleaning up...")
        clean_up(device_id)
        app_logger.info("Cleanup complete, exiting...")