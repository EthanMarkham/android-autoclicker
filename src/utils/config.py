"""Configuration management for Android AutoClicker"""

import json
import os
from pathlib import Path
from typing import Dict, Any, Optional
from src.utils.logging import app_logger

class Config:
    """Configuration manager for Android AutoClicker"""
    
    # Default configuration values
    DEFAULT_CONFIG = {
        "click_speed": {
            "min_delay": 0.1,
            "max_delay": 0.2,
            "description": "Random delay range between clicks in seconds"
        },
        "image_matching": {
            "threshold": 0.8,
            "description": "Template matching confidence threshold (0.0-1.0)"
        },
        "automation": {
            "scan_interval": 30,
            "random_offset": 2,
            "description": "How often to rescan for template and click randomization offset. Set to null to skip rescanning."
        },
        "click_mode": {
            "mode": "template",
            "description": "Click mode: 'template' for image matching, 'coordinates' for direct coordinates"
        },
        "coordinates": {
            "x": None,
            "y": None,
            "description": "Fixed coordinates for clicking (only used when click_mode is 'coordinates')"
        },
        "paths": {
            "template_path": "images/default.png",
            "tmp_directory": "tmp",
            "description": "Default paths for templates and temporary files"
        },
        "cleanup": {
            "max_age_hours": 24,
            "description": "Maximum age of temporary files before cleanup"
        },
        "logging": {
            "max_file_size_mb": 10,
            "description": "Maximum log file size in MB"
        }
    }
    
    def __init__(self, config_path: Optional[str] = None):
        """Initialize configuration
        
        Args:
            config_path: Path to configuration file. If None, uses default locations.
        """
        self.config_path = self._find_config_file(config_path)
        self.config = self._load_config()
        
    def _find_config_file(self, config_path: Optional[str]) -> Optional[str]:
        """Find configuration file in order of preference"""
        if config_path and os.path.exists(config_path):
            return config_path
            
        # Check for config.json in current directory
        if os.path.exists("config.json"):
            return "config.json"
            
        # Check for config.json in executable directory (when running as .exe)
        if hasattr(os, 'sys') and getattr(os.sys, 'frozen', False):
            exe_dir = os.path.dirname(os.sys.executable)
            exe_config = os.path.join(exe_dir, "config.json")
            if os.path.exists(exe_config):
                return exe_config
                
        return None
    
    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from file or use defaults"""
        if not self.config_path or not os.path.exists(self.config_path):
            app_logger.info("No config file found, using default configuration")
            return self._create_default_config()
            
        try:
            with open(self.config_path, 'r') as f:
                file_config = json.load(f)
                
            # Merge with defaults, file config takes precedence
            config = self._merge_configs(self.DEFAULT_CONFIG, file_config)
            app_logger.info(f"Loaded configuration from: {self.config_path}")
            return config
            
        except Exception as e:
            app_logger.warning(f"Failed to load config file: {e}")
            app_logger.warning("Using default configuration")
            return self._create_default_config()
    
    def _create_default_config(self) -> Dict[str, Any]:
        """Create default configuration and save to file"""
        config = self.DEFAULT_CONFIG.copy()
        
        # Try to save default config for future use
        try:
            default_path = "config.json"
            with open(default_path, 'w') as f:
                json.dump(config, f, indent=2)
            app_logger.info(f"Created default configuration file: {default_path}")
        except Exception as e:
            app_logger.debug(f"Could not create default config file: {e}")
            
        return config
    
    def _merge_configs(self, default: Dict[str, Any], file_config: Dict[str, Any]) -> Dict[str, Any]:
        """Recursively merge file config with defaults"""
        result = default.copy()
        
        for key, value in file_config.items():
            if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                result[key] = self._merge_configs(result[key], value)
            else:
                result[key] = value
                
        return result
    
    def get(self, key_path: str, default: Any = None) -> Any:
        """Get configuration value using dot notation
        
        Args:
            key_path: Dot-separated path to config value (e.g., 'click_speed.min_delay')
            default: Default value if key not found
            
        Returns:
            Configuration value or default
        """
        keys = key_path.split('.')
        value = self.config
        
        try:
            for key in keys:
                value = value[key]
            return value
        except (KeyError, TypeError):
            return default
    
    def set(self, key_path: str, value: Any) -> None:
        """Set configuration value using dot notation
        
        Args:
            key_path: Dot-separated path to config value
            value: Value to set
        """
        keys = key_path.split('.')
        config = self.config
        
        # Navigate to parent of target key
        for key in keys[:-1]:
            if key not in config:
                config[key] = {}
            config = config[key]
            
        # Set the value
        config[keys[-1]] = value
    
    def save(self, path: Optional[str] = None) -> bool:
        """Save current configuration to file
        
        Args:
            path: Optional path to save to. Uses current config_path if None.
            
        Returns:
            True if saved successfully, False otherwise
        """
        save_path = path or self.config_path or "config.json"
        
        try:
            with open(save_path, 'w') as f:
                json.dump(self.config, f, indent=2)
            app_logger.info(f"Configuration saved to: {save_path}")
            return True
        except Exception as e:
            app_logger.error(f"Failed to save configuration: {e}")
            return False
    
    def validate(self) -> bool:
        """Validate current configuration values
        
        Returns:
            True if configuration is valid, False otherwise
        """
        try:
            # Validate click speed
            min_delay = self.get('click_speed.min_delay', 0.1)
            max_delay = self.get('click_speed.max_delay', 0.2)
            if min_delay < 0 or max_delay < 0 or min_delay > max_delay:
                app_logger.error("Invalid click speed configuration: min_delay must be <= max_delay and both >= 0")
                return False
            
            # Validate threshold
            threshold = self.get('image_matching.threshold', 0.8)
            if not 0.0 <= threshold <= 1.0:
                app_logger.error("Invalid image matching threshold: must be between 0.0 and 1.0")
                return False
            
            # Validate scan interval (can be null to skip rescanning)
            scan_interval = self.get('automation.scan_interval', 30)
            if scan_interval is not None and scan_interval < 1:
                app_logger.error("Invalid scan interval: must be >= 1 second or null")
                return False
            
            # Validate random offset
            random_offset = self.get('automation.random_offset', 2)
            if random_offset < 0:
                app_logger.error("Invalid random offset: must be >= 0")
                return False
            
            # Validate click mode
            click_mode = self.get('click_mode.mode', 'template')
            if click_mode not in ['template', 'coordinates']:
                app_logger.error("Invalid click mode: must be 'template' or 'coordinates'")
                return False
            
            # Validate coordinates if using coordinate mode
            if click_mode == 'coordinates':
                x = self.get('coordinates.x')
                y = self.get('coordinates.y')
                if x is None or y is None:
                    app_logger.error("Coordinates mode requires both x and y coordinates to be set")
                    return False
                if not isinstance(x, (int, float)) or not isinstance(y, (int, float)):
                    app_logger.error("Coordinates must be numeric values")
                    return False
                if x < 0 or y < 0:
                    app_logger.error("Coordinates must be non-negative")
                    return False
                
            return True
            
        except Exception as e:
            app_logger.error(f"Configuration validation error: {e}")
            return False

# Global configuration instance
config = Config()
