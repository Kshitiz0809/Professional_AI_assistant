#!/usr/bin/env python
"""
Ollama Integration for AI Assistant
"""
import requests
import json
from typing import Optional, Dict, Any

class OllamaClient:
    def __init__(self, base_url: str = "http://localhost:11434"):
        self.base_url = base_url
        self.available_models = []
        self.current_model = None
        self.check_connection()
        
    def check_connection(self) -> bool:
        """Check if Ollama service is running"""
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=5)
            if response.status_code == 200:
                models_data = response.json()
                self.available_models = [model['name'] for model in models_data.get('models', [])]
                print(f"✅ Connected to Ollama. Available models: {self.available_models}")
                
                # Set default model
                if 'mistral:latest' in self.available_models:
                    self.current_model = 'mistral:latest'
                elif 'gpt-oss:20b' in self.available_models:
                    self.current_model = 'gpt-oss:20b'
                elif self.available_models:
                    self.current_model = self.available_models[0]
                    
                print(f"🤖 Using model: {self.current_model}")
                return True
            return False
        except Exception as e:
            print(f"❌ Cannot connect to Ollama: {str(e)}")
            return False
    
    def generate_response(self, prompt: str, model: Optional[str] = None, timeout: int = 10) -> str:
        """Generate response using Ollama with shorter timeout"""
        model = model or self.current_model
        if not model:
            return "No model available"
            
        try:
            # For code generation, use more focused options
            is_code_request = any(keyword in prompt.lower() for keyword in 
                                ['program', 'code', 'function', 'cpp', 'python', 'java', 'javascript', 'algorithm'])
            
            if is_code_request:
                options = {
                    "temperature": 0.3,  # Lower temperature for more focused code
                    "top_p": 0.8,
                    "max_tokens": 500,  # Reduced for faster responses
                    "stop": ["\n\n\n"]  # Stop at multiple newlines to avoid excessive output
                }
                timeout = 15  # Reduced timeout for code generation
            else:
                options = {
                    "temperature": 0.7,
                    "top_p": 0.9,
                    "max_tokens": 200  # Reduced for faster responses
                }
            
            payload = {
                "model": model,
                "prompt": prompt,
                "stream": False,
                "options": options
            }
            
            response = requests.post(
                f"{self.base_url}/api/generate",
                json=payload,
                timeout=timeout
            )
            
            if response.status_code == 200:
                result = response.json()
                return result.get('response', 'No response generated')
            else:
                return f"Error: {response.status_code} - {response.text}"
                
        except requests.exceptions.Timeout:
            return "Request timed out. Ollama is taking too long to respond."
        except Exception as e:
            return f"Error generating response: {str(e)}"
    
    def chat_completion(self, messages: list, model: Optional[str] = None) -> str:
        """Chat completion similar to OpenAI format"""
        model = model or self.current_model
        if not model:
            return "No model available"
            
        # Convert messages to a single prompt
        prompt = ""
        for msg in messages:
            role = msg.get('role', 'user')
            content = msg.get('content', '')
            if role == 'system':
                prompt += f"System: {content}\n"
            elif role == 'user':
                prompt += f"Human: {content}\n"
            elif role == 'assistant':
                prompt += f"Assistant: {content}\n"
        
        prompt += "Assistant: "
        
        return self.generate_response(prompt, model)
    
    def switch_model(self, model_name: str) -> bool:
        """Switch to a different model"""
        if model_name in self.available_models:
            self.current_model = model_name
            print(f"🔄 Switched to model: {model_name}")
            return True
        else:
            print(f"❌ Model {model_name} not available. Available: {self.available_models}")
            return False
    
    def quick_code_response(self, request: str) -> str:
        """Quick code generation with templates for common requests"""
        request_lower = request.lower()
        
        # Fibonacci programs in different languages
        if 'fibonacci' in request_lower or 'fabonaci' in request_lower:
            if 'cpp' in request_lower or 'c++' in request_lower:
                return """Here's a C++ program for Fibonacci sequence:

```cpp
#include <iostream>
using namespace std;

int fibonacci(int n) {
    if (n <= 1)
        return n;
    return fibonacci(n - 1) + fibonacci(n - 2);
}

// Iterative version (more efficient)
int fibonacciIterative(int n) {
    if (n <= 1) return n;
    
    int a = 0, b = 1, c;
    for (int i = 2; i <= n; i++) {
        c = a + b;
        a = b;
        b = c;
    }
    return b;
}

int main() {
    int n;
    cout << "Enter number of terms: ";
    cin >> n;
    
    cout << "Fibonacci sequence: ";
    for (int i = 0; i < n; i++) {
        cout << fibonacciIterative(i) << " ";
    }
    cout << endl;
    
    return 0;
}
```

This program includes both recursive and iterative versions of Fibonacci calculation. The iterative version is more efficient for larger numbers."""
            
            elif 'python' in request_lower:
                return """Here's a Python program for Fibonacci sequence:

```python
def fibonacci_recursive(n):
    if n <= 1:
        return n
    return fibonacci_recursive(n-1) + fibonacci_recursive(n-2)

def fibonacci_iterative(n):
    if n <= 1:
        return n
    
    a, b = 0, 1
    for _ in range(2, n + 1):
        a, b = b, a + b
    return b

def fibonacci_sequence(n):
    return [fibonacci_iterative(i) for i in range(n)]

# Main program
if __name__ == "__main__":
    n = int(input("Enter number of terms: "))
    
    print("Fibonacci sequence:")
    sequence = fibonacci_sequence(n)
    print(" ".join(map(str, sequence)))
    
    print(f"\\nThe {n}th Fibonacci number is: {fibonacci_iterative(n)}")
```"""
            
        # Return None if no quick template matches
        return None

# Test the Ollama client
if __name__ == "__main__":
    client = OllamaClient()
    
    if client.current_model:
        print("Testing Ollama integration...")
        response = client.generate_response("Hello! How are you today?")
        print(f"Response: {response}")
    else:
        print("No models available for testing.")
