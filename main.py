from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty
from components.music_service import suggest_music
from components.DeezerPlayer import DeezerPlayer
from kivymd.app import MDApp
from kivy.lang import Builder
from kivymd.uix.screen import MDScreen
from kivy.animation import Animation
from kivy.core.window import Window
from kivy.graphics import Rectangle, Color
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.clock import Clock

import requests

Window.fullscreen = False


class MoodSelect(BoxLayout):
    """UI หลักของหน้าเลือกอารมณ์"""

    text_input = ObjectProperty(None)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.tracker = MoodTracker()
        self.player = DeezerPlayer()
        self.is_playing = False
        self.start_time = 0
        self.progress_event = None  # Store the Clock event for progress updates

        # เพิ่มดติมการเปลี่ยน Background
        self.background_images = [
            "Images/background.png",
            "Images/background1.png",
            "Images/background2.jpg",
            "Images/background3.jpg",
            "Images/background4.png",
            "Images/background5.jpg",
            "Images/background6.jpg",
            "Images/background7.jpg",
            "Images/background8.jpg",
            "Images/background9.png",
            "Images/background10.png",
            "Images/background11.png",
            "Images/background12.png",
            "Images/background13.png",
            "Images/background14.png",
            "Images/background15.png",
            "Images/background16.png",
            "Images/background17.png",
            "Images/background18.png",
            "Images/background19.png",
        ]
        self.current_background_index = 0
        with self.canvas.before:
            self.bg_color = Color(1, 1, 1, 1)  # กำหนดสีพื้นหลังเริ่มต้น
            self.bg_rect = Rectangle(
                source=self.background_images[self.current_background_index], size=self.size, pos=self.pos
            )

    def on_size(self, *args):
        self.bg_rect.size = self.size
        self.bg_rect.pos = self.pos

    def change_background(self):
        self.current_background_index = (self.current_background_index + 1) % len(self.background_images)
        self.bg_rect.source = self.background_images[self.current_background_index]

    def emoji_select(self, mood, button):
        """ส่วนไว้รับการเลือก emoji"""
        # ทำ animation เวลาปุ่มถูกเลือก
        anim = Animation(size=(90, 90), duration=0.1, t="out_quad") + Animation(
            size=(80, 80), duration=0.1, t="out_quad"
        )
        anim.start(button)
        self.tracker.track_mood(mood)

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
                self.ids.track_name_label.text = f"{track}\nby {artist}"
                # Pass the callback to start_progress when the sound plays
                self.player.play_preview(None, track, artist, on_play=lambda x: self.start_progress())
                self.show_disk_animation(True)
                self.text_input.text = ""
                self.is_playing = True
            except Exception as e:
                print(f"Error suggesting music: {e}")

    def change_background(self):
        self.current_background_index = (self.current_background_index + 1) % len(self.background_images)
        image_path = self.background_images[self.current_background_index]

        # เปลี่ยนภาพพื้นหลังใน Canvas
        self.bg_rect.source = image_path

    def show_disk_animation(self, show=True):
        # ควบคุมการแสดง แผ่นเพลง(disk.gif)
        if hasattr(self.ids, "disk_image"):  # ตรวจสอบว่า self.ids มี widget ที่มี id ชื่อว่า "disk_image" อยู่หรือไม่
            # หาก show เป็น True -> แสดงแผ่นเพลง (opacity = 1)
            # หาก show เป็น False -> ซ่อนแผ่นเพลง (opacity = 0)
            self.ids.disk_image.opacity = 1 if show else 0

        # ลบชื่อเพลงกับศิลปืนออกหลังเพลงหยุด
        if not show and hasattr(self.ids, "track_name_label"):
            self.ids.track_name_label.text = "Let's start your day with some great music!"

    def exit_app(self):
        App.get_running_app().stop()

    def start_progress(self):
        # Reset and start the progress bar
        self.ids.progress_bar.value = 0
        self.ids.time_label.text = "0:00 / 0:30"
        self.start_time = Clock.get_time()

        # Schedule updates 10 times per second
        if hasattr(self, "progress_event") and self.progress_event:
            Clock.unschedule(self.progress_event)
        self.progress_event = Clock.schedule_interval(self.update_progress, 0.1)

    def update_progress(self, dt):
        # Calculate elapsed time
        elapsed = Clock.get_time() - self.start_time
        if elapsed <= 30:  # 30 seconds is the maximum duration
            # Update progress bar
            self.ids.progress_bar.value = elapsed

            # Format time as minutes:seconds
            elapsed_min = int(elapsed) // 60
            elapsed_sec = int(elapsed) % 60
            self.ids.time_label.text = f"{elapsed_min}:{elapsed_sec:02d} / 0:30"
        else:
            self.reset_progress_bar()

    def reset_progress_bar(self):
        # Reset progress bar and time label
        self.ids.progress_bar.value = 0
        self.ids.time_label.text = "0:00 / 0:30"

        # Cancel the update schedule
        if hasattr(self, "progress_event") and self.progress_event:
            Clock.unschedule(self.progress_event)
            self.progress_event = None


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
    text = text.replace('"', "").strip()  # ลบเครื่องหมายคำพูด (") และตัดช่องว่างที่ส่วนเกินออกจากข้อความ
    parts = text.split(" by ")

    # หากมีการแยกข้อความสำเร็จเป็น 2 ส่วน จะคืนค่าชื่อเพลงและศิลปิน
    if len(parts) >= 2:
        return parts[0], parts[1]

    return text, "Unknown Artist"


class MoodTrackerApp(MDApp):
    def build(self):
        return MoodSelect()

    def stop_app(self):
        self.stop()

    def on_request_close(self, *args):
        self.stop()
        return True


if __name__ == "__main__":
    MoodTrackerApp().run()
