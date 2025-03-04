from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from components.music_service import suggest_music
from components.DeezerPlayer import DeezerPlayer
import os

deezer_player = DeezerPlayer().play_preview

def get_api_key():
    key = os.getenv("OPENAI_API_KEY")
    if not key:
        print("Error: OPENAI_API_KEY is not set.")
    return key

class MoodSelect(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.tracker = MoodTracker()
        self.orientation = "vertical"
        self.padding = [20, 20, 20, 20]
        self.spacing = 10

        self.add_widget(Label(text="🎵 What's your mood today?", font_size=24, bold=True, size_hint_y=None, height=40))

        emoji_grid = GridLayout(cols=3, spacing=10, size_hint_y=None, height=200)
        self.emoji_map = {
            "😊 Happy": "Happy",
            "😢 Sad": "Sad",
            "😡 Angry": "Angry",
            "😌 Calm": "Calm",
            "🤩 Excited": "Excited",
            "🔥 Ahh~~~": "Horny",
        }

        for emoji, mood in self.emoji_map.items():
            btn = Button(text=emoji, font_size=20, size_hint=(1, None), height=60)
            btn.bind(on_press=lambda instance, e=mood: self.emoji_select(e))
            emoji_grid.add_widget(btn)
        self.add_widget(emoji_grid)

        self.add_widget(Label(text="📝 Describe your feelings:", font_size=18, size_hint_y=None, height=30))
        self.text_input = TextInput(multiline=True, size_hint_y=None, height=100, hint_text="Type a short description of your emotions...")
        self.add_widget(self.text_input)

        self.submit_button = Button(text="🎶 Get Music Recommendation", font_size=18, size_hint_y=None, height=60, background_color=[0.2, 0.6, 1, 1])
        self.submit_button.bind(on_press=self.submit_mood)
        self.add_widget(self.submit_button)

        self.result_label = Label(text="", font_size=16, size_hint_y=None, height=40)
        self.add_widget(self.result_label)
    
    def emoji_select(self, mood):
        self.tracker.track_mood(mood)

    def submit_mood(self, instance):
        text = self.text_input.text
        if text:
            self.tracker.track_text(text)
            mood_data = self.tracker.show_moods()
            if mood_data:
                response = suggest_music(mood_data[0])
                if response:
                    track, artist = split_text(response)
                    self.result_label.text = f"🎵 Recommended: {track} by {artist}"
                    deezer_player(None, track, artist)
                else:
                    self.result_label.text = "No recommendation available."
            self.text_input.text = ""

class MoodTracker:
    def __init__(self):
        self.moods = []
        self.text = []

    def track_mood(self, mood: str):
        self.moods.append(mood)
        print(f"Your Mood: {mood}")

    def track_text(self, text: str):
        self.text.append(text)
        print(f"Your Description: {text}")

    def show_moods(self):
        if not self.moods or not self.text:
            print("No data recorded")
            return None
        return [(self.moods[-1], self.text[-1])]

def split_text(text):
    text = text.replace('"', "")
    return text.split(" by ")

class MoodTrackerApp(App):
    def build(self):
        return MoodSelect()

if __name__ == "__main__":
    MoodTrackerApp().run()
