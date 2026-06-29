
import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.utils import platform
from kivy.core.window import Window
from datetime import datetime
from kivy.clock import Clock
import json

# --- استيراد مكتبات معالجة اللغة العربية ---
try:
    import arabic_reshaper
    from bidi.algorithm import get_display
except ImportError:
    arabic_reshaper = None
    get_display = None

# --- إعدادات الخط العربي ---
# ملاحظة: استبدل المسار أدناه بمسار ملف الخط (.ttf)
ARABIC_FONT = "DejaVuSans.ttf" 

def fix_arabic(text):
    """دالة لمعالجة النصوص العربية لتظهر بشكل صحيح في Kivy"""
    if not text or not arabic_reshaper:
        return text
    try:
        reshaped_text = arabic_reshaper.reshape(text)
        bidi_text = get_display(reshaped_text)
        return bidi_text
    except Exception:
        return text


# --- محاولة استيراد مكتبات أندرويد فقط إذا كان النظام أندرويد ---
if platform == 'android':
    try:
        from jnius import autoclass, cast
        PythonActivity = autoclass('org.kivy.android.PythonActivity')
        Intent = autoclass('android.content.Intent')
        Settings = autoclass('android.provider.Settings')
        Uri = autoclass('android.net.Uri')
        MediaProjectionManager = autoclass('android.media.projection.MediaProjectionManager')
        Context = autoclass('android.content.Context')
    except ImportError:
        print("Error: jnius not found")
        autoclass = None
else:
    autoclass = None

class AIAgentGUI(BoxLayout):
    def __init__(self, **kwargs):
        super(AIAgentGUI, self).__init__(**kwargs)
        
        self.orientation = 'vertical'
        self.padding = 20
        self.spacing = 10 

        # --- تتبع حالة الحلقة (Anti-Looping) ---
        self.last_action = None
        self.repeat_count = 0
        self.is_running = False

        # Application Title
        self.add_widget(Label(
            text=fix_arabic("AI Agent - Closed Loop Engineering (v4)"),
            font_size='22sp', bold=True, size_hint_y=None, height=45
        ))

        # --- 1. Target Package Name ---
        self.add_widget(Label(
            text=fix_arabic("Target Package Name:"),
            size_hint_y=None, height=25, halign='left', text_size=(Window.width-40, 25)
        ))
        self.package_input = TextInput(
            text="com.whatsapp", multiline=False, size_hint_y=None, height=45, font_size='16sp'
        )
        self.add_widget(self.package_input)

        # --- 2. Task Description ---
        self.add_widget(Label(
            text=fix_arabic("Task Description & Context:"),
            size_hint_y=None, height=25, halign='left', text_size=(Window.width-40, 25)
        ))
        self.task_input = TextInput(
            text=fix_arabic("Open WhatsApp, search for 'Mom' and send 'I am on my way'."),
            multiline=True, size_hint_y=None, height=80, font_size='14sp'
        )
        self.add_widget(self.task_input)

        # --- 3. Logs Area ---
        self.add_widget(Label(
            text=fix_arabic("Agent Intelligence Logs:"),
            size_hint_y=None, height=25, halign='left', text_size=(Window.width-40, 25)
        ))
        self.logs_display = TextInput(
            text=fix_arabic("-- Agent ready for Full Loop Engineering (English) --\n"),
            readonly=True, multiline=True,
            background_color=(0.02, 0.02, 0.02, 1),
            foreground_color=(0.1, 0.9, 0.1, 1),
            font_size='13sp'
        )
        self.add_widget(self.logs_display)

        # --- 4. Start Button ---
        self.start_button = Button(
            text=fix_arabic("Start Loop Engineering"),
            size_hint_y=None, height=60,
            background_color=(0.2, 0.7, 0.3, 1),
            bold=True
        )
        self.start_button.bind(on_press=self.toggle_agent_loop)
        self.add_widget(self.start_button)
        
        self.gemini_api_key = "YOUR_GEMINI_API_KEY_HERE"


    def log_status(self, message):
        now = datetime.now().strftime("%H:%M:%S")
        fixed_msg = fix_arabic(message)
        self.logs_display.text += f"[{now}] {fixed_msg}\n"
        self.logs_display.cursor = (0, len(self.logs_display.text))

    def toggle_agent_loop(self, instance):
        """Toggle the agent loop on/off"""
        if not self.is_running:
            self.is_running = True
            self.start_button.text = fix_arabic("Stop Agent Loop")
            self.start_button.background_color = (0.9, 0.2, 0.2, 1)
            self.run_automated_cycle()
        else:
            self.is_running = False
            self.start_button.text = fix_arabic("Start Loop Engineering")
            self.start_button.background_color = (0.2, 0.7, 0.3, 1)
            self.log_status("System: Agent loop stopped manually.")



    def run_automated_cycle(self, *args):
        """Start the Loop Engineering cycle (Observation -> Evaluation -> Action)"""
        if not self.is_running: return

        package_name = self.package_input.text.strip()
        user_task = self.task_input.text.strip()
        
        if not package_name or not user_task:
            self.log_status("Error: Input fields are empty.")
            self.is_running = False
            return

        self.log_status("--- Starting New Loop Cycle ---")
        self.log_status("[1. Observation]: Capturing screen and analyzing state...")
        
        # Simulate Gemini API call
        self.call_gemini_api(package_name, user_task)

    def call_gemini_api(self, package_name, user_task):
        """Send data to Gemini and wait for decision"""
        self.log_status("[2. Evaluation]: Gemini is processing data like a human...")
        
        # Simulated response
        simulated_response = {
            "observation": "I see the home screen with the target app icon.",
            "evaluation": f"To complete the task '{user_task}', I need to open {package_name}.",
            "action_type": "CLICK",
            "coordinates": {"x": 500, "y": 1000},
            "text_to_type": ""
        }
        
        self.process_gemini_decision(simulated_response)

    def process_gemini_decision(self, response_json):
        """Parse JSON and execute action"""
        obs = response_json.get("observation")
        eval_txt = response_json.get("evaluation")
        action = response_json.get("action_type", "").upper()
        coords = response_json.get("coordinates", {})
        
        self.log_status(f"AI Observation: {obs}")
        self.log_status(f"AI Evaluation: {eval_txt}")

        # Anti-Looping Safeguard
        if self.last_action == action and self.last_coords == coords:
            self.repeat_count += 1
            if self.repeat_count >= 2:
                self.log_status("Warning: Stickiness detected! Recovering (Anti-Looping)...")
                self.execute_recovery()
                return
        else:
            self.repeat_count = 0
            self.last_action = action
            self.last_coords = coords

        # 3. Action Execution
        self.log_status(f"[3. Execution]: Executing {action} command...")
        
        if action == "CLICK":
            self.perform_click(coords['x'], coords['y'])
        elif action == "TYPE":
            text = response_json.get("text_to_type", "")
            self.perform_type(text)
        elif action == "SCROLL":
            self.perform_scroll()
        
        self.log_status("Loop Closure: Execution done. Waiting 2 seconds for UI update...")
        Clock.schedule_once(self.run_automated_cycle, 2)

    def perform_click(self, x, y):
        if platform == 'android' and autoclass:
            self.log_status(f"Android: Dispatching click at ({x}, {y}) via Accessibility Service.")
        else:
            self.log_status(f"Simulation: Clicked successfully at ({x}, {y}).")

    def perform_type(self, text):
        self.log_status(f"Simulation: Typing text: '{text}'")

    def perform_scroll(self):
        self.log_status("Simulation: Executing scroll action.")

    def execute_recovery(self):
        """Simulate human-like recovery"""
        self.log_status("Recovery: Pressing BACK button to escape stuck state.")
        self.repeat_count = 0
        Clock.schedule_once(self.run_automated_cycle, 3)

class AIAgentApp(App):
    def build(self):
        self.title = "AI Agent - Autonomous Loop Engineering"
        return AIAgentGUI()

if __name__ == '__main__':
    AIAgentApp().run()
