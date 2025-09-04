"""Common helper utilities"""

import os
import time
from pathlib import Path
from typing import Optional
from src.utils.logging import app_logger
import subprocess

def ensure_dir(path: str) -> None:
    """Ensure directory exists"""
    Path(path).mkdir(parents=True, exist_ok=True)

def cleanup_temp_files(directory: str = "tmp", max_age_hours: int = 24) -> None:
    """Clean up temporary files older than max_age_hours"""
    try:
        if os.path.exists(directory):
            current_time = time.time()
            for file in os.listdir(directory):
                if file == '.gitkeep':  # Skip .gitkeep file
                    continue
                    
                file_path = os.path.join(directory, file)
                try:
                    if os.path.isfile(file_path):
                        os.unlink(file_path)
                        app_logger.debug(f"Cleaned up file: {file_path}")
                except Exception as e:
                    app_logger.error(f"Error deleting {file_path}: {e}")
            app_logger.info("Temporary files cleanup complete")
    except Exception as e:
        app_logger.error(f"Error cleaning up temp files: {e}")

def cleanup_device_screenshots(device_id: str) -> None:
    """Clean up screenshots from device"""
    try:
        cmd = f"adb -s {device_id} shell rm -f /sdcard/screen*.png"
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode == 0:
            app_logger.debug("Cleaned up device screenshots")
        else:
            app_logger.warning(f"Failed to clean device screenshots: {result.stderr}")
    except Exception as e:
        app_logger.error(f"Error cleaning device screenshots: {e}")

def clean_up(device_id: str):
    """Clean up temp files and device screenshots"""
    cleanup_temp_files()
    cleanup_device_screenshots(device_id)
    
def check_adb_installation() -> bool:
    """Check if ADB is installed and accessible"""
    try:
        result = subprocess.run(['adb', 'version'], capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            app_logger.debug("ADB is installed and accessible")
            return True
        else:
            return False
    except (subprocess.TimeoutExpired, FileNotFoundError, subprocess.SubprocessError):
        return False

def get_connected_device() -> Optional[str]:
    """Get the first connected device ID"""
    # First check if ADB is installed
    if not check_adb_installation():
        app_logger.error("❌ ADB (Android Debug Bridge) is not installed or not in PATH")
        app_logger.error("")
        app_logger.error("Please install ADB:")
        app_logger.error("1. Download from: https://developer.android.com/studio/releases/platform-tools")
        app_logger.error("2. Extract the files")
        app_logger.error("3. Add the folder to your system PATH")
        app_logger.error("4. Restart your terminal/command prompt")
        app_logger.error("5. Test by running: adb version")
        app_logger.error("")
        app_logger.error("For detailed instructions, visit:")
        app_logger.error("https://developer.android.com/studio/command-line/adb")
        return None
    
    # Import here to avoid circular dependency
    from src.core.adb import get_device_list
    devices = get_device_list()
    if not devices:
        app_logger.error("No devices connected")
        app_logger.error("")
        app_logger.error("Please ensure:")
        app_logger.error("1. Your Android device is connected via USB")
        app_logger.error("2. USB Debugging is enabled in Developer Options")
        app_logger.error("3. You've authorized the computer on your device")
        app_logger.error("4. Test by running: adb devices")
        return None
    if len(devices) > 1:
        app_logger.warning(f"Multiple devices found, using first one: {devices[0]}")
    return devices[0] 