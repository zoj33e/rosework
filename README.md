# Fistborn Semi-Automatic Roadwork System

A computer vision-based auto roadwork system for Fistborn. This project uses real-time screen capture and template matching to automatically run roadwork.

## Features

- **Real-time Target Tracking**: Uses OpenCV template matching to detect and track waypoints on screen.
- **Multi-scale Detection**: Implements scale-invariant template matching for robust target detection.
- **Smooth Mouse Control**: Provides smooth and natural mouse movement for aiming.
- **Debug Visualization**: Real-time debug window showing detection results and tracking status.
- **Stamina Management**: AutoHotkey script for managing run/walk states based on stamina levels.

## Components

### Python Waypoints tracking (`main.py`)
- Screen capture using MSS
- Template matching with OpenCV
- Smooth mouse movement via Windows API
- Configurable detection parameters
- Real-time debug visualization

### AutoHotkey Stamina Manager (`running.ahk`)
- Automatic stamina detection via pixel color
- Toggle between run and walk modes
- Configurable regeneration delay
- F1/F2/F3 hotkey controls

## Requirements

### Python Dependencies
```bash
pip install opencv-python numpy mss keyboard
```

### Additional Software
- **AutoHotkey**: Required for the stamina management script
- **Windows**: This application is Windows-specific due to mouse control API usage

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/RoadworkV1.git
cd RoadworkV1
```

2. Install Python dependencies:
```bash
pip install -r requirements.txt
```

3. Ensure you have AutoHotkey installed for the stamina script

4. Place your target icon in the `images/` folder as `icon.png` or use the one in the repository.

## Usage

### Waypoints tracking
1. Run the Python script:
```bash
python main.py
```

2. Controls:
- **F1**: Start/Resume tracking
- **F2**: Pause tracking
- **Q**: Quit application

### Stamina Manager
1. Run the AutoHotkey script:
```bash
autohotkey running.ahk
```

2. Controls:
- **F1**: Toggle auto-run on/off
- **F2**: Stop movement
- **F3**: Exit application

## Configuration

### Detection Settings (main.py)
```python
MATCH_THRESHOLD = 0.65       # Detection confidence threshold
SCALES = np.linspace(0.9, 1.1, 3)  # Multi-scale detection range
ROI_RATIO = 0.4              # Screen region to scan (40% of screen)
```

### Mouse Settings
```python
SMOOTH = 6.0                 # Mouse smoothing factor
DEADZONE = 5                 # Pixels from center to ignore
FPS_LIMIT = 60               # Target frame rate
SEARCH_SPEED = 100.0         # Auto-search turning speed
SEARCH_RANGE = 1000          # Maximum search distance
```

### Stamina Settings (running.ahk)
```autohotkey
REGEN_DELAY := 5000          # Stamina regeneration delay (ms)
Pixel coordinates for stamina detection
```

## How It Works

1. **Screen Capture**: Continuously captures a central region of the screen
2. **Template Matching**: Uses multi-scale template matching to find the waypoints.
3. **Mouse Movement**: Applies smooth mouse movement to center the waypoints.
4. **Auto-Search**: When waypoints are lost, performs systematic search pattern.
5. **Stamina Management**: Monitors stamina bar and adjusts movement accordingly.

## File Structure
```
RoadworkV1/
├── main.py              # Main waypoints tracking script
├── running.ahk          # Stamina management script
├── images/
│   └── icon.png         # Target icon for detection
├── README.md           # This file
└── requirements.txt     # Python dependencies
```

## Performance Notes

- **ROI Ratio**: Smaller ROI values improve FPS but reduce detection range
- **Match Threshold**: Higher values reduce false positives but may miss targets
- **Smooth Factor**: Higher values provide smoother movement but slower response
- **Debug Window**: Can be disabled (`SHOW_DEBUG = False`) for better performance

## Compatibility

- **Operating System**: Windows 10/11
- **Python**: 3.7+
- **Display**: Supports multiple monitor setups (uses primary monitor)

## Disclaimer

This software is intended for educational purposes and legitimate gaming applications. Users are responsible for ensuring compliance with game terms of service and applicable laws.

## License

This project is open source. Please refer to the LICENSE file for details.

## Contributing

Feel free to submit issues and enhancement requests!

This repository is released under GPL-3.0 for educational
and research purposes.

The maintained and optimized version of Fistborn is distributed
separately. Commercial redistribution requires explicit permission
from the author.
