import speech_recognition as sr
import pyttsx3
import requests
import json
from datetime import datetime

class VoiceAssistant:
    def __init__(self, backend_url="http://localhost:8000"):
        self.backend_url = backend_url
        self.context = {}
        self.recognizer = sr.Recognizer()
        self.engine = pyttsx3.init()
        
        # Configure voice properties
        self.engine.setProperty('rate', 150)
        voices = self.engine.getProperty('voices')
        self.engine.setProperty('voice', voices[0].id)  # Index 0 for male, 1 for female

    def listen(self):
        """Listen for user input through microphone"""
        with sr.Microphone() as source:
            print("Listening...")
            self.recognizer.adjust_for_ambient_noise(source, duration=1)
            try:
                audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=5)
                text = self.recognizer.recognize_google(audio)
                print("You said:", text)
                return text.lower()
            except sr.WaitTimeoutError:
                print("No speech detected within timeout period")
                return ""
            except sr.UnknownValueError:
                print("Could not understand audio")
                return ""
            except sr.RequestError as e:
                if "Forbidden" in str(e):
                    print("❌ Speech recognition access denied. Possible solutions:")
                    print("1. Check microphone permissions")
                    print("2. Make sure microphone is not being used by another app")
                    print("3. Try running as administrator")
                    print("4. Check internet connection for Google Speech API")
                elif "recognition request failed" in str(e):
                    print("❌ Speech recognition service unavailable")
                    print("💡 Try using text input instead")
                else:
                    print(f"❌ Speech recognition error: {str(e)}")
                return ""
            except Exception as e:
                print(f"❌ Unexpected error: {str(e)}")
                return ""

    def speak(self, text):
        """Convert text to speech"""
        print("Assistant:", text)
        self.engine.say(text)
        self.engine.runAndWait()

    def chat_with_backend(self, message):
        """Send message to backend and get response"""
        try:
            response = requests.post(
                f"{self.backend_url}/chat",
                json={"message": message, "context": self.context}
            )
            result = response.json()
            if "error" in result:
                return f"Error: {result['error']}", {}
            return result["answer"], result["context"]
        except Exception as e:
            return f"Error connecting to backend: {str(e)}", {}

    def execute_task(self, task, parameters=None):
        """Execute specific task through backend"""
        try:
            response = requests.post(
                f"{self.backend_url}/task",
                json={"task": task, "parameters": parameters or {}}
            )
            return response.json()
        except Exception as e:
            return {"error": f"Error executing task: {str(e)}"}

    def run(self):
        """Main loop for voice assistant"""
        self.speak("Hello! I'm your AI assistant. How can I help you?")
        
        while True:
            user_input = self.listen()
            
            if not user_input:
                continue
                
            if user_input in ["exit", "quit", "goodbye"]:
                self.speak("Goodbye! Have a great day!")
                break
                
            # Get response from backend
            answer, new_context = self.chat_with_backend(user_input)
            self.context = new_context
            self.speak(answer)

if __name__ == "__main__":
    assistant = VoiceAssistant()
    assistant.run()
