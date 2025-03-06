from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty
from components.music_service import suggest_music
from components.DeezerPlayer import DeezerPlayer


class MoodSelect(BoxLayout):
    """UI หลักของหน้าเลือกอารมณ์"""

    text_input = ObjectProperty(None)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.tracker = MoodTracker()
        self.player = DeezerPlayer()

    def emoji_select(self, mood):
        """ส่วนไว้รับการเลือก emoji"""
        self.tracker.track_mood(mood)

    def submit_mood(self, *args):
        text = self.text_input.text
        if text:
            self.tracker.track_text(text)  # print คำอธิบายอารมณ์
            self.get_music_recommendation()

    def get_music_recommendation(self):
        mood_data = self.tracker.get_mood_data()
        if mood_data:
            try:
                response = suggest_music(mood_data[0])
                track, artist = split_text(response)
                self.player.play_preview(None, track, artist)
                self.text_input.text = ""  # Clear ช่อง input
            except Exception as e:
                print(f"Error suggesting music: {e}")


class MoodTracker:
    def __init__(self):
        self.moods = []
        self.descriptions = []
        self.all = None

    def track_mood(self, mood: str):
        self.moods.append(mood)
        print(f"Your Mood : {mood}")

    def track_text(self, text: str):
        """เก็บคำอธิบายอารมณ์"""
        self.descriptions.append(text)
        print(f"Your Shortly describe your emotions : {self.moods}")

    def get_mood_data(self):
        """คืนค่าคู่ของอารมณ์กับคำอธิบาย"""
        return list(zip(self.moods, self.descriptions))


def split_text(text):
    text = text.replace('"', "")
    return text.split(" by ")


class MoodTrackerApp(App):
    def build(self):
        return MoodSelect()


if __name__ == "__main__":
    MoodTrackerApp().run()
