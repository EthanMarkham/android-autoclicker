# Android Autoclicker

An automated clicking bot for mobile games using ADB (Android Debug Bridge) and computer vision.

## Features

- 🎯 **Template Matching**: Finds and clicks on specific images on screen
- 📱 **ADB Integration**: Works with any Android device via USB debugging
- 🖼️ **Custom Templates**: Use your own template images
- 📊 **Debug Logging**: Detailed logging for troubleshooting
- 🚀 **Standalone Executable**: No Python installation required for end users
- 📦 **Pre-built Downloads**: Get ready-to-use executables from [GitHub Releases](https://github.com/yourusername/android-autoclicker/releases)

## Quick Start

### For End Users (Recommended)

**Download pre-built executables from GitHub Releases:**

1. **Go to the [Releases page](https://github.com/EthanMarkham/android-autoclicker/releases)**
2. **Download the latest release for your platform:**
   - **Windows**: `android-autoclicker-windows.zip`
   - **macOS**: `android-autoclicker-macos.zip`
   - **Linux**: `android-autoclicker-linux.zip`
3. **Extract the zip file**
4. **Install ADB** (see Prerequisites below)
5. **Run the executable** (see Usage below)

> **Note**: The executables are automatically built and uploaded to GitHub Releases whenever a new version is tagged. No need to build anything yourself!

### For Developers

1. **Clone and setup**:

   ```bash
   git clone <your-repo>
   cd clicker
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. **Run the bot**:

   ```bash
   python run.py --help
   python run.py images/default.png --debug
   ```

3. **Build executable**:
   ```bash
   python build.py
   # Or use the batch script:
   # Windows: build.bat
   # Linux/Mac: ./build.sh
   ```

### For End Users

1. **Prerequisites**:

   - Download and install [ADB Platform Tools](https://developer.android.com/studio/releases/platform-tools)
   - Add ADB to your system PATH
   - Enable USB Debugging on your Android device

2. **Download the portable version** from the `dist/android-autoclicker/` folder

3. **Run the bot**:

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

   # Use custom config file
   ./android-autoclicker --config /path/to/config.json
   ```

## Command Line Options

```
usage: android-autoclicker [-h] [--debug] [--device DEVICE] [--config CONFIG]
                           [--threshold THRESHOLD] [--click-speed MIN MAX]
                           [--scan-interval SCAN_INTERVAL] [--coordinates X Y]
                           [--click-mode {template,coordinates}] [template_path]

Android Autoclicker - Automated clicking bot for mobile games

positional arguments:
  template_path            Path to the template image to search for (default: images/default.png)

options:
  -h, --help              show this help message and exit
  --debug                 Enable debug logging
  --device DEVICE         Device index to use when multiple devices are connected (0-based)
  --config CONFIG         Path to configuration file (default: config.json)
  --threshold THRESHOLD   Image matching threshold (0.0-1.0, overrides config)
  --click-speed MIN MAX   Click speed range in seconds (overrides config)
  --scan-interval SCAN_INTERVAL  Template rescan interval in seconds (overrides config). Use 0 to disable.
  --coordinates X Y       Click coordinates (overrides config, enables coordinate mode)
  --click-mode {template,coordinates}  Click mode (overrides config)
```

## Configuration

The bot uses a `config.json` file for settings. You can:

1. **Edit `config.json` directly** to change default values
2. **Use command line arguments** to override specific settings
3. **Create your own config file** with `--config` option

### Available Settings

- **click_speed**: Random delay range between clicks (seconds)
  - `min_delay`: Minimum delay between clicks
  - `max_delay`: Maximum delay between clicks
- **image_matching**: Template matching settings
  - `threshold`: Confidence threshold (0.0-1.0, higher = more strict)
- **automation**: Automation behavior
  - `scan_interval`: How often to rescan for template (seconds). Set to `null` to disable rescanning
  - `random_offset`: Click randomization offset (pixels)
- **click_mode**: Clicking method
  - `mode`: Either "template" for image matching or "coordinates" for direct coordinates
- **coordinates**: Fixed click coordinates (only used when click_mode is "coordinates")
  - `x`: X coordinate for clicking
  - `y`: Y coordinate for clicking
- **paths**: File paths
  - `template_path`: Default template image path
  - `tmp_directory`: Temporary files directory

### Example Configurations

#### Template Mode (Default)

```json
{
  "click_speed": {
    "min_delay": 0.1,
    "max_delay": 0.2
  },
  "image_matching": {
    "threshold": 0.8
  },
  "automation": {
    "scan_interval": 30,
    "random_offset": 2
  },
  "click_mode": {
    "mode": "template"
  },
  "paths": {
    "template_path": "images/default.png",
    "tmp_directory": "tmp"
  }
}
```

#### Coordinate Mode

```json
{
  "click_speed": {
    "min_delay": 0.1,
    "max_delay": 0.2
  },
  "automation": {
    "scan_interval": null,
    "random_offset": 2
  },
  "click_mode": {
    "mode": "coordinates"
  },
  "coordinates": {
    "x": 500,
    "y": 300
  },
  "paths": {
    "template_path": "images/default.png",
    "tmp_directory": "tmp"
  }
}
```

#### Disable Rescanning

```json
{
  "automation": {
    "scan_interval": null
  }
}
```

## Template Images

- **Supported formats**: PNG, JPG, JPEG
- **Recommended size**: Small, distinctive features work best
- **Placement**: Place template images in the same directory as the executable
- **Tips**:
  - Use high-contrast images
  - Avoid templates that change frequently
  - Test templates before running automation

## How It Works

### Template Mode (Default)

1. **Screenshot**: Takes a screenshot of the connected Android device
2. **Template Matching**: Uses OpenCV to find the template image on screen
3. **Clicking**: Clicks near the found location with small random variations
4. **Monitoring**: Re-scans every 30 seconds (configurable) to handle screen changes
5. **Cleanup**: Automatically cleans up temporary files

### Coordinate Mode

1. **Direct Clicking**: Clicks at fixed coordinates without image processing
2. **Randomization**: Adds small random variations to prevent detection
3. **No Monitoring**: No rescanning needed since coordinates are fixed
4. **Cleanup**: Automatically cleans up temporary files

### Disabled Rescanning

- Set `scan_interval` to `null` or use `--scan-interval 0` to disable template rescanning
- Useful when you're confident the template won't move or when using coordinate mode

## Troubleshooting

### "No devices connected"

- Ensure ADB is installed and in PATH
- Check USB debugging is enabled on device
- Try: `adb devices` to verify connection

### "Template not found"

- Ensure template image is visible on screen
- Try a different template image
- Check image format (PNG/JPG/JPEG)
- Use `--debug` flag for more information

### "Module not found" errors

- Rebuild the executable: `python build.py`
- Ensure all dependencies are installed in venv

## Development

### Project Structure

```
clicker/
├── src/
│   ├── core/           # ADB and image processing
│   ├── game/           # Automation logic
│   └── utils/          # Helper functions and logging
├── images/             # Template images
├── logs/               # Log files
├── tmp/                # Temporary screenshots
├── run.py              # Main entry point
├── build.py            # Build script
└── requirements.txt    # Dependencies
```

### Building from Source

1. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

2. Build executable:

   ```bash
   python build.py
   ```

3. Test the build:
   ```bash
   dist/android-autoclicker.exe --help
   ```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

### MIT License Summary

- ✅ Commercial use allowed
- ✅ Modification allowed
- ✅ Distribution allowed
- ✅ Private use allowed
- ❌ No liability or warranty provided

## GitHub Releases

### How to Get Built Executables

1. **Visit the [Releases page](https://github.com/yourusername/android-autoclicker/releases)**
2. **Find the latest release** (e.g., v1.0.0)
3. **Download the appropriate file for your platform:**
   - `android-autoclicker-windows.zip` - For Windows
   - `android-autoclicker-macos.zip` - For macOS (Intel + Apple Silicon)
   - `android-autoclicker-linux.zip` - For Linux
4. **Extract the zip file** to any folder
5. **Follow the usage instructions** in the extracted README.txt

### Automatic Builds

- **Every time a new version is tagged**, GitHub Actions automatically builds executables for all platforms
- **No manual intervention required** - the builds happen automatically
- **All dependencies included** - just download and run!

### Latest Release

[![Latest Release](https://img.shields.io/github/v/release/yourusername/android-autoclicker?style=for-the-badge)](https://github.com/yourusername/android-autoclicker/releases/latest)

## Contributing

We welcome contributions! Here's how you can help:

### 🐛 Bug Reports

- Use the [Issues](https://github.com/EthanMarkham/android-autoclicker/issues) page
- Include: OS, Python version, error messages, steps to reproduce
- Check existing issues first

### 💡 Feature Requests

- Open an [Issue](https://github.com/EthanMarkham/android-autoclicker/issues) with the "enhancement" label
- Describe the feature and its use case
- Consider if it fits the project's scope

### 🔧 Code Contributions

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/amazing-feature`
3. **Make your changes** and test thoroughly
4. **Commit with clear messages**: `git commit -m "Add amazing feature"`
5. **Push to your fork**: `git push origin feature/amazing-feature`
6. **Open a Pull Request**

### 📋 Development Setup

```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/android-autoclicker.git
cd android-autoclicker

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run tests
python run.py --help

# Build executable
python build.py
```

### 🎯 Areas for Contribution

- **Bug fixes** - Fix issues and improve stability
- **New features** - Add useful functionality
- **Documentation** - Improve README, code comments, examples
- **Testing** - Add tests for better reliability
- **Cross-platform** - Ensure compatibility across platforms
- **Performance** - Optimize image processing and automation speed

### 📝 Code Style

- Follow existing code patterns
- Use clear, descriptive variable names
- Add comments for complex logic
- Keep functions focused and small
- Test your changes thoroughly

### 🤝 Community Guidelines

- Be respectful and constructive
- Help others learn and grow
- Follow the [Code of Conduct](CODE_OF_CONDUCT.md)
- Remember: we're all here to build something great together!

---

**Thank you for contributing to Android AutoClicker!** 🚀
