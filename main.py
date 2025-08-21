import os
from fastapi import FastAPI, Request
from pydantic import BaseModel
from openai import OpenAI
from dotenv import load_dotenv
from ollama_client import OllamaClient
from gemini_client import GeminiClient

# Load environment variables
load_dotenv()

# Setup AI Clients with new priority order (fastest first)
# 1. Gemini Pro (free tier, fast, cloud-based)
gemini_client = GeminiClient()

# 2. OpenAI (fast, reliable, paid)
try:
    openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY")) if os.getenv("OPENAI_API_KEY") else None
except Exception as e:
    print(f"⚠️  OpenAI initialization error: {e}")
    openai_client = None

# 3. Ollama (local, slower but private)
ollama_client = OllamaClient()

# Track selected provider (default to auto priority)
selected_provider = None  # None means use priority order, or specific provider name

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "AI Assistant Backend is running!", "status": "active"}

class ChatRequest(BaseModel):
    message: str
    context: dict = {}

class TaskRequest(BaseModel):
    task: str
    parameters: dict = {}

@app.post("/chat")
async def chat_endpoint(req: ChatRequest):
    """Chat endpoint with multi-provider AI support"""
    
    # Build context string
    context_str = ""
    if req.context:
        for key, value in req.context.items():
            context_str += f"{key}: {value}\n"
    
    # Build messages for AI
    messages = [
        {"role": "system", "content": "You are a helpful AI assistant that can understand and respond to queries while maintaining context."}
    ]
    
    if context_str:
        messages.append({"role": "system", "content": f"Context: {context_str}"})
    
    messages.append({"role": "user", "content": req.message})
    
    # Debug: Print current selected provider
    print(f"🔍 Current selected_provider: {selected_provider}")
    
    # Check if specific provider is selected
    if selected_provider == "gemini":
        print("🎯 Using Gemini as primary provider")
        # Try Gemini first when selected
        if gemini_client.is_configured:
            try:
                answer = gemini_client.chat_completion(messages)
                if answer and "Gemini error" not in answer and "not configured" not in answer:
                    new_context = req.context
                    new_context['last_message'] = req.message
                    new_context['last_answer'] = answer
                    return {"answer": answer, "provider": "Google Gemini Pro", "context": new_context}
            except Exception as e:
                print(f"Gemini error: {e}")
    
    elif selected_provider == "ollama":
        print("🎯 Using Ollama as primary provider")
        # Try Ollama first when selected
        if ollama_client.check_connection():
            try:
                answer = ollama_client.chat_completion(messages)
                if answer and "Error:" not in answer:
                    new_context = req.context
                    new_context['last_message'] = req.message
                    new_context['last_answer'] = answer
                    return {"answer": answer, "provider": f"Ollama ({ollama_client.current_model})", "context": new_context}
            except Exception as e:
                print(f"Ollama error: {e}")
    
    print("🔄 Using default priority order")
    # Default priority order: Gemini → OpenAI → Ollama → Fallback
    # Priority 1: Try Gemini Pro first (free, fast, cloud-based)
    if gemini_client.is_configured:
        try:
            answer = gemini_client.chat_completion(messages)
            if answer and "Gemini error" not in answer and "not configured" not in answer:
                # Update context
                new_context = req.context
                new_context['last_message'] = req.message
                new_context['last_answer'] = answer
                
                return {
                    "answer": answer,
                    "provider": "Google Gemini Pro", 
                    "context": new_context
                }
        except Exception as e:
            print(f"Gemini error: {e}")
    
    # Priority 2: Try OpenAI (fast, reliable, paid)
    if openai_client:
        try:
            response = openai_client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=messages,
                max_tokens=500,
                timeout=10
            )
            
            answer = response.choices[0].message.content
            
            # Update context
            new_context = req.context
            new_context['last_message'] = req.message
            new_context['last_answer'] = answer
            
            return {
                "answer": answer,
                "provider": "OpenAI GPT-3.5",
                "context": new_context
            }
        except Exception as e:
            print(f"OpenAI error: {e}")
    
    # Priority 3: Try Ollama (local, slower but private)
    if ollama_client.current_model:
        try:
            # Check for quick code generation first
            quick_response = ollama_client.quick_code_response(req.message)
            if quick_response:
                new_context = req.context
                new_context['last_message'] = req.message
                new_context['last_answer'] = quick_response
                
                return {
                    "answer": quick_response,
                    "provider": f"Ollama ({ollama_client.current_model}) - Quick Code",
                    "context": new_context
                }
            
            # Regular Ollama chat
            answer = ollama_client.chat_completion(messages)
            if answer and "Error:" not in answer:
                # Update context
                new_context = req.context
                new_context['last_message'] = req.message
                new_context['last_answer'] = answer
                
                return {
                    "answer": answer,
                    "provider": f"Ollama ({ollama_client.current_model})",
                    "context": new_context
                }
        except Exception as e:
            print(f"Ollama error: {e}")
            
    # Fallback: Simple rule-based responses
    fallback_responses = {
        "hello": "Hello! I'm an AI assistant ready to help you.",
        "hi": "Hi there! How can I assist you today?",
        "how are you": "I'm doing well, thank you for asking! How can I help you?",
        "what is your name": "I'm your AI Assistant, powered by multiple AI providers including Gemini Pro, OpenAI, and Ollama.",
        "help": "I can help you with various tasks like answering questions, writing code, creative writing, math problems, and general conversation. What would you like assistance with?",
        "bye": "Goodbye! Feel free to chat with me anytime.",
        "thank you": "You're welcome! Is there anything else I can help you with?",
        "weather": "I don't have access to real-time weather data, but I'd be happy to help you with other questions!"
    }
    
    # Check for simple keyword matches
    message_lower = req.message.lower().strip()
    for keyword, response in fallback_responses.items():
        if keyword in message_lower:
            new_context = req.context
            new_context['last_message'] = req.message
            new_context['last_answer'] = response
            
            return {
                "answer": response,
                "provider": "Rule-based Fallback",
                "context": new_context
            }
    
    # Final fallback
    return {
        "answer": "I'm sorry, all AI providers are currently unavailable. Please try again later or check your connection.",
        "provider": "Error Fallback",
        "context": req.context
    }
    messages = [
        {"role": "system", "content": "You are a helpful AI assistant that can understand and respond to queries while maintaining context."}
    ]
    
    if context_str:
        messages.append({"role": "system", "content": f"Context: {context_str}"})
    
    messages.append({"role": "user", "content": req.message})
    
    # Use selected provider if specified, otherwise use priority order
    if selected_provider == "gemini":
        return await try_gemini_first(messages, req)
    elif selected_provider == "ollama":
        return await try_ollama_first(messages, req)  
    elif selected_provider == "openai":
        return await try_openai_first(messages, req)
    else:
        # Default priority order: Gemini → OpenAI → Ollama → Fallback
        return await try_priority_order(messages, req)

async def try_gemini_first(messages, req):
    """Try Gemini first, fallback to others if needed"""
    # Try Gemini Pro first
    if gemini_client.is_configured:
        try:
            answer = gemini_client.chat_completion(messages)
            if answer and "Gemini error" not in answer and "not configured" not in answer:
                new_context = req.context
                new_context['last_message'] = req.message
                new_context['last_answer'] = answer
                return {"answer": answer, "provider": "Google Gemini Pro", "context": new_context}
        except Exception as e:
            print(f"Gemini error: {e}")
    
    # Fallback to others
    return await try_other_providers(messages, req, exclude="gemini")

async def try_ollama_first(messages, req):
    """Try Ollama first, fallback to others if needed"""
    # Try Ollama first
    if ollama_client.check_connection():
        try:
            answer = ollama_client.chat_completion(messages)
            if answer and "Error:" not in answer:
                new_context = req.context
                new_context['last_message'] = req.message
                new_context['last_answer'] = answer
                return {"answer": answer, "provider": f"Ollama ({ollama_client.current_model})", "context": new_context}
        except Exception as e:
            print(f"Ollama error: {e}")
    
    # Fallback to others
    return await try_other_providers(messages, req, exclude="ollama")

async def try_openai_first(messages, req):
    """Try OpenAI first, fallback to others if needed"""
    # Try OpenAI first
    if openai_client:
        try:
            response = openai_client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=messages,
                max_tokens=500,
                timeout=10
            )
            answer = response.choices[0].message.content
            new_context = req.context
            new_context['last_message'] = req.message
            new_context['last_answer'] = answer
            return {"answer": answer, "provider": "OpenAI GPT-3.5", "context": new_context}
        except Exception as e:
            print(f"OpenAI error: {e}")
    
    # Fallback to others
    return await try_other_providers(messages, req, exclude="openai")

async def try_other_providers(messages, req, exclude=None):
    """Try remaining providers as fallback"""
    # Try Gemini if not excluded
    if exclude != "gemini" and gemini_client.is_configured:
        try:
            answer = gemini_client.chat_completion(messages)
            if answer and "Gemini error" not in answer:
                new_context = req.context
                new_context['last_message'] = req.message
                new_context['last_answer'] = answer
                return {"answer": answer, "provider": "Google Gemini Pro (fallback)", "context": new_context}
        except Exception as e:
            print(f"Gemini fallback error: {e}")
    
    # Try Ollama if not excluded
    if exclude != "ollama" and ollama_client.check_connection():
        try:
            answer = ollama_client.chat_completion(messages)
            if answer and "Error:" not in answer:
                new_context = req.context
                new_context['last_message'] = req.message
                new_context['last_answer'] = answer
                return {"answer": answer, "provider": f"Ollama ({ollama_client.current_model}) (fallback)", "context": new_context}
        except Exception as e:
            print(f"Ollama fallback error: {e}")
    
    # Try OpenAI if not excluded
    if exclude != "openai" and openai_client:
        try:
            response = openai_client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=messages,
                max_tokens=500,
                timeout=10
            )
            answer = response.choices[0].message.content
            new_context = req.context
            new_context['last_message'] = req.message
            new_context['last_answer'] = answer
            return {"answer": answer, "provider": "OpenAI GPT-3.5 (fallback)", "context": new_context}
        except Exception as e:
            print(f"OpenAI fallback error: {e}")
    
    # Final fallback
    return await try_priority_order(messages, req)

async def try_priority_order(messages, req):
    # Use context to maintain conversation history
    context_str = "\n".join([f"{k}: {v}" for k, v in req.context.items()])
    
    # Build messages for AI
    messages = [
        {"role": "system", "content": "You are a helpful AI assistant that can understand and respond to queries while maintaining context."}
    ]
    
    if context_str:
        messages.append({"role": "system", "content": f"Context: {context_str}"})
    
    messages.append({"role": "user", "content": req.message})
    
    # Priority 1: Try Gemini Pro first (free, fast, cloud-based)
    if gemini_client.is_configured:
        try:
            answer = gemini_client.chat_completion(messages)
            if answer and "Gemini error" not in answer and "not configured" not in answer:
                # Update context
                new_context = req.context
                new_context['last_message'] = req.message
                new_context['last_answer'] = answer
                
                return {
                    "answer": answer, 
                    "context": new_context,
                    "provider": "Google Gemini Pro"
                }
        except Exception as e:
            print(f"Gemini error: {str(e)}")
    
    # Priority 2: Try OpenAI (fast, reliable, paid)
    if openai_client:
        try:
            response = openai_client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=messages
            )
            answer = response.choices[0].message.content
            
            # Update context
            new_context = req.context
            new_context['last_message'] = req.message
            new_context['last_answer'] = answer
            
            return {
                "answer": answer, 
                "context": new_context,
                "provider": "OpenAI (GPT-3.5-turbo)"
            }
        except Exception as e:
            print(f"OpenAI error: {str(e)}")

    # Priority 3: Try Ollama (local, slower but private)
    if ollama_client.current_model:
        try:
            # Check for quick code generation first
            quick_response = ollama_client.quick_code_response(req.message)
            if quick_response:
                new_context = req.context
                new_context['last_message'] = req.message
                new_context['last_answer'] = quick_response
                
                return {
                    "answer": quick_response, 
                    "context": new_context,
                    "provider": f"Ollama Quick Response ({ollama_client.current_model})"
                }
            
            # If no quick response, use full AI generation with shorter timeout
            answer = ollama_client.chat_completion(messages)
            if answer and "Error" not in answer and "timed out" not in answer.lower():
                # Update context
                new_context = req.context
                new_context['last_message'] = req.message
                new_context['last_answer'] = answer
                
                return {
                    "answer": answer, 
                    "context": new_context,
                    "provider": f"Ollama ({ollama_client.current_model})"
                }
        except Exception as e:
            print(f"Ollama error: {str(e)}")
        
    # Final fallback: Rule-based responses when all AI services are unavailable
    fallback_responses = {
        "hello": "Hello! How can I help you today?",
        "hi": "Hi there! What can I do for you?",
        "how are you": "I'm doing great! How about you?",
        "what is your name": "I'm your AI assistant. How can I assist you?",
        "thank you": "You're welcome! Is there anything else I can help with?",
        "diagram": "Here's a simple text diagram:\n\n```\n┌─────────────┐\n│   System    │\n│  Overview   │\n└─────────────┘\n      |\n      v\n┌─────────────┐\n│   Process   │\n│    Flow     │\n└─────────────┘\n```",
        "chart": "Text-based chart example:\n\nData Flow:\nInput → Process → Output\n  |       |        |\n  v       v        v\nUser → System → Result",
    }
    
    # Simple keyword matching for fallback
    message_lower = req.message.lower()
    answer = "I'm sorry, all AI services are currently unavailable. Please try again later."
    
    # Check for diagram/chart requests
    if "diagram" in message_lower or "chart" in message_lower or "|" in req.message:
        if "diagram" in message_lower:
            answer = fallback_responses["diagram"]
        elif "chart" in message_lower:
            answer = fallback_responses["chart"]
        else:
            # Simple ASCII art for pipe symbol requests
            answer = """Here's a simple diagram using | symbols:

```
    Input Data
        |
        v
   ┌─────────┐
   │ Process │
   └─────────┘
        |
        v
   Output Result
        |
        v
    ┌─────────┐
    │ Display │
    └─────────┘
```"""
    else:
        # Other fallback responses
        for key, response in fallback_responses.items():
            if key in message_lower:
                answer = response
                break
    
    # Update context
    new_context = req.context
    new_context['last_message'] = req.message
    new_context['last_answer'] = answer
    
    return {
        "answer": answer, 
        "context": new_context, 
        "provider": "Rule-based Fallback"
    }

@app.post("/task")
async def task_endpoint(req: TaskRequest):
    # Handle specific tasks (can be extended based on requirements)
    tasks = {
        "weather": lambda params: "Weather functionality to be implemented",
        "play_music": lambda params: "Music playback functionality to be implemented",
        "set_reminder": lambda params: "Reminder functionality to be implemented"
    }
    
    if req.task in tasks:
        return {"result": tasks[req.task](req.parameters)}
    return {"error": "Task not supported"}

@app.get("/models")
async def get_models():
    """Get available AI models from all providers"""
    models = {
        "providers": {
            "gemini": {
                "available": ["gemini-pro"],
                "status": "configured" if gemini_client.is_configured else "not configured",
                "priority": 1,
                "description": "Google Gemini Pro (free tier, fast, cloud-based)"
            },
            "openai": {
                "available": ["gpt-3.5-turbo", "gpt-4"],
                "status": "configured" if openai_client else "not configured",
                "priority": 2,
                "description": "OpenAI GPT models (fast, reliable, paid)"
            },
            "ollama": {
                "available": ollama_client.available_models,
                "current": ollama_client.current_model,
                "status": "connected" if ollama_client.current_model else "disconnected",
                "priority": 3,
                "description": "Local AI models (private, slower)"
            }
        },
        "priority_order": "Gemini → OpenAI → Ollama → Rule-based fallback"
    }
    return models

@app.post("/switch_model")
async def switch_model(model_data: dict):
    """Switch AI model and provider"""
    global selected_provider
    
    model_name = model_data.get("model")
    if not model_name:
        return {"error": "Model name required"}
    
    print(f"🔧 Switch model request: '{model_name}'")
    
    # Parse provider and model from format "Provider: model"
    if ":" in model_name:
        provider, actual_model = model_name.split(":", 1)
        provider = provider.strip().lower()
        actual_model = actual_model.strip()
        
        print(f"🔧 Parsed - Provider: '{provider}', Model: '{actual_model}'")
        
        if provider == "gemini":
            selected_provider = "gemini"
            print(f"🔧 Set selected_provider to: {selected_provider}")
            return {"message": f"Switched to Gemini Pro", "current_model": actual_model, "provider": "gemini"}
        
        elif provider == "ollama":
            selected_provider = "ollama"
            print(f"🔧 Set selected_provider to: {selected_provider}")
            if ollama_client.switch_model(actual_model):
                return {"message": f"Switched to Ollama: {actual_model}", "current_model": actual_model, "provider": "ollama"}
            else:
                return {"error": f"Could not switch to Ollama: {actual_model}"}
        
        elif provider == "openai":
            selected_provider = "openai"
            return {"message": f"Switched to OpenAI: {actual_model}", "current_model": actual_model, "provider": "openai"}
    
    # Legacy format - assume Ollama
    if ollama_client.switch_model(model_name):
        selected_provider = "ollama"
        return {"message": f"Switched to Ollama: {model_name}", "current_model": model_name, "provider": "ollama"}
    else:
        return {"error": f"Could not switch to {model_name}"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
