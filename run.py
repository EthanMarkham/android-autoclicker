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
  android-autoclicker                           # Use default template (images/default.png)
  android-autoclicker /path/to/template.png     # Use custom template
  android-autoclicker --debug                   # Enable debug logging
  android-autoclicker /path/to/template.png --debug  # Custom template with debug logging
        """
    else:
        # Running as Python script
        program_name = "python run.py"
        examples = """
Examples:
  python run.py                           # Use default template (images/default.png)
  python run.py /path/to/template.png     # Use custom template
  python run.py --debug                   # Enable debug logging
  python run.py /path/to/template.png --debug  # Custom template with debug logging
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
    
    return parser.parse_args()

def main():
    try:
        # Parse command line arguments
        args = parse_arguments()
        
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
        
        # Create debug screenshot directory
        ensure_dir("tmp")
        
        # Get connected device
        device_id = get_connected_device()
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