import tkinter as tk
import configparser
import threading
import time
import random
import base64
import os
import sys
import traceback
from PIL import Image, ImageTk
import pyautogui
from datetime import datetime
from openai import OpenAI

# Set pyautogui safety
pyautogui.PAUSE = 0.1
pyautogui.FAILSAFE = True

class DesktopSayon:
    def __init__(self):
        try:
            print("Initializing Desktop Sayon...")
            self.config = self.load_config()
            print("Config loaded successfully")
            
            self.setup_directories()
            print("Directories created")
            
            self.setup_client()
            print("LLM client setup complete")
            
            # Drag variables
            self.dragging = False
            self.drag_start_time = 0
            self.drag_start_pos = (0, 0)
            self.click_start_time = 0
            
            # Main window setup
            self.root = tk.Tk()
            self.root.title("Desktop Sayon")
            self.root.attributes('-topmost', True)
            self.root.attributes('-transparentcolor', 'black')
            self.root.overrideredirect(True)
            self.root.configure(bg='black')
            print("Main window created")
            
            # Load avatar image
            self.load_avatar()
            print("Avatar loaded successfully")
            
            # Position window at bottom right
            self.position_window()
            print("Window positioned")
            
            # Create UI elements
            self.create_ui()
            print("UI elements created")
            
            # Bind mouse events for drag functionality
            self.setup_mouse_events()
            
            # Start auto dialog timer
            self.schedule_next_dialog()
            print("Auto dialog scheduled")
            
            print("Desktop Sayon initialized successfully!")
            
        except Exception as e:
            print(f"Error during initialization: {e}")
            traceback.print_exc()
            input("Press Enter to exit...")
            sys.exit(1)
        
    def load_config(self):
        """Load configuration from config.ini"""
        try:
            config = configparser.ConfigParser()
            config_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'config', 'config.ini')
            
            if not os.path.exists(config_path):
                raise FileNotFoundError(f"Config file not found: {config_path}")
                
            config.read(config_path, encoding='utf-8')
            print(f"Config loaded from: {config_path}")
            return config
        except Exception as e:
            print(f"Error loading config: {e}")
            raise
        
    def setup_directories(self):
        """Create necessary directories"""
        try:
            base_dir = os.path.dirname(os.path.dirname(__file__))
            images_dir = os.path.join(base_dir, 'record', 'images')
            text_dir = os.path.join(base_dir, 'record', 'text')
            
            os.makedirs(images_dir, exist_ok=True)
            os.makedirs(text_dir, exist_ok=True)
            print(f"Directories created: {images_dir}, {text_dir}")
        except Exception as e:
            print(f"Error creating directories: {e}")
            raise
        
    def setup_client(self):
        """Setup OpenAI client"""
        try:
            self.client = OpenAI(
                base_url=self.config['LLM']['LLM_URL'],
                api_key=self.config['LLM']['LLM_KEY']
            )
        except Exception as e:
            print(f"Error setting up LLM client: {e}")
            raise
        
    def load_avatar(self):
        """Load and process avatar image"""
        try:
            base_dir = os.path.dirname(os.path.dirname(__file__))
            avatar_path = os.path.join(base_dir, 'assets', 'portrait.png')
            
            if not os.path.exists(avatar_path):
                raise FileNotFoundError(f"Avatar image not found: {avatar_path}")
                
            avatar_height = int(self.config['AVATAR']['AVATAR_HEIGHT'])
            
            # Load image
            image = Image.open(avatar_path).convert("RGBA")
            print(f"Avatar loaded from: {avatar_path}")
            
            # Calculate proportional width
            original_width, original_height = image.size
            aspect_ratio = original_width / original_height
            avatar_width = int(avatar_height * aspect_ratio)
            
            # Resize image
            image = image.resize((avatar_width, avatar_height), Image.Resampling.LANCZOS)
            
            # Apply transparency
            transparency = float(self.config['AVATAR']['AVATAR_TRANSPARENCY'])
            # Create new image with adjusted alpha
            data = image.getdata()
            new_data = []
            for item in data:
                if item[3] > 0:  # If not fully transparent
                    new_alpha = int(item[3] * (1 - transparency))
                    new_data.append((item[0], item[1], item[2], new_alpha))
                else:
                    new_data.append(item)
            image.putdata(new_data)
            
            self.avatar_image = ImageTk.PhotoImage(image)
            self.avatar_width = avatar_width
            self.avatar_height = avatar_height
            
            print(f"Avatar processed: {avatar_width}x{avatar_height}, transparency: {transparency}")
            
        except Exception as e:
            print(f"Error loading avatar: {e}")
            raise
        
    def position_window(self):
        """Position window at bottom right of screen"""
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        
        # Calculate window size (avatar + space for larger text above)
        window_width = max(320, self.avatar_width + 20)  # Ensure minimum width for text
        window_height = self.avatar_height + 200  # More space for larger text box
        
        # Position at bottom right with some margin
        margin = 20
        x = screen_width - window_width - margin
        y = screen_height - window_height - margin - 50  # Account for taskbar
        
        self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")
        
        # Store position for drag functionality
        self.window_x = x
        self.window_y = y
        
    def setup_mouse_events(self):
        """Setup mouse events for dragging and clicking"""
        # Only bind events to avatar and main window, exclude text components
        for widget in [self.avatar_label, self.avatar_frame]:
            widget.bind("<Button-1>", self.on_mouse_down)
            widget.bind("<B1-Motion>", self.on_mouse_drag)
            widget.bind("<ButtonRelease-1>", self.on_mouse_up)
            
    def on_mouse_down(self, event):
        """Handle mouse down event"""
        self.click_start_time = time.time()
        self.drag_start_time = time.time()
        self.drag_start_pos = (event.x_root, event.y_root)
        self.dragging = False
        
    def on_mouse_drag(self, event):
        """Handle mouse drag event"""
        current_time = time.time()
        # If mouse has been held for more than 0.3 seconds, start dragging
        if current_time - self.drag_start_time > 0.3:
            if not self.dragging:
                self.dragging = True
                self.root.configure(cursor='fleur')  # Change cursor to indicate dragging
                
            # Calculate new position
            dx = event.x_root - self.drag_start_pos[0]
            dy = event.y_root - self.drag_start_pos[1]
            
            new_x = self.window_x + dx
            new_y = self.window_y + dy
            
            # Keep window on screen
            screen_width = self.root.winfo_screenwidth()
            screen_height = self.root.winfo_screenheight()
            window_width = max(320, self.avatar_width + 20)
            window_height = self.avatar_height + 200
            
            new_x = max(0, min(new_x, screen_width - window_width))
            new_y = max(0, min(new_y, screen_height - window_height))
            
            self.root.geometry(f"+{new_x}+{new_y}")
            
    def on_mouse_up(self, event):
        """Handle mouse release event"""
        current_time = time.time()
        click_duration = current_time - self.click_start_time
        
        if self.dragging:
            # End dragging
            self.dragging = False
            self.root.configure(cursor='')
            # Update stored position
            geometry = self.root.geometry()
            parts = geometry.split('+')
            self.window_x = int(parts[1])
            self.window_y = int(parts[2])
        elif click_duration < 0.3:
            # Short click - trigger dialog
            self.on_avatar_click()
            
    def on_avatar_click(self):
        """Handle avatar click (now called from mouse up)"""
        # Cancel current timer
        if hasattr(self, 'dialog_timer'):
            self.root.after_cancel(self.dialog_timer)
            
        # Perform immediate dialog
        self.perform_dialog_action()
        
        # Schedule next dialog
        self.schedule_next_dialog()
        
    def create_ui(self):
        """Create UI elements"""
        # Create main frame
        self.main_frame = tk.Frame(self.root, bg='black')
        self.main_frame.pack(fill='both', expand=True)
        
        # Text display frame at top (initially hidden)
        self.text_frame = tk.Frame(self.main_frame, bg='black')
        self.text_frame.pack(side='top', pady=(10, 5))
        
        self.text_label = tk.Label(
            self.text_frame,
            text="",
            bg='#FFFFFF',  # White background
            fg='#000000',  # Black text
            font=('Arial', 10),
            wraplength=300,  # Much wider text wrapping
            justify='left',  # Left align for better readability
            padx=12,
            pady=8,
            relief='solid',
            borderwidth=1
        )
        
        # Avatar frame at bottom
        self.avatar_frame = tk.Frame(self.main_frame, bg='black')
        self.avatar_frame.pack(side='bottom', pady=(5, 10))
        
        # Avatar label
        self.avatar_label = tk.Label(
            self.avatar_frame,
            image=self.avatar_image,
            bg='black',
            cursor='hand2'
        )
        self.avatar_label.pack()
        
    def fade_avatar(self, target_alpha, callback=None):
        """Fade avatar to target alpha"""
        current_transparency = float(self.config['AVATAR']['AVATAR_TRANSPARENCY'])
        # Current alpha is the visible alpha (1 - transparency)
        current_alpha = 1 - current_transparency
        
        steps = 10  # Reduced from 20 to make it twice as fast
        alpha_step = (target_alpha - current_alpha) / steps
        
        def fade_step(step):
            if step <= steps:
                alpha = current_alpha + alpha_step * step
                # Ensure alpha is between 0 and 1
                alpha = max(0, min(1, alpha))
                self.set_avatar_alpha(alpha)
                self.root.after(25, lambda: fade_step(step + 1))  # Reduced from 50ms
            elif callback:
                self.root.after(25, callback)  # Small delay before callback
                
        fade_step(1)
        
    def set_avatar_alpha(self, alpha):
        """Set avatar transparency - alpha 1.0 = fully visible, 0.0 = fully transparent"""
        try:
            # Reload original image and apply new alpha
            base_dir = os.path.dirname(os.path.dirname(__file__))
            avatar_path = os.path.join(base_dir, 'assets', 'portrait.png')
            image = Image.open(avatar_path).convert("RGBA")
            
            # Resize
            avatar_height = int(self.config['AVATAR']['AVATAR_HEIGHT'])
            original_width, original_height = image.size
            aspect_ratio = original_width / original_height
            avatar_width = int(avatar_height * aspect_ratio)
            image = image.resize((avatar_width, avatar_height), Image.Resampling.LANCZOS)
            
            # Apply alpha - directly multiply by the alpha value
            data = image.getdata()
            new_data = []
            for item in data:
                if item[3] > 0:  # If pixel has some alpha
                    # Apply the alpha multiplier
                    new_alpha = int(item[3] * alpha)
                    new_data.append((item[0], item[1], item[2], new_alpha))
                else:
                    new_data.append(item)
            image.putdata(new_data)
            
            # Update display
            self.avatar_image = ImageTk.PhotoImage(image)
            self.avatar_label.configure(image=self.avatar_image)
            
        except Exception as e:
            print(f"Error setting avatar alpha: {e}")
        
    def take_screenshot(self):
        """Take screenshot and save"""
        try:
            base_dir = os.path.dirname(os.path.dirname(__file__))
            screenshot_path = os.path.join(base_dir, 'record', 'images', 'screen.png')
            screenshot = pyautogui.screenshot()
            screenshot.save(screenshot_path)
            print(f"Screenshot saved to: {screenshot_path}")
        except Exception as e:
            print(f"Error taking screenshot: {e}")
        
    def get_system_prompt(self):
        """Load system prompt"""
        try:
            base_dir = os.path.dirname(os.path.dirname(__file__))
            prompt_path = os.path.join(base_dir, 'config', 'system_prompt.txt')
            with open(prompt_path, 'r', encoding='utf-8') as f:
                return f.read().strip()
        except Exception as e:
            print(f"Error loading system prompt: {e}")
            return "You are a helpful desktop assistant."
            
    def encode_image_base64(self, image_path):
        """Encode image to base64"""
        try:
            if not os.path.exists(image_path):
                raise FileNotFoundError(f"Image file not found: {image_path}")
                
            with open(image_path, "rb") as image_file:
                image_data = image_file.read()
                if len(image_data) == 0:
                    raise ValueError("Image file is empty")
                return base64.b64encode(image_data).decode('utf-8')
        except Exception as e:
            print(f"Error encoding image: {e}")
            raise
            
    def get_llm_response(self):
        """Get response from LLM"""
        try:
            system_prompt = self.get_system_prompt()
            base_dir = os.path.dirname(os.path.dirname(__file__))
            screenshot_path = os.path.join(base_dir, 'record', 'images', 'screen.png')
            base64_image = self.encode_image_base64(screenshot_path)
            
            response = self.client.chat.completions.create(
                model=self.config['LLM']['LLM_MODEL'],
                messages=[{
                    'role': 'system',
                    'content': system_prompt
                }, {
                    'role': 'user',
                    'content': [{
                        'type': 'text',
                        'text': 'Please analyze this screen capture:'
                    }, {
                        'type': 'image_url',
                        'image_url': {
                            'url': f'data:image/png;base64,{base64_image}'
                        }
                    }]
                }],
                stream=False
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            print(f"Error getting LLM response: {e}")
            return "Error occurred while processing..."
            
    def save_dialogue(self, text):
        """Save dialogue to file"""
        try:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            base_dir = os.path.dirname(os.path.dirname(__file__))
            dialogue_path = os.path.join(base_dir, 'record', 'text', 'dialogue.txt')
            with open(dialogue_path, 'a', encoding='utf-8') as f:
                f.write(f"[{timestamp}] {text}\n")
            print(f"Dialogue saved to: {dialogue_path}")
        except Exception as e:
            print(f"Error saving dialogue: {e}")
            
    def show_text(self, text):
        """Display text above avatar"""
        self.text_label.configure(text=text)
        # Set semi-transparent white background
        self.text_label.configure(bg='#FFFFFF')
        self.text_label.pack(pady=5)
        
        # Hide text after specified time
        display_time = float(self.config['TIMING']['TEXT_DISPLAY_TIME'])
        self.root.after(int(display_time * 60 * 1000), self.hide_text)
        
    def hide_text(self):
        """Hide displayed text"""
        self.text_label.pack_forget()
        
    def perform_dialog_action(self):
        """Perform the main dialog action"""
        def action():
            # Immediately hide avatar
            self.set_avatar_alpha(0)
            
            # Take screenshot after a short delay
            time.sleep(0.2)
            self.take_screenshot()
            
            # Immediately restore avatar to normal transparency
            original_transparency = float(self.config['AVATAR']['AVATAR_TRANSPARENCY'])
            target_alpha = 1 - original_transparency
            self.set_avatar_alpha(target_alpha)
            
            # Get LLM response in background
            def get_response():
                response = self.get_llm_response()
                self.root.after(0, lambda: self.handle_response(response))
                
            threading.Thread(target=get_response, daemon=True).start()
            
        threading.Thread(target=action, daemon=True).start()
        
    def handle_response(self, response):
        """Handle LLM response"""
        self.save_dialogue(response)
        self.show_text(response)
        
    def schedule_next_dialog(self):
        """Schedule next automatic dialog"""
        # Exponential distribution + 1 minute
        mean_interval = float(self.config['TIMING']['DIALOG_INTERVAL'])
        interval = random.expovariate(1/mean_interval) + 1
        
        # Convert to milliseconds
        delay_ms = int(interval * 60 * 1000)
        
        self.dialog_timer = self.root.after(delay_ms, self.auto_dialog)
        
    def auto_dialog(self):
        """Automatic dialog trigger"""
        self.perform_dialog_action()
        self.schedule_next_dialog()
        
    def run(self):
        """Start the application"""
        print("Starting main application loop...")
        self.root.mainloop()

def main():
    try:
        print("Desktop Sayon starting...")
        app = DesktopSayon()
        app.run()
    except Exception as e:
        print(f"Fatal error: {e}")
        traceback.print_exc()
        input("Press Enter to exit...")

if __name__ == "__main__":
    main()
