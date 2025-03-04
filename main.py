from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from components.music_service import suggest_music
from components.DeezerPlayer import DeezerPlayer

deezer_player = DeezerPlayer().play_preview


class MoodSelect(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.tracker = MoodTracker()
        self.orientation = "vertical"
        self.space = 20
        self.padding = 50

        self.add_widget(Label(text="What's your mood today?", size_hint_y=None, height=30))

        emoji_grid = BoxLayout(spacing=10, size_hint_y=None, height=80)
        self.emoji_map = {
            "😊 Happy": "Happy",
            "😢 Sad": "Sad",
            "😡 Angry": "Angry",
            "😌 Calm": "Calm",
            "🤩 Excited": "Excited",
            "🔥 Ahh~~~": "Horny",
        }

        for emoji, mood in self.emoji_map.items():
            btn = Button(
                text=emoji,
                font_size=40,
            )
            btn.bind(on_press=lambda instance, e=mood: self.emoji_select(e))
            emoji_grid.add_widget(btn)
        self.add_widget(emoji_grid)

        # Text input
        self.add_widget(Label(text="📝 Describe your feelings:", size_hint_y=None, height=30))
        self.text_input = TextInput(
            multiline=False, size_hint_y=None, height=100, hint_text="Type a short description of your emotions..."
        )
        self.add_widget(self.text_input)

        self.submit_button = Button(text="Get Music Recommendation", size_hint_y=None, height=50)
        self.submit_button.bind(on_press=self.submit_mood)
        self.add_widget(self.submit_button)

    def emoji_select(self, mood):
        self.tracker.track_mood(mood)

    def submit_mood(self, instance):
        text = self.text_input.text
        if text:
            self.tracker.track_text(text)  # print คำอธิบายอารมณ์
            mood_data = self.tracker.show_moods()
            if mood_data:
                response = suggest_music(mood_data[0])
                track, artist = split_text(response)
                deezer_player(None, track, artist)
            self.text_input.text = ""


class MoodTracker:
    def __init__(self):
        self.moods = []
        self.text = []
        self.all = None

    def track_mood(self, mood: str):
        self.moods.append(mood)
        print(f"Your Mood : {mood}")

    def track_text(self, text: str):
        self.text.append(text)
        print(f"Your Shortly describe your emotions : {self.moods}")

    def show_moods(self):
        self.all = zip(self.moods, self.text)
        if self.all is None:
            print("Empty")
        else:
            return list(self.all)
            # print('Your Moods:')
            # for mood in self.all:
            #     print(f'- {mood}')


def split_text(text):
    text = text.replace('"', "")
    return text.split(" by ")


class MoodTrackerApp(App):
    def build(self):
        return MoodSelect()


if __name__ == "__main__":
    MoodTrackerApp().run()
