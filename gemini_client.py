#!/usr/bin/env python
"""
Google Gemini Pro Integration for AI Assistant
"""
import google.generativeai as genai
import os
from typing import Optional, Dict, Any

class GeminiClient:
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        self.model = None
        self.is_configured = False
        self.setup_client()
        
    def setup_client(self) -> bool:
        """Setup Gemini client"""
        if not self.api_key:
            print("❌ Gemini API key not found")
            return False
            
        try:
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel('gemini-1.5-flash')
            self.is_configured = True
            print("✅ Connected to Google Gemini Pro")
            return True
        except Exception as e:
            print(f"❌ Failed to setup Gemini: {str(e)}")
            return False
    
    def generate_response(self, prompt: str, temperature: float = 0.7) -> str:
        """Generate response using Gemini Pro"""
        if not self.is_configured:
            return "Gemini not configured"
            
        try:
            # Configure generation parameters
            generation_config = genai.types.GenerationConfig(
                temperature=temperature,
                max_output_tokens=1000,
            )
            
            response = self.model.generate_content(
                prompt,
                generation_config=generation_config
            )
            
            return response.text
            
        except Exception as e:
            return f"Gemini error: {str(e)}"
    
    def chat_completion(self, messages: list) -> str:
        """Chat completion similar to OpenAI format"""
        if not self.is_configured:
            return "Gemini not configured"
            
        # Convert messages to a single prompt
        prompt = ""
        for msg in messages:
            role = msg.get('role', 'user')
            content = msg.get('content', '')
            if role == 'system':
                prompt += f"Instructions: {content}\n\n"
            elif role == 'user':
                prompt += f"Human: {content}\n"
            elif role == 'assistant':
                prompt += f"Assistant: {content}\n"
        
        prompt += "Assistant: "
        
        return self.generate_response(prompt)

# Test the Gemini client
if __name__ == "__main__":
    print("Testing Google Gemini Pro integration...")
    client = GeminiClient()
    
    if client.is_configured:
        response = client.generate_response("Hello! How are you today?")
        print(f"Gemini Response: {response}")
    else:
        print("Gemini not configured. Add GEMINI_API_KEY to your .env file")
