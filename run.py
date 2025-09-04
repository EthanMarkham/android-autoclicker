#!/usr/bin/env python3

import sys
import traceback
import argparse
from pathlib import Path

from src.game.automation import run_automation
from src.utils.helpers import get_connected_device, ensure_dir
from src.utils.logging import setup_logging, app_logger

def parse_arguments():
    """Parse command line arguments"""
    # Detect if running as executable
    is_executable = getattr(sys, 'frozen', False)
    
    if is_executable:
        # Running as .exe
        program_name = "android-autoclicker"
        examples = """
Examples:
  android-autoclicker                                    # Use default template (images/default.png)
  android-autoclicker /path/to/template.png              # Use custom template
  android-autoclicker --debug                            # Enable debug logging
  android-autoclicker --device 1                         # Select device by index
  android-autoclicker --config /path/to/config.json      # Use custom config file
  android-autoclicker --threshold 0.9                    # Override image matching threshold
  android-autoclicker --click-speed 0.05 0.15            # Override click speed range
  android-autoclicker --coordinates 500 300              # Click at specific coordinates
  android-autoclicker --scan-interval 0                  # Disable template rescanning
  android-autoclicker --click-mode coordinates            # Use coordinate mode
        """
    else:
        # Running as Python script
        program_name = "python run.py"
        examples = """
Examples:
  python run.py                                    # Use default template (images/default.png)
  python run.py /path/to/template.png              # Use custom template
  python run.py --debug                            # Enable debug logging
  python run.py --device 1                         # Select device by index
  python run.py --config /path/to/config.json      # Use custom config file
  python run.py --threshold 0.9                    # Override image matching threshold
  python run.py --click-speed 0.05 0.15            # Override click speed range
  python run.py --coordinates 500 300              # Click at specific coordinates
  python run.py --scan-interval 0                  # Disable template rescanning
  python run.py --click-mode coordinates            # Use coordinate mode
        """
    
    parser = argparse.ArgumentParser(
        description="Android AutoClicker - Automated clicking bot for Android devices",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=examples
    )
    
    parser.add_argument(
        'template_path',
        nargs='?',
        default='images/default.png',
        help='Path to the template image to search for (default: images/default.png)'
    )
    
    parser.add_argument(
        '--debug',
        action='store_true',
        help='Enable debug logging'
    )
    
    parser.add_argument(
        '--device',
        type=int,
        help='Device index to use when multiple devices are connected (0-based)'
    )
    
    parser.add_argument(
        '--config',
        help='Path to configuration file (default: config.json)'
    )
    
    parser.add_argument(
        '--threshold',
        type=float,
        help='Image matching threshold (0.0-1.0, overrides config)'
    )
    
    parser.add_argument(
        '--click-speed',
        nargs=2,
        type=float,
        metavar=('MIN', 'MAX'),
        help='Click speed range in seconds (overrides config)'
    )
    
    parser.add_argument(
        '--scan-interval',
        type=int,
        help='Template rescan interval in seconds (overrides config). Use 0 to disable rescanning.'
    )
    
    parser.add_argument(
        '--coordinates',
        nargs=2,
        type=int,
        metavar=('X', 'Y'),
        help='Click coordinates (overrides config, enables coordinate mode)'
    )
    
    parser.add_argument(
        '--click-mode',
        choices=['template', 'coordinates'],
        help='Click mode: template for image matching, coordinates for direct coordinates (overrides config)'
    )
    
    return parser.parse_args()

def main():
    try:
        # Parse command line arguments
        args = parse_arguments()
        
        # Initialize configuration
        from src.utils.config import Config
        config = Config(args.config)
        
        # Apply command line overrides
        if args.threshold is not None:
            if not 0.0 <= args.threshold <= 1.0:
                print(f"Error: Threshold must be between 0.0 and 1.0, got {args.threshold}")
                sys.exit(1)
            config.set('image_matching.threshold', args.threshold)
            
        if args.click_speed is not None:
            min_speed, max_speed = args.click_speed
            if min_speed < 0 or max_speed < 0 or min_speed > max_speed:
                print(f"Error: Invalid click speed range: min={min_speed}, max={max_speed}")
                print("Min must be <= max and both must be >= 0")
                sys.exit(1)
            config.set('click_speed.min_delay', min_speed)
            config.set('click_speed.max_delay', max_speed)
            
        if args.scan_interval is not None:
            if args.scan_interval < 0:
                print(f"Error: Scan interval must be >= 0 (use 0 to disable), got {args.scan_interval}")
                sys.exit(1)
            # Convert 0 to None to disable rescanning
            scan_interval_value = None if args.scan_interval == 0 else args.scan_interval
            config.set('automation.scan_interval', scan_interval_value)
            
        if args.coordinates is not None:
            x, y = args.coordinates
            if x < 0 or y < 0:
                print(f"Error: Coordinates must be non-negative, got x={x}, y={y}")
                sys.exit(1)
            config.set('click_mode.mode', 'coordinates')
            config.set('coordinates.x', x)
            config.set('coordinates.y', y)
            
        if args.click_mode is not None:
            config.set('click_mode.mode', args.click_mode)
        
        # Validate configuration
        if not config.validate():
            print("Error: Invalid configuration values")
            sys.exit(1)
        
        # Validate template path
        template_path = Path(args.template_path)
        if not template_path.exists():
            print(f"Error: Template image not found: {template_path}")
            print("Please provide a valid path to an image file.")
            sys.exit(1)
        
        if not template_path.suffix.lower() in ['.png', '.jpg', '.jpeg']:
            print(f"Error: Unsupported image format: {template_path.suffix}")
            print("Please use PNG, JPG, or JPEG images.")
            sys.exit(1)
        
        # Set up logging
        setup_logging(debug=args.debug)
        
        # Log startup information
        app_logger.info(f"Starting Android AutoClicker")
        app_logger.info(f"Template image: {template_path.absolute()}")
        app_logger.info(f"Debug logging: {'enabled' if args.debug else 'disabled'}")
        app_logger.info(f"Configuration: {config.config_path or 'default'}")
        
        # Log configuration values
        click_mode = config.get('click_mode.mode', 'template')
        app_logger.info(f"Click mode: {click_mode}")
        
        if click_mode == 'coordinates':
            x = config.get('coordinates.x')
            y = config.get('coordinates.y')
            app_logger.info(f"Click coordinates: ({x}, {y})")
        else:
            app_logger.info(f"Image threshold: {config.get('image_matching.threshold')}")
            
        app_logger.info(f"Click speed: {config.get('click_speed.min_delay')}-{config.get('click_speed.max_delay')}s")
        scan_interval = config.get('automation.scan_interval')
        if scan_interval is None:
            app_logger.info("Scan interval: disabled (no rescanning)")
        else:
            app_logger.info(f"Scan interval: {scan_interval}s")
        
        # Create debug screenshot directory
        ensure_dir("tmp")
        
        # Get connected device
        device_id = get_connected_device(args.device)
        if not device_id:
            sys.exit(1)
        
        # Run automation with custom template
        run_automation(device_id, str(template_path))
            
    except Exception as e:
        app_logger.error(f"Error: {e}")
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    main() 