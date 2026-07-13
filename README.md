# JARVIS Pro - Advanced AI Assistant

## Overview

JARVIS Pro is a production-ready AI assistant built with Python 3.12, featuring:

- **Multi-Model AI**: Gemini (primary) + OpenAI (backup) with automatic fallback
- **Modern GUI**: Dark-themed interface with chat history and real-time responses
- **PC Control**: 
  - Application management (open, close, list running apps)
  - System control (shutdown, restart, sleep, lock)
  - System monitoring (CPU, memory, disk, network)
  - Volume control (mute, unmute, set level)
  - File and folder operations
- **Voice Assistant**: Speech recognition and text-to-speech
- **Smart Search**: Web search integration with SerpAPI
- **Multi-Mode**: GUI, CLI, and Voice modes
- **Command Recognition**: Natural language command parsing

## Quick Start

### 1. Clone Repository
```bash
git clone https://github.com/hadigujjar12125/Jarvis-.git
cd Jarvis-
```

### 2. Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure API Keys
```bash
cp .env.example .env
# Edit .env with your API keys
```

### 5. Run JARVIS Pro
```bash
python main.py              # GUI mode (default)
python main.py --cli        # CLI mode
python main.py --voice      # Voice mode
python main.py --debug      # Debug mode
```

## Configuration

### Environment Variables

Create a `.env` file based on `.env.example`:

```env
# API Keys
GEMINI_API_KEY=your_key_here
OPENAI_API_KEY=your_key_here
SEARCH_API_KEY=your_key_here

# Voice Settings
WAKE_WORD=jarvis
VOICE_NAME=en-US-GuyNeural
MIC_DEVICE_INDEX=0

# Application Settings
ASSISTANT_NAME=Jarvis
USER_NAME=User
DEBUG_MODE=0

# Search Settings
AUTO_WEB_SEARCH_ENABLE=1
```

## Features

### AI System
- Google Gemini (primary, free tier available)
- OpenAI GPT-3.5 (backup)
- Automatic provider switching on failure
- Context-aware responses with conversation history

### PC Control Commands

#### System Control
```
shutdown / power off     - Shut down the computer
restart / reboot         - Restart the computer
sleep / sleep mode       - Put computer to sleep
lock / lock computer     - Lock the computer
```

#### System Information
```
system info              - Get system information
cpu usage / cpu load     - Get CPU usage percentage
memory usage / ram usage - Get memory usage
disk usage / storage     - Get disk usage
network status           - Get network status
```

#### Application Control
```
open [app name]          - Open an application
close [app name]         - Close an application
list apps / running apps - List running applications
```

#### Volume Control
```
mute / silence           - Mute system audio
unmute / sound on        - Unmute system audio
volume [0-100]           - Set volume to specific level
```

#### File Operations
```
open file [path]         - Open a file
open folder [path]       - Open a folder
```

### GUI Features
- Clean dark-themed interface
- Real-time chat display with timestamps
- Message history with color-coded user/assistant text
- Status bar showing application state
- Responsive input field with Enter to send
- Clear history button
- Multi-threaded processing for non-blocking UI

### Voice Features
- Speech recognition via Google Speech Recognition
- Text-to-speech via Edge TTS
- Natural voice output with audio playback
- Automatic microphone selection

### Search Integration
- Automatic web search for informational queries
- Search intent detection based on question patterns
- Result summarization in AI responses
- Configurable auto-search toggle

## Project Structure

```
jarvis/
├── core/
│   ├── __init__.py
│   └── command_handler.py    # Command parsing and handling
├── gui/
│   ├── __init__.py
│   └── gui.py                # Modern GUI interface
├── automation/
│   ├── __init__.py
│   └── pc_control.py         # PC control system
├── main.py                   # Entry point
├── ai.py                     # AI agent with multi-model support
├── config.py                 # Configuration management
├── search.py                 # Web search engine
├── voice.py                  # Voice input/output
├── requirements.txt          # Python dependencies
├── .env.example              # Configuration template
└── README.md                 # This file
```

## Usage Examples

### GUI Mode
```bash
python main.py
```
- Open JARVIS Pro in modern GUI window
- Type messages in input field
- Press Enter or click Send to submit
- View responses in chat history

### CLI Mode
```bash
python main.py --cli
```
Examples:
```
You: open chrome
JARVIS: Opened chrome

You: cpu usage
JARVIS: CPU usage: 25.3%

You: what is machine learning?
JARVIS: Machine learning is a subset of artificial intelligence...

You: mute
JARVIS: System muted

You: exit
JARVIS: Goodbye!
```

### Voice Mode
```bash
python main.py --voice
```
- System listens for voice input
- Processes spoken commands
- Responds with audio output

### Debug Mode
```bash
python main.py --debug
```
- Enables detailed logging
- Shows all internal operations

## API Setup

### Google Gemini
1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Create API key
3. Add to `.env`: `GEMINI_API_KEY=your_key`

### OpenAI
1. Go to [OpenAI Platform](https://platform.openai.com/api-keys)
2. Create API key
3. Add to `.env`: `OPENAI_API_KEY=your_key`

### SerpAPI (Search)
1. Go to [SerpAPI](https://serpapi.com)
2. Create account and get API key
3. Add to `.env`: `SEARCH_API_KEY=your_key`

## Troubleshooting

### GUI not starting
```bash
python main.py --cli
```
Try CLI mode first to isolate GUI issues.

### No microphone detected
```bash
python -c "import speech_recognition as sr; print(sr.Microphone.list_microphone_names())"
```
Update `MIC_DEVICE_INDEX` in `.env` with correct index.

### AI model not responding
1. Check API keys in `.env`
2. Verify internet connection
3. Check logs for detailed error messages

### PC control commands not working
- Ensure admin/sudo privileges for system commands
- Check if process names are correct (use `list apps`)
- Verify OS compatibility (Windows, macOS, Linux)

## Performance Tips

- Use CLI mode for faster startup
- Keep conversation history lean (40+ messages may slow down)
- Enable auto-search only when needed
- Use voice mode for hands-free operation

## Security Considerations

- Never commit `.env` files with real API keys
- Use environment variables for sensitive data
- Keep dependencies updated: `pip install --upgrade -r requirements.txt`
- Be cautious with PC control commands (shutdown, file operations)

## System Requirements

- Python 3.8+
- 512 MB RAM minimum (1GB recommended)
- Internet connection (for AI and search)
- Audio device (for voice features)
- Administrative privileges (for PC control)

## Supported OS

- Windows 7+
- macOS 10.12+
- Linux (Ubuntu 18.04+, Fedora 30+, etc.)

## Contributing

1. Fork the repository
2. Create feature branch: `git checkout -b feature/amazing-feature`
3. Commit changes: `git commit -m 'Add amazing feature'`
4. Push to branch: `git push origin feature/amazing-feature`
5. Open Pull Request

## License

MIT License - See LICENSE file for details

## Changelog

### Version 2.1.0
- Added modern GUI interface
- Implemented PC control system
- Added command recognition and parsing
- Improved error handling and logging
- Enhanced documentation

### Version 2.0.0
- Complete rewrite with type hints
- Multi-model AI support
- Web search integration
- Voice I/O capabilities
- Production-ready code

## Roadmap

### 2.2.0
- Clipboard operations
- Screenshot capture
- System notifications
- Custom voice wake words

### 2.3.0
- Plugin system
- Advanced voice commands
- Email integration
- Calendar management

## Credits

Created with ❤️ by the JARVIS Team

Thanks to:
- Google Gemini API
- OpenAI
- Python community
- Edge TTS
- SerpAPI

---

**JARVIS Pro 2.1.0** - Your Intelligent Digital Assistant

✅ GUI Interface | ✅ PC Control | ✅ AI Powered | ✅ Multi-Modal
