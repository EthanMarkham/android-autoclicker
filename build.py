#!/usr/bin/env python3
"""
Build script for Android AutoClicker
Creates standalone executable using PyInstaller
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def clean_build_dirs():
    """Clean previous build artifacts"""
    dirs_to_clean = ['build', 'dist', '__pycache__']
    for dir_name in dirs_to_clean:
        if os.path.exists(dir_name):
            print(f"Cleaning {dir_name}/...")
            try:
                shutil.rmtree(dir_name)
            except PermissionError:
                print(f"Warning: Could not remove {dir_name}/ (files in use)")

def build_executable():
    """Build the executable using PyInstaller"""
    print("Building Android AutoClicker executable...")
    
    # PyInstaller command using spec file
    cmd = [
        'pyinstaller',
        '--clean',  # Clean PyInstaller cache
        'android-autoclicker.spec'  # Use spec file
    ]
    
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print("Build successful!")
        print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Build failed: {e}")
        print(f"Error output: {e.stderr}")
        return False

def create_standalone_package():
    """Create a standalone package with ADB instructions"""
    print("Creating standalone package...")
    
    # Create dist directory if it doesn't exist
    dist_dir = Path('dist')
    if not dist_dir.exists():
        dist_dir.mkdir()
    
    # Create standalone directory
    standalone_dir = dist_dir / 'android-autoclicker'
    if standalone_dir.exists():
        if standalone_dir.is_file():
            standalone_dir.unlink()  # Remove if it's a file
        else:
            shutil.rmtree(standalone_dir)  # Remove if it's a directory
    standalone_dir.mkdir()
    
    # Handle different platform outputs
    if os.name == 'nt':
        # Windows: single .exe file
        exe_name = 'android-autoclicker.exe'
        exe_path = dist_dir / exe_name
        if exe_path.exists():
            shutil.copy2(exe_path, standalone_dir / exe_name)
            print(f"Copied {exe_name} to standalone package")
        else:
            print(f"Warning: Executable {exe_name} not found!")
            return None
    else:
        # macOS/Linux: directory structure
        exe_name = 'android-autoclicker'
        exe_dir = dist_dir / exe_name
        
        if exe_dir.exists() and exe_dir.is_dir():
            # Copy the entire directory contents
            for item in exe_dir.iterdir():
                if item.is_file():
                    shutil.copy2(item, standalone_dir / item.name)
                    if item.name == exe_name:
                        os.chmod(standalone_dir / exe_name, 0o755)
                        print(f"Copied {exe_name} to standalone package")
                elif item.is_dir():
                    shutil.copytree(item, standalone_dir / item.name)
            print(f"Copied {exe_name} directory contents to standalone package")
        else:
            print(f"Warning: Executable directory {exe_name} not found!")
            return None
    
    # Copy images directory
    if Path('images').exists():
        shutil.copytree('images', standalone_dir / 'images')
        print("Copied images directory to standalone package")
    
    # Copy config file if it exists
    if Path('config.json').exists():
        shutil.copy2('config.json', standalone_dir / 'config.json')
        print("Copied config.json to standalone package")
    else:
        # Create default config file
        from src.utils.config import Config
        config = Config()
        config.save(str(standalone_dir / 'config.json'))
        print("Created default config.json in standalone package")
    
    # Create README for standalone version
    readme_content = """# Android AutoClicker

## Prerequisites
1. **ADB (Android Debug Bridge) must be installed and in your PATH**
   - Download from: https://developer.android.com/studio/releases/platform-tools
   - Extract and add to your system PATH
   - Test by running: `adb version`

2. **Enable USB Debugging on your Android device**
   - Go to Settings > Developer Options > USB Debugging
   - Connect device via USB
   - Test by running: `adb devices`

## Usage
```bash
# Use default template
./android-autoclicker

# Use custom template
./android-autoclicker /path/to/your/template.png

# Enable debug logging
./android-autoclicker --debug

# Select specific device (when multiple connected)
./android-autoclicker --device 1

# Override configuration values
./android-autoclicker --threshold 0.9 --click-speed 0.05 0.15

# Click at specific coordinates
./android-autoclicker --coordinates 500 300

# Disable template rescanning
./android-autoclicker --scan-interval 0

# Use coordinate mode
./android-autoclicker --click-mode coordinates

# Use custom config file
./android-autoclicker --config /path/to/config.json
```

## Configuration
The bot uses `config.json` for settings. You can:
1. Edit `config.json` directly to change default values
2. Use command line arguments to override specific settings
3. Create your own config file with `--config` option

### Available Settings
- **click_speed**: Random delay range between clicks (seconds)
- **image_matching.threshold**: Template matching confidence (0.0-1.0)
- **automation.scan_interval**: How often to rescan for template (seconds). Set to null to disable.
- **automation.random_offset**: Click randomization offset (pixels)
- **click_mode.mode**: Click mode - "template" or "coordinates"
- **coordinates.x/y**: Fixed coordinates for clicking (coordinate mode only)

## Template Images
- Place your template images in the same directory as the executable
- Supported formats: PNG, JPG, JPEG
- The bot will search for the template on screen and click near it

## Troubleshooting
- If "No devices connected" error: Check ADB installation and USB debugging
- If "Template not found" error: Ensure template image is visible on screen
- For more help, run: `./android-autoclicker --help`
"""
    
    with open(standalone_dir / 'README.txt', 'w') as f:
        f.write(readme_content)
    
    print(f"Standalone package created: {standalone_dir}")
    return standalone_dir

def main():
    """Main build process"""
    print("=== Android AutoClicker Build Script ===")
    
    # Check if PyInstaller is installed
    try:
        import PyInstaller
        print(f"PyInstaller version: {PyInstaller.__version__}")
    except ImportError:
        print("PyInstaller not found. Installing...")
        subprocess.run([sys.executable, '-m', 'pip', 'install', 'pyinstaller'], check=True)
    
    # Clean previous builds
    clean_build_dirs()
    
    # Build executable
    if build_executable():
        print("\n[SUCCESS] Executable built successfully!")
        
        # Create standalone package
        standalone_dir = create_standalone_package()
        
        if standalone_dir:
            print(f"\n[COMPLETE] Build complete!")
            print(f"Standalone package: {standalone_dir}")
            print("\nTo distribute:")
            print(f"1. Share the entire '{standalone_dir.name}' folder")
            print("2. Recipients need ADB installed (see README.txt)")
            print("3. They can run: android-autoclicker --help")
        else:
            print("\n[ERROR] Failed to create standalone package!")
    else:
        print("\n[ERROR] Build failed!")
        sys.exit(1)

if __name__ == '__main__':
    main()
