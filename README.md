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

   # Custom template with debug
   ./android-autoclicker /path/to/your/template.png --debug
   ```

## Command Line Options

```
usage: android-autoclicker [-h] [--debug] [template_path]

Android Autoclicker - Automated clicking bot for mobile games

positional arguments:
  template_path  Path to the template image to search for (default: images/default.png)

options:
  -h, --help     show this help message and exit
  --debug        Enable debug logging
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

1. **Screenshot**: Takes a screenshot of the connected Android device
2. **Template Matching**: Uses OpenCV to find the template image on screen
3. **Clicking**: Clicks near the found location with small random variations
4. **Monitoring**: Re-scans every 30 seconds to handle screen changes
5. **Cleanup**: Automatically cleans up temporary files

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
