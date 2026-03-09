# BSGO Auto-Miner

An intelligent automation bot for Battlestar Galactica Online (BSGO) that leverages AI-powered object detection and automated gameplay to efficiently mine resources across multiple sectors.

## 🎯 Overview

This sophisticated bot automates the mining process in BSGO using:
- **YOLOv5 object detection** for identifying asteroids and resources
- **OCR technology** for game state recognition  
- **Intelligent navigation** with sector pathfinding
- **Combat awareness** and base management
- **GUI configuration** for easy setup and management

## ✨ Features

### Core Automation
- **Autonomous Mining**: Automatically detects and mines asteroids using AI vision
- **Smart Navigation**: Optimal pathfinding between sectors using NetworkX algorithms
- **Combat Detection**: Recognizes damage and responds appropriately
- **Base Management**: Handles repairs, undocking, and reward collection
- **Multi-Sector Support**: Rotates through configured mining sectors

### AI-Powered Detection
- **YOLOv5 Integration**: Custom-trained model for asteroid detection
- **Resource Classification**: Identifies different asteroid types (titanium, tylium, water, etc.)
- **OCR Text Recognition**: Reads game interface elements and coordinates
- **Distance Calculation**: Determines proximity to mining targets

### User Interface
- **Configuration GUI**: Easy-to-use interface for bot setup
- **Sector Selection**: Visual sector picker with multi-selection
- **Scheduling System**: Delayed start with customizable timing
- **Real-time Monitoring**: Console logging with color-coded status updates

## 🔧 System Requirements

### Software Dependencies
- **Python 3.8+**
- **Windows OS** (configured for Windows-specific coordinates)
- **Tesseract OCR** installed at `C:\Program Files\Tesseract-OCR\tesseract.exe`
- **BSGO Game Client** running in windowed mode

### Hardware Requirements
- **GPU support** recommended for YOLOv5 inference
- **Minimum 8GB RAM** for stable operation
- **Dual monitor setup** recommended for monitoring

## 📦 Installation

### 1. Clone Repository
```bash
git clone https://github.com/your-repo/BSGO-Auto-Miner.git
cd BSGO-Auto-Miner
```

### 2. Install Python Dependencies
```bash
# Install YOLOv5 requirements
pip install -r yolov5/requirements.txt

# Install additional dependencies
pip install pytesseract easyocr pyautogui termcolor rapidfuzz networkx opencv-python torch torchvision
```

### 3. Install Tesseract OCR
Download and install Tesseract OCR from: https://github.com/tesseract-ocr/tesseract
- Install to default path: `C:\Program Files\Tesseract-OCR\`

### 4. Download Models
Ensure the following model files are present:
- `yolov5s.pt` (base YOLOv5 model)
- `bsgo_ai/models/best.pt` (custom-trained asteroid detection model)

## ⚙️ Configuration

### Initial Setup
1. **Launch GUI**: Run `python bsgo_ai/gui.py`
2. **Configure Mining Parameters**:
   - Mining Duration: Total session time (minutes)
   - Sector Duration: Time per sector before rotation (minutes)
3. **Select Mining Sectors**: Choose from available game sectors
4. **Set Schedule**: Immediate start or delayed activation

### Game Configuration
1. **BSGO Settings**:
   - Run game in **windowed mode**
   - Set resolution for coordinate accuracy
   - Ensure keybindings match `config.py` settings

2. **Screen Position**: 
   - Position game window consistently
   - Verify coordinates align with predefined zones

### Key Bindings (Default)
```python
# Combat & Navigation
POST_COMBUSTION = 'space'
TURN_LEFT = 'q'
TURN_RIGHT = 'd'
MAP_KEY = 'n'
START_JUMP = 'j'
SCAN = '&'

# Mining & Targeting
ENABLE_ALL_GUNS = 'g'
CANCEL_TARGET = 'c'
ARTEMIS_KEY = '"'
```

## 🚀 Usage

### Quick Start
1. **Start BSGO** and log into your character
2. **Position ship** in a mining sector or base
3. **Run the GUI**: `python bsgo_ai/gui.py`
4. **Configure settings** and select sectors
5. **Click "Start"** to begin automated mining

### Advanced Usage
```bash
# Direct bot execution (with config file)
python bsgo_ai/status/main.py

# Random delay bot launcher
python bsgo_ai/bot.py

# GUI configuration only
python bsgo_ai/gui.py
```

### Configuration File Example
```json
{
    "mining_time": 300,
    "sector_time": 45,
    "sectors": [13, 18, 16, 12],
    "first_connection": true,
    "start_delay": {
        "mode": "now"
    }
}
```

## 📁 Project Structure

```
BSGO-Auto-Miner/
├── bsgo_ai/                    # Main bot package
│   ├── gui.py                 # Configuration interface
│   ├── bot.py                 # Bot launcher with delays
│   ├── config.py              # Game coordinates & settings
│   ├── json_loader.py         # Configuration loader
│   ├── pyautogui_lib.py       # Automation functions
│   ├── cursor.py              # Mouse control utilities
│   ├── actions/               # Input handling
│   ├── detectors/             # OCR & text recognition
│   ├── models/                # AI model files
│   ├── status/                # Game state management
│   │   ├── main.py           # Main bot logic
│   │   ├── mining.py         # Mining automation
│   │   ├── sector.py         # Navigation & pathfinding
│   │   ├── combat.py         # Combat detection
│   │   └── inbase.py         # Base operations
│   └── sectors_links/         # Sector navigation data
├── yolov5/                    # YOLOv5 framework
│   ├── models/               # Neural network models
│   ├── utils/                # Utilities & helpers
│   ├── data/                 # Training configurations
│   └── detect.py             # Detection scripts
├── yolov5s.pt                # Base YOLOv5 weights
└── screenshot_saver.py       # Debug utilities
```

## 🤖 Key Components

### AI Detection System
- **YOLOv5 Model**: Custom-trained for asteroid detection
- **Object Classes**: `asteroid`, `asteroid_no_resource`, `asteroid_titanium`, `asteroid_tylium`, `asteroid_water`, `planetoid`, `platform`
- **EasyOCR Integration**: English text recognition with GPU acceleration
- **Tesseract OCR**: Backup text extraction system

### Navigation Engine
- **NetworkX Pathfinding**: Shortest path calculation between sectors
- **Sector Database**: JSON-based sector mapping with connections
- **Jump Automation**: Automated FTL jumps with timing control
- **Position Verification**: OCR-based location confirmation

### Mining Logic
- **Target Detection**: AI-powered asteroid identification
- **Distance Calculation**: Approach optimization for mining efficiency
- **Resource Analysis**: Smart targeting based on asteroid composition
- **Combat Avoidance**: Automatic evasion when under attack

### State Management
Player status tracking:
- `PS_MINING`: Active mining operations
- `PS_INBASE`: Docked at station
- `PS_JUMP`: Traveling between sectors
- `PS_IN_COMBAT`: Engaged in combat
- `PS_KILLED`: Requiring respawn

## 🛠️ Troubleshooting

### Common Issues

**Bot not detecting asteroids:**
- Verify YOLOv5 model path: `bsgo_ai/models/best.pt`
- Check GPU availability for inference
- Ensure game graphics settings for visibility

**OCR reading errors:**
- Confirm Tesseract installation path
- Verify game window position and size
- Check coordinate alignment in `config.py`

**Navigation failures:**
- Update sector database: `sectors_links/secteurs.json`
- Verify sector connections in navigation data
- Check FTL jump timing settings

**GUI configuration issues:**
- Ensure JSON file permissions: `gui_config.json`
- Validate sector ID selections
- Check Python tkinter installation

### Performance Optimization
- **GPU Acceleration**: Enable CUDA for YOLOv5
- **Memory Management**: Monitor RAM usage during long sessions  
- **Detection Thresholds**: Adjust confidence levels in mining logic
- **Timing Adjustments**: Calibrate delays for your system performance

## ⚠️ Important Notes

### Legal & Ethical Considerations
- **Use responsibly** and in accordance with BSGO Terms of Service
- **Educational purposes**: This project demonstrates AI automation techniques
- **No warranty provided** - use at your own risk

### Game Compatibility
- Designed for specific BSGO game version and UI layout
- Coordinate system may require adjustment for different resolutions
- Keybinding configuration must match your game settings

### Security Notes
- **Screen capture required** for AI detection functionality
- **Input automation active** - avoid manual input during operation
- **Process monitoring** recommended during initial setup
  

## 📄 License

This project is provided for educational and research purposes. Please ensure compliance with all applicable terms of service and local regulations.

---
