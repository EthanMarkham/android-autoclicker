"""Image processing utilities"""

import subprocess
import time
import cv2
from typing import Optional, Tuple, List
from src.utils.logging import app_logger

def find_template(device_id: str, template_path: str, threshold: Optional[float] = None) -> Optional[Tuple[int, int]]:
    """Find a template in the current screen without waiting
    
    Args:
        device_id: ADB device ID
        template_path: Path to template image
        threshold: Match confidence threshold. If None, uses config value.
        
    Returns:
        Tuple of (x, y) coordinates if found, None otherwise
    """
    # Use config threshold if not provided
    if threshold is None:
        from src.utils.config import config
        threshold = config.get('image_matching.threshold', 0.8)
    try:
        # Take screenshot
        screenshot_path = f"tmp/screen_{int(time.time())}.png"
        result = subprocess.run(
            f"adb -s {device_id} exec-out screencap -p > {screenshot_path}",
            shell=True
        )
        if result.returncode != 0:
            app_logger.error("Failed to capture screenshot")
            return None
            
        screenshot = cv2.imread(screenshot_path)
        if screenshot is None:
            app_logger.error("Failed to load screenshot")
            return None
            
        # Load template
        template = cv2.imread(template_path)
        if template is None:
            app_logger.error(f"Failed to load template: {template_path}")
            return None
            
        # Match template
        result = cv2.matchTemplate(screenshot, template, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
        
        if max_val >= threshold:
            # Get center point
            w, h = template.shape[1], template.shape[0]
            x = max_loc[0] + w//2
            y = max_loc[1] + h//2
            app_logger.debug(f"Found template at ({x}, {y}) with confidence {max_val:.2f}")
            return (x, y)
            
        return None
        
    except Exception as e:
        app_logger.error(f"Error finding template: {e}")
        return None 
