"""Core ADB functionality"""

import subprocess
import time
from typing import List
from src.utils.logging import app_logger

def get_device_list() -> List[str]:
    """Get list of connected devices"""
    try:
        cmd = "adb devices"
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode == 0:
            # Parse output and get device IDs
            lines = result.stdout.strip().split('\n')[1:]  # Skip first line
            devices = []
            for line in lines:
                if line.strip():
                    device_id = line.split()[0]
                    devices.append(device_id)
            return devices
        else:
            app_logger.error(f"Error getting device list: {result.stderr}")
            return []
            
    except Exception as e:
        app_logger.error(f"Error getting device list: {e}")
        return []

def tap_screen(device_id: str, x: int, y: int) -> bool:
    """Tap screen at coordinates"""
    try:
        cmd = f"adb -s {device_id} shell input tap {x} {y}"
        result = subprocess.run(cmd, capture_output=True, text=True)
        return result.returncode == 0
        
    except Exception as e:
        app_logger.error(f"Error tapping screen: {e}")
        return False
