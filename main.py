import json
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.lang import Builder
from components.music_service import suggest_music
from components.DeezerPlayer import DeezerPlayer

# โหลด KV Language
Builder.load_file("mood_tracker.kv")

deezer_player = DeezerPlayer().play_preview


class MoodTracker:
    def __init__(self):
        self.data = {"moods": [], "text": []}

    def track_mood(self, mood: str):
        self.data["moods"].append(mood)
        print(f"Your Mood: {mood}")

    def track_text(self, text: str):
        self.data["text"].append(text)
        print(f"Your Emotions Description: {text}")

    def show_moods(self):
        if not self.data["moods"]:
            return None
        return list(zip(self.data["moods"], self.data["text"]))

    def save_to_file(self, filename="mood_data.json"):
        with open(filename, "w") as file:
            json.dump(self.data, file, indent=4)
        print("Data saved successfully!")


class MoodSelect(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.tracker = MoodTracker()

    def emoji_select(self, mood):
        self.tracker.track_mood(mood)

    def submit_mood(self):
        text = self.ids.text_input.text
        if text:
            self.tracker.track_text(text)
            mood_data = self.tracker.show_moods()
            if mood_data:
                response = suggest_music(mood_data[0][0])
                track, artist = split_text(response)

                if track and artist:
                    self.ids.song_label.text = f"🎵 {track} - {artist}"
                    deezer_player(None, track, artist)

            self.tracker.save_to_file()
            self.ids.text_input.text = ""


def split_text(text):
    text = text.replace('"', "")
    if " by " in text:
        return text.split(" by ", 1)
    return text, "Unknown Artist"


class MoodTrackerApp(App):
    def build(self):
        return MoodSelect()


if __name__ == "__main__":
    MoodTrackerApp().run()
