# 🧪 AI Assistant Testing Guide

## Quick Test Checklist

### ✅ Prerequisites Check
- [ ] Python 3.8+ installed
- [ ] Virtual environment created (.venv folder exists)
- [ ] Dependencies installed (requirements.txt)
- [ ] .env file exists with API keys

### ✅ Backend Server Test
- [ ] Server starts without errors
- [ ] Shows "✅ Connected to Google Gemini Pro"
- [ ] Shows available Ollama models (if installed)
- [ ] Displays "Uvicorn running on http://0.0.0.0:8001"

### ✅ GUI Application Test  
- [ ] GUI launches successfully
- [ ] Shows "🔄 Loaded X models" message
- [ ] Interface displays with modern styling
- [ ] Model dropdown shows available options
- [ ] Close button works properly

### ✅ Feature Testing
- [ ] **Text Chat**: Type message and get AI response
- [ ] **Model Switching**: Change between Gemini/Ollama models
- [ ] **Voice Input**: Click microphone button (optional)
- [ ] **Voice Output**: AI speaks responses (optional)
- [ ] **Status Updates**: Real-time connection status

### ✅ API Testing (Optional)
```bash
# Test health check
curl -X GET "http://localhost:8001/"

# Test models endpoint  
curl -X GET "http://localhost:8001/models"

# Test chat endpoint
curl -X POST "http://localhost:8001/chat" \
     -H "Content-Type: application/json" \
     -d '{"message": "Hello", "context": {}}'
```

## 🐛 Common Issues & Solutions

### Issue: "ModuleNotFoundError"
**Solution:** Activate virtual environment first
```bash
cd /d/Project/modern_ai_assistant
source .venv/Scripts/activate  # or .venv/Scripts/activate.bat on Windows
pip install -r requirements.txt
```

### Issue: "Connection refused" 
**Solution:** Ensure backend server is running first
```bash
# Terminal 1: Start backend
python main.py

# Terminal 2: Start GUI  
python modern_gui.py
```

### Issue: "No models available"
**Solution:** Check API keys in .env file
```env
GEMINI_API_KEY=your_key_here
OPENAI_API_KEY=your_key_here  # optional
```

### Issue: Ollama not working
**Solution:** Install Ollama and pull models
```bash
# Install Ollama from https://ollama.ai
ollama pull mistral
ollama pull llama2
```

## 🎯 Expected Behavior

### **Successful Startup Messages**
```
✅ Connected to Google Gemini Pro
✅ Connected to Ollama. Available models: ['mistral:latest']
🤖 Using model: mistral:latest
INFO: Uvicorn running on http://0.0.0.0:8001
🔄 Loaded 2 models: ['Gemini: gemini-pro', 'Ollama: mistral:latest']
```

### **GUI Features Working**
- Modern professional interface
- Model selection dropdown
- Text input/output areas
- Voice input button (if microphone available)
- Real-time status updates
- Close button with confirmation

## ✅ Success Criteria
Your AI Assistant is working correctly if:
1. Backend starts without critical errors
2. GUI launches and connects to backend
3. You can send messages and receive AI responses
4. Model switching works between available providers
5. Application closes cleanly when requested

---
*🎉 If all tests pass, your Professional AI Assistant is ready for use!*
