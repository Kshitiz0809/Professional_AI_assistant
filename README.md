# 🤖 Professional AI Assistant

A modern, multi-provider AI assistant with voice capabilities, built with Python and FastAPI. Features support for Google Gemini Pro, OpenAI GPT, and local Ollama models with automatic fallback and intelligent provider switching.

![Professional AI Assistant](https://img.shields.io/badge/Python-3.8+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)
![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey.svg)

## ✨ Features

### 🧠 **Multi-Provider AI Support**
- **Google Gemini Pro** - Free, fast, cloud-based AI
- **OpenAI GPT-3.5/4** - Premium AI models
- **Local Ollama Models** - Private, offline AI (Mistral, LLaMA, etc.)
- **Intelligent Fallback** - Automatically switches providers if one fails
- **Priority-based Routing** - Optimizes for speed and reliability

### 🎨 **Modern Professional UI**
- Clean, responsive interface built with Tkinter
- Color-coded conversation display
- Real-time status indicators
- Voice input/output capabilities
- Model switching with live preview

### 🔊 **Voice Features**
- Speech-to-text input using microphone
- Text-to-speech output for responses
- Background processing for smooth UX

### 🚀 **Production Ready**
- FastAPI backend with async support
- RESTful API endpoints
- Error handling and logging
- Context-aware conversations
- Scalable architecture

## 🛠️ Installation

### Prerequisites
- **Python 3.8+** installed on your system
- **Microphone** (optional, for voice features)
- **Internet connection** (for cloud AI providers)

### Quick Start

1. **Clone the repository**
```bash
git clone https://github.com/Kshitiz0809/professional-ai-assistant.git
cd professional-ai-assistant
```

2. **Create virtual environment**
```bash
python -m venv .venv

# On Windows
.venv\Scripts\activate

# On macOS/Linux
source .venv/bin/activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt

# If PyAudio installation fails (voice features), use minimal requirements:
pip install -r requirements-minimal.txt
```
**Note:** If PyAudio installation fails (required for microphone input), use `requirements-minimal.txt` instead. Voice features will be disabled but the app will still work perfectly for text-based interactions.

4. **Configure API Keys**
Create a `.env` file in the project root:
```env
# Google Gemini Pro API Key (Free tier available)
GEMINI_API_KEY=your_gemini_api_key_here

# OpenAI API Key (Optional - Paid service) 
OPENAI_API_KEY=your_openai_api_key_here
```

5. **Install Ollama (Optional - for local AI)**
```bash
# Visit https://ollama.ai and install Ollama
# Then pull some models:
ollama pull mistral
ollama pull llama2
```

6. **Run the application**
```bash
# Option 1: Use the convenient start scripts
# Windows: Double-click start.bat or run ./start.bat
# Unix/Linux/macOS: ./start.sh

# Option 2: Manual start
# Terminal 1: Start the backend server
python main.py

# Terminal 2: Start the GUI
python modern_gui.py
```

## ⚙️ Getting API Keys

### 🔑 **Google Gemini Pro (Recommended - Free)**
1. Visit [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy the key to your `.env` file

### 🔑 **OpenAI GPT (Optional - Paid)**
1. Visit [OpenAI Platform](https://platform.openai.com/api-keys)
2. Create an account and add billing information
3. Generate a new API key
4. Copy the key to your `.env` file

### 🔑 **Ollama (Optional - Local/Free)**
1. Install [Ollama](https://ollama.ai/) 
2. Pull models: `ollama pull mistral`
3. Models run locally, no API key needed

## 🚀 Usage

### Starting the Application

**Method 1: Manual (Recommended)**
```bash
# Terminal 1: Start the backend server
python main.py

# Terminal 2: Start the GUI
python modern_gui.py
```

### Using the Interface

1. **Select AI Model**: Choose from dropdown (Gemini, OpenAI, or Ollama)
2. **Type Message**: Enter your question in the input field
3. **Voice Input**: Click 🎤 Voice Input button to speak
4. **Send**: Press Enter or click Send button
5. **Switch Models**: Change AI providers anytime using the dropdown

### API Endpoints

The FastAPI server provides REST endpoints:

- `GET /` - Health check
- `GET /models` - List available AI providers and models  
- `POST /chat` - Send message and get AI response
- `POST /switch_model` - Switch active AI model

Example API usage:
```bash
curl -X POST "http://localhost:8001/chat" \
     -H "Content-Type: application/json" \
     -d '{"message": "Hello, how are you?", "context": {}}'
```

## 🏗️ Architecture

```
📁 professional-ai-assistant/
├── 📄 main.py              # FastAPI backend server
├── 📄 modern_gui.py        # Modern Tkinter GUI interface  
├── 📄 gemini_client.py     # Google Gemini Pro integration
├── 📄 ollama_client.py     # Local Ollama models integration
├── 📄 voice_assistant.py   # Speech recognition and TTS
├── 📄 requirements.txt     # Python dependencies
├── 📄 start.bat/.sh        # Easy startup scripts
├── 📄 .env                 # Configuration (API keys)
└── 📄 README.md           # Documentation
```

## 🧪 Testing Your Installation

After installation, you can verify everything works by:

1. **Test Backend**: Run `python main.py` - should show connection messages
2. **Test GUI**: Run `python modern_gui.py` - should launch the interface
3. **Quick Test**: Use the start scripts (`./start.bat` or `./start.sh`)

See `TESTING.md` for detailed testing procedures.

## 🐛 Troubleshooting

### Common Issues

#### "ModuleNotFoundError" 
- **Solution**: Ensure virtual environment is activated
```bash
# Windows
.venv\Scripts\activate

# macOS/Linux  
source .venv/bin/activate

# Then install dependencies
pip install -r requirements.txt
```

#### PyAudio installation fails
- **Solution**: Voice features will be disabled, but app still works
- **Windows**: Try `pip install pipwin && pipwin install pyaudio`
- **macOS**: Try `brew install portaudio && pip install pyaudio`
- **Linux**: Try `sudo apt-get install portaudio19-dev && pip install pyaudio`

#### "Connection refused" error
- Ensure the server is running: `python main.py`
- Check if port 8001 is available
- Verify firewall settings

#### "API key not valid" error  
- Check your `.env` file has correct API keys
- Ensure no extra spaces or quotes in the keys
- Verify the API key is active in the provider's dashboard

#### Ollama models not loading
- Ensure Ollama is installed and running
- Pull models: `ollama pull mistral`  
- Check Ollama service status: `ollama list`

### Getting Help

1. Check the [Issues](https://github.com/yourusername/professional-ai-assistant/issues) page
2. Create a new issue with:
   - Your operating system
   - Python version
   - Error message/logs
   - Steps to reproduce

## 💡 Use Cases

- **Personal Assistant** - Daily questions and tasks
- **Learning Tool** - Educational support and explanations  
- **Code Helper** - Programming assistance and debugging
- **Creative Writing** - Story ideas and content generation
- **Research Assistant** - Information gathering and analysis
- **Language Practice** - Conversation and translation
- **Business Support** - Email drafting, meeting summaries

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Google** for Gemini Pro API
- **OpenAI** for GPT models
- **Ollama** for local AI model support
- **FastAPI** for the excellent web framework
- **Python community** for amazing libraries

---

**Made with ❤️ for the AI Community**

*Star ⭐ this repository if you find it helpful!*
