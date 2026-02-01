# Teleprompter for OBS

A Python script for OBS Studio that creates a smooth scrolling teleprompter overlay for live streaming and video recording.

## Features

- 📜 Smooth auto-scrolling text display
- ⌨️ Hotkey controls (start/stop, speed adjustment)
- 🎨 Customizable font, size, and alignment
- 🖱️ Mouse wheel speed control
- 🔄 Reset position function

## Installation

1. Open OBS Studio
2. Go to **Tools** → **Scripts**
3. Click **+** and select `teleprompter.py`
4. Configure the script in the OBS Scripts panel

## Controls

| Control | Action |
|---------|--------|
| Space | Start/Stop scrolling |
| Up Arrow | Increase scroll speed |
| Down Arrow | Decrease scroll speed |
| Mouse Wheel | Adjust speed |
| Reset Button | Reset scroll position |

## Configuration

In the OBS Scripts panel, you can configure:

- **Teleprompter Text**: The script content to display
- **Scroll Speed**: Pixels per frame (1-10)
- **Font Size**: Text size in pixels
- **Alignment**: Left, center, or right
- **Line Height**: Spacing between lines

## Setup

1. Create a **Browser Source** in OBS named `Teleprompter_Text`
2. Load the script via OBS Scripts
3. Enter your script text in the configuration
4. Use hotkeys to control during streaming

## Requirements

- OBS Studio 27.0+
- Python 3.6+ (bundled with OBS on Windows)

## License

MIT License - see [LICENSE](LICENSE) for details.
