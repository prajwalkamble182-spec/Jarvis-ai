from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window
from kivy.clock import Clock
import threading

Window.clearcolor = (0.05, 0.07, 0.1, 1)

class JarvisUI(BoxLayout):
    def __init__(self, **kwargs):
        super(JarvisUI, self).__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = 15
        self.spacing = 10

        self.header = Label(
            text="[b]J.A.R.V.I.S.[/b]\n[size=12][color=00ffff]SYSTEM ONLINE[/color][/size]",
            markup=True,
            font_size='22sp',
            size_hint=(1, 0.12),
            color=(0, 0.9, 1, 1)
        )
        self.add_widget(self.header)

        self.scroll = ScrollView(size_hint=(1, 0.68))
        self.log_label = Label(
            text="[color=00ffaa]JARVIS:[/color] Hello! I am online and ready for your commands.\n",
            markup=True,
            font_size='14sp',
            size_hint_y=None,
            text_size=(Window.width - 40, None),
            halign='left',
            valign='top'
        )
        self.log_label.bind(texture_size=lambda instance, value: setattr(instance, 'height', value[1]))
        self.scroll.add_widget(self.log_label)
        self.add_widget(self.scroll)

        self.input_field = TextInput(
            hint_text="Enter command or tap Speak...",
            multiline=False,
            size_hint=(1, 0.1),
            background_color=(0.12, 0.15, 0.2, 1),
            foreground_color=(1, 1, 1, 1),
            cursor_color=(0, 0.9, 1, 1),
            padding=(10, 10, 10, 10)
        )
        self.input_field.bind(on_text_validate=self.send_command)
        self.add_widget(self.input_field)

        btn_layout = BoxLayout(size_hint=(1, 0.1), spacing=10)

        self.send_btn = Button(
            text="SEND",
            background_normal='',
            background_color=(0, 0.6, 0.8, 1),
            bold=True
        )
        self.send_btn.bind(on_press=self.send_command)

        self.mic_btn = Button(
            text="🎙️ SPEAK",
            background_normal='',
            background_color=(0, 0.8, 0.4, 1),
            bold=True
        )
        self.mic_btn.bind(on_press=self.trigger_voice)

        btn_layout.add_widget(self.send_btn)
        btn_layout.add_widget(self.mic_btn)
        self.add_widget(btn_layout)

    def append_log(self, text):
        def update_text(dt):
            self.log_label.text += text + "\n"
            self.scroll.scroll_y = 0
        Clock.schedule_once(update_text)

    def send_command(self, instance):
        user_text = self.input_field.text.strip()
        if not user_text:
            return
        
        self.append_log(f"[color=ffffff]You:[/color] {user_text}")
        self.input_field.text = ""

        threading.Thread(target=self.process_jarvis_response, args=(user_text,)).start()

    def process_jarvis_response(self, text):
        cmd = text.lower()
        if "hello" in cmd or "hi" in cmd:
            reply = "Greetings! How may I assist you today?"
        elif "time" in cmd:
            import datetime
            now = datetime.datetime.now().strftime("%I:%M %p")
            reply = f"The current time is {now}."
        elif "who are you" in cmd:
            reply = "I am JARVIS, your personal AI assistant."
        else:
            reply = f"Command '{text}' received. I am processing your request."

        self.append_log(f"[color=00ffaa]JARVIS:[/color] {reply}")

    def trigger_voice(self, instance):
        self.append_log("[color=ffcc00]System:[/color] Listening for voice input...")

class JarvisApp(App):
    def build(self):
        self.title = "JARVIS Assistant"
        return JarvisUI()

if __name__ == '__main__':
    JarvisApp().run()
  
