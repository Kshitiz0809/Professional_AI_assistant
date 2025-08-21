import tkinter as tk
from tkinter import scrolledtext, ttk, messagebox
import threading
from voice_assistant import VoiceAssistant
import requests
import sys

class ModernAssistantGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("🤖 Professional AI Assistant")
        self.root.geometry("800x900")
        self.root.minsize(600, 700)
        self.root.configure(bg='#f0f0f0')
        
        # Set modern theme
        self.setup_theme()
        
        self.context = {}
        self.assistant = VoiceAssistant()
        
        self.setup_modern_gui()
        self.load_models()
        
        # Protocol for window closing
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
    def setup_theme(self):
        """Setup modern theme colors"""
        self.colors = {
            'bg_primary': '#2c3e50',
            'bg_secondary': '#34495e', 
            'bg_light': '#ecf0f1',
            'text_dark': '#2c3e50',
            'text_light': '#ffffff',
            'accent': '#3498db',
            'success': '#27ae60',
            'warning': '#f39c12',
            'danger': '#e74c3c'
        }
        
        # Configure ttk styles
        style = ttk.Style()
        style.theme_use('clam')
        
        # Button styles
        style.configure('Modern.TButton',
                       background=self.colors['accent'],
                       foreground='white',
                       borderwidth=0,
                       focuscolor='none',
                       padding=(10, 8))
        
        style.map('Modern.TButton',
                 background=[('active', '#2980b9')])
        
        style.configure('Danger.TButton',
                       background=self.colors['danger'],
                       foreground='white',
                       borderwidth=0,
                       focuscolor='none',
                       padding=(10, 8))
        
        style.map('Danger.TButton',
                 background=[('active', '#c0392b')])
        
    def setup_modern_gui(self):
        # Main container
        main_frame = tk.Frame(self.root, bg=self.colors['bg_light'])
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Header Section
        self.create_header(main_frame)
        
        # Chat Section
        self.create_chat_section(main_frame)
        
        # Input Section
        self.create_input_section(main_frame)
        
        # Control Section
        self.create_control_section(main_frame)
        
        # Footer Section
        self.create_footer_section(main_frame)
        
    def create_header(self, parent):
        """Create modern header with title and controls"""
        header_frame = tk.Frame(parent, bg=self.colors['bg_primary'], height=80)
        header_frame.pack(fill=tk.X, pady=(0, 20))
        header_frame.pack_propagate(False)
        
        # Title
        title_label = tk.Label(header_frame, 
                              text="🤖 Professional AI Assistant",
                              font=('Arial', 18, 'bold'),
                              bg=self.colors['bg_primary'],
                              fg=self.colors['text_light'])
        title_label.pack(side=tk.LEFT, padx=20, pady=20)
        
        # Close button
        close_btn = ttk.Button(header_frame, 
                              text="✕ Close",
                              style='Danger.TButton',
                              command=self.on_closing)
        close_btn.pack(side=tk.RIGHT, padx=20, pady=20)
        
        # Minimize button
        minimize_btn = ttk.Button(header_frame,
                                 text="− Minimize", 
                                 style='Modern.TButton',
                                 command=self.minimize_window)
        minimize_btn.pack(side=tk.RIGHT, padx=10, pady=20)
        
    def create_chat_section(self, parent):
        """Create modern chat display area"""
        chat_frame = tk.LabelFrame(parent, 
                                  text=" 💬 Conversation ",
                                  font=('Arial', 12, 'bold'),
                                  bg=self.colors['bg_light'],
                                  fg=self.colors['text_dark'])
        chat_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 15))
        
        # Chat display with modern styling
        self.chat_area = scrolledtext.ScrolledText(chat_frame, 
                                                  wrap=tk.WORD, 
                                                  width=70, 
                                                  height=25,
                                                  bg='white',
                                                  fg=self.colors['text_dark'],
                                                  font=('Consolas', 10),
                                                  borderwidth=2,
                                                  relief=tk.FLAT)
        self.chat_area.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        # Configure text tags for different message types
        self.chat_area.tag_configure("user", foreground=self.colors['accent'], font=('Consolas', 10, 'bold'))
        self.chat_area.tag_configure("assistant", foreground=self.colors['success'], font=('Consolas', 10, 'bold'))
        self.chat_area.tag_configure("system", foreground=self.colors['warning'], font=('Consolas', 10, 'bold'))
        
    def create_input_section(self, parent):
        """Create modern input section"""
        input_frame = tk.LabelFrame(parent,
                                   text=" ✏️ Message Input ",
                                   font=('Arial', 12, 'bold'),
                                   bg=self.colors['bg_light'],
                                   fg=self.colors['text_dark'])
        input_frame.pack(fill=tk.X, pady=(0, 15))
        
        # Input container
        input_container = tk.Frame(input_frame, bg=self.colors['bg_light'])
        input_container.pack(fill=tk.X, padx=15, pady=15)
        
        # Input field with modern styling
        self.input_field = tk.Entry(input_container,
                                   font=('Arial', 11),
                                   bg='white',
                                   fg=self.colors['text_dark'],
                                   borderwidth=2,
                                   relief=tk.FLAT,
                                   insertwidth=2)
        self.input_field.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=8)
        self.input_field.bind("<Return>", lambda e: self.send_message())
        
        # Send button
        self.send_button = ttk.Button(input_container,
                                     text="📤 Send",
                                     style='Modern.TButton',
                                     command=self.send_message)
        self.send_button.pack(side=tk.RIGHT, padx=(10, 0))
        
    def create_control_section(self, parent):
        """Create modern control buttons section"""
        control_frame = tk.LabelFrame(parent,
                                     text=" 🎛️ Controls ",
                                     font=('Arial', 12, 'bold'),
                                     bg=self.colors['bg_light'],
                                     fg=self.colors['text_dark'])
        control_frame.pack(fill=tk.X, pady=(0, 15))
        
        # Button container
        btn_container = tk.Frame(control_frame, bg=self.colors['bg_light'])
        btn_container.pack(fill=tk.X, padx=15, pady=15)
        
        # Voice input button
        self.voice_button = ttk.Button(btn_container,
                                      text="🎤 Voice Input",
                                      style='Modern.TButton',
                                      command=self.start_voice_input)
        self.voice_button.pack(side=tk.LEFT, padx=(0, 10))
        
        # Server status button
        self.status_button = ttk.Button(btn_container,
                                       text="🔍 Check Server",
                                       style='Modern.TButton',
                                       command=self.check_server_status)
        self.status_button.pack(side=tk.LEFT, padx=(0, 10))
        
        # Clear chat button
        self.clear_button = ttk.Button(btn_container,
                                      text="🗑️ Clear Chat",
                                      style='Modern.TButton',
                                      command=self.clear_chat)
        self.clear_button.pack(side=tk.LEFT, padx=(0, 10))
        
        # Model selection section
        model_container = tk.Frame(control_frame, bg=self.colors['bg_light'])
        model_container.pack(fill=tk.X, padx=15, pady=(0, 15))
        
        tk.Label(model_container,
                text="🤖 AI Model:",
                font=('Arial', 11, 'bold'),
                bg=self.colors['bg_light'],
                fg=self.colors['text_dark']).pack(side=tk.LEFT)
        
        self.model_var = tk.StringVar()
        self.model_combo = ttk.Combobox(model_container,
                                       textvariable=self.model_var,
                                       state="readonly",
                                       width=30,
                                       font=('Arial', 10))
        self.model_combo.pack(side=tk.LEFT, padx=10)
        
        self.switch_button = ttk.Button(model_container,
                                       text="🔄 Switch Model",
                                       style='Modern.TButton',
                                       command=self.switch_model)
        self.switch_button.pack(side=tk.RIGHT)
        
    def create_footer_section(self, parent):
        """Create modern footer with status"""
        footer_frame = tk.Frame(parent, bg=self.colors['bg_secondary'], height=40)
        footer_frame.pack(fill=tk.X)
        footer_frame.pack_propagate(False)
        
        # Status label
        self.status_label = tk.Label(footer_frame,
                                    text="🟢 Ready | Server: http://localhost:8001",
                                    font=('Arial', 9),
                                    bg=self.colors['bg_secondary'],
                                    fg=self.colors['text_light'])
        self.status_label.pack(side=tk.LEFT, padx=15, pady=10)
        
        # Version info
        version_label = tk.Label(footer_frame,
                                text="v2.0 Professional Edition",
                                font=('Arial', 9),
                                bg=self.colors['bg_secondary'],
                                fg=self.colors['text_light'])
        version_label.pack(side=tk.RIGHT, padx=15, pady=10)
        
    def minimize_window(self):
        """Minimize the window"""
        self.root.iconify()
        
    def on_closing(self):
        """Handle window closing with confirmation"""
        if messagebox.askokcancel("Close Application", 
                                 "Are you sure you want to close the AI Assistant?"):
            self.root.quit()
            self.root.destroy()
            sys.exit(0)
    
    def append_message(self, sender, message):
        """Add message to chat with proper formatting"""
        self.chat_area.insert(tk.END, f"{sender}: ", sender.lower())
        self.chat_area.insert(tk.END, f"{message}\n\n")
        self.chat_area.see(tk.END)
        
    def send_message(self):
        """Send message with modern UI updates"""
        message = self.input_field.get().strip()
        if not message:
            return
        
        self.input_field.delete(0, tk.END)
        self.append_message("You", message)
        self.send_button.configure(text="⏳ Sending...", state="disabled")
        
        # Send in background thread
        threading.Thread(target=self._send_message_thread, args=(message,), daemon=True).start()
    
    def _send_message_thread(self, message):
        """Background thread for sending messages"""
        try:
            response = requests.post(
                "http://localhost:8001/chat",
                json={"message": message, "context": self.context},
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                answer = result.get("answer", "No response received")
                provider = result.get("provider", "Unknown")
                self.context = result.get("context", {})
                
                # Update UI in main thread
                self.root.after(0, lambda: self.append_message("Assistant", answer))
                self.root.after(0, lambda: self.append_message("System", f"🤖 Provider: {provider}"))
            else:
                self.root.after(0, lambda: self.append_message("Assistant", 
                    f"❌ Server error: {response.status_code}"))
        except Exception as e:
            self.root.after(0, lambda: self.append_message("Assistant", 
                f"❌ Cannot connect to backend server. Error: {str(e)}"))
        finally:
            # Re-enable send button
            self.root.after(0, lambda: self.send_button.configure(text="📤 Send", state="normal"))
    
    def start_voice_input(self):
        """Start voice input with UI feedback"""
        self.voice_button.configure(text="🎙️ Listening...", state="disabled")
        threading.Thread(target=self._voice_input_thread, daemon=True).start()
    
    def _voice_input_thread(self):
        """Background thread for voice input"""
        try:
            text = self.assistant.listen()
            if text and text != "Could not understand audio":
                self.root.after(0, lambda: self.input_field.insert(0, text))
                self.root.after(0, lambda: self.append_message("System", f"🎤 Voice input: {text}"))
            else:
                self.root.after(0, lambda: self.append_message("System", 
                    "❌ Could not understand voice input"))
        except Exception as e:
            self.root.after(0, lambda: self.append_message("System", 
                f"❌ Voice input error: {str(e)}"))
        finally:
            self.root.after(0, lambda: self.voice_button.configure(text="🎤 Voice Input", state="normal"))
    
    def check_server_status(self):
        """Check server status with modern feedback"""
        self.status_button.configure(text="🔄 Checking...", state="disabled")
        threading.Thread(target=self._check_server_thread, daemon=True).start()
    
    def _check_server_thread(self):
        """Background thread for server status check"""
        try:
            # Check server connectivity
            response = requests.get("http://localhost:8001", timeout=3)
            self.root.after(0, lambda: self.append_message("System", "✅ Server is running and connected!"))
            
            # Check AI providers status
            models_response = requests.get("http://localhost:8001/models", timeout=3)
            if models_response.status_code == 200:
                models_data = models_response.json()
                providers = models_data.get("providers", {})
                
                self.root.after(0, lambda: self.append_message("System", "🤖 AI Providers Status:"))
                
                # Show each provider status
                for provider_name, provider_info in providers.items():
                    status = "✅ configured" if provider_info.get("status") == "configured" else "✅ connected" if provider_info.get("status") == "connected" else "❌ unavailable"
                    description = provider_info.get("description", "")
                    self.root.after(0, lambda p=provider_name.upper(), s=status, d=description: 
                        self.append_message("System", f"   {p}: {s}\n   → {d}"))
                
                priority = models_data.get("priority_order", "Not specified")
                self.root.after(0, lambda: self.append_message("System", f"🎯 Priority: {priority}"))
                
                # Update status bar
                working_count = sum(1 for p in providers.values() 
                                   if p.get("status") in ["configured", "connected"])
                status_text = f"🟢 Ready | {working_count}/{len(providers)} providers active"
                self.root.after(0, lambda: self.status_label.configure(text=status_text))
                
        except Exception as e:
            self.root.after(0, lambda: self.append_message("System", 
                "❌ Cannot connect to backend server. Please make sure the server is running on http://localhost:8001"))
            self.root.after(0, lambda: self.status_label.configure(text="🔴 Server Offline"))
        finally:
            self.root.after(0, lambda: self.status_button.configure(text="🔍 Check Server", state="normal"))
    
    def clear_chat(self):
        """Clear chat with confirmation"""
        if messagebox.askyesno("Clear Chat", "Are you sure you want to clear the conversation?"):
            self.chat_area.delete('1.0', tk.END)
            self.context = {}
            self.append_message("System", "🗑️ Chat cleared!")
    
    def load_models(self):
        """Load available models from server"""
        try:
            response = requests.get("http://localhost:8001/models", timeout=3)
            if response.status_code == 200:
                models_data = response.json()
                providers = models_data.get("providers", {})
                
                # Collect all available models from all providers
                all_models = []
                for provider_name, provider_info in providers.items():
                    if provider_info.get("status") in ["configured", "connected"]:
                        available = provider_info.get("available", [])
                        for model in available:
                            # Add provider prefix for clarity
                            display_name = f"{provider_name.title()}: {model}"
                            all_models.append(display_name)
                
                # Update dropdown with all models
                self.model_combo['values'] = all_models
                
                # Set default to first working provider's model
                if all_models:
                    self.model_var.set(all_models[0])
                    
                print(f"🔄 Loaded {len(all_models)} models: {all_models}")
                
        except Exception as e:
            self.append_message("System", f"Could not load models: {str(e)}")
            print(f"❌ Model loading error: {e}")
    
    def switch_model(self):
        """Switch AI model with modern feedback"""
        selected_model = self.model_var.get()
        if not selected_model:
            return
        
        self.switch_button.configure(text="🔄 Switching...", state="disabled")
        
        try:
            # Parse the model format "Provider: model"
            if ":" in selected_model:
                provider, model_name = selected_model.split(":", 1)
                provider = provider.strip().lower()
                model_name = model_name.strip()
                
                if provider == "ollama":
                    # Only Ollama models can be switched via API
                    response = requests.post(
                        "http://localhost:8001/switch_model",
                        json={"model": model_name},
                        timeout=5
                    )
                    result = response.json()
                    if "error" in result:
                        self.append_message("System", f"❌ {result['error']}")
                    else:
                        self.append_message("System", f"✅ {result['message']}")
                else:
                    # For Gemini/OpenAI, just show a message (priority order handles this)
                    self.append_message("System", f"🔄 Selected {selected_model}. The system will prioritize this provider for responses.")
            else:
                self.append_message("System", "❌ Invalid model format")
                
        except Exception as e:
            self.append_message("System", f"Error switching model: {str(e)}")
        finally:
            self.switch_button.configure(text="🔄 Switch Model", state="normal")

if __name__ == "__main__":
    root = tk.Tk()
    app = ModernAssistantGUI(root)
    
    # Initial welcome message
    app.append_message("Assistant", "Hello! How can I help you today?")
    app.append_message("System", "🚀 Server is running and connected!")
    
    root.mainloop()
