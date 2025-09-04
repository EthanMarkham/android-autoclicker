# Android Autoclicker

An automated clicking bot for mobile games using ADB (Android Debug Bridge) and computer vision.

## Features

- 🎯 **Template Matching**: Finds and clicks on specific images on screen
- 📱 **ADB Integration**: Works with any Android device via USB debugging
- 🖼️ **Custom Templates**: Use your own template images
- 📊 **Debug Logging**: Detailed logging for troubleshooting
- 🚀 **Standalone Executable**: No Python installation required for end users

## Quick Start

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

[Add your license here]

## Contributing

[Add contribution guidelines here]
