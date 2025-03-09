from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty
from kivy.lang import Builder
from kivy.animation import Animation
from kivy.core.window import Window
from kivy.graphics import Rectangle, Color
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.clock import Clock

from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen

from components.music_service import suggest_music
from components.DeezerPlayer import DeezerPlayer

import requests

# กำหนดให้แอปไม่แสดงผลแบบเต็มจอ
Window.fullscreen = False


class MoodTracker:
    """
    คลาสสำหรับติดตามและจัดการข้อมูลอารมณ์ของผู้ใช้
    """

    def __init__(self):
        # รายการเก็บอารมณ์ที่ผู้ใช้เลือก
        self.moods = []
        # รายการเก็บคำอธิบายอารมณ์ที่ผู้ใช้ป้อน
        self.descriptions = []
        self.all = None

    def track_mood(self, mood: str):
        """
        บันทึกอารมณ์ที่ผู้ใช้เลือก

        Args:
            mood (str): อารมณ์ที่ได้รับจากการเลือก emoji
        """
        self.moods.append(mood)
        print(f"Your Mood : {mood}")

    def track_text(self, text: str):
        """
        บันทึกคำอธิบายอารมณ์ที่ผู้ใช้ป้อน

        Args:
            text (str): ข้อความอธิบายอารมณ์
        """
        self.descriptions.append(text)
        print(f"Your Shortly describe your emotions : {self.moods}")

    def get_mood_data(self):
        """
        คืนค่าคู่ของอารมณ์และคำอธิบาย

        Returns:
            list: รายการของคู่ (อารมณ์, คำอธิบาย)
        """
        return list(zip(self.moods, self.descriptions))


def split_text(text):
    """
    แยกข้อความเพลงเป็นชื่อเพลงและชื่อศิลปิน

    Args:
        text (str): ข้อความที่ประกอบด้วยชื่อเพลงและศิลปิน (รูปแบบ "ชื่อเพลง by ชื่อศิลปิน")

    Returns:
        tuple: (ชื่อเพลง, ชื่อศิลปิน)
    """
    # ลบเครื่องหมายคำพูด (") และตัดช่องว่างที่ส่วนเกินออกจากข้อความ
    text = text.replace('"', "").strip()
    parts = text.split(" by ")

    # หากมีการแยกข้อความสำเร็จเป็น 2 ส่วน จะคืนค่าชื่อเพลงและศิลปิน
    if len(parts) >= 2:
        return parts[0], parts[1]

    # หากไม่สามารถแยกได้ จะคืนค่าข้อความเดิมและ "Unknown Artist"
    return text, "Unknown Artist"


class MoodSelect(BoxLayout):
    """
    หน้า UI หลักสำหรับเลือกอารมณ์และแสดงคำแนะนำเพลง
    """

    # สร้างการอ้างอิงไปยัง widget ที่มี id เป็น text_input
    text_input = ObjectProperty(None)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # สร้าง instance ของ MoodTracker เพื่อติดตามอารมณ์
        self.tracker = MoodTracker()
        # สร้าง instance ของ DeezerPlayer เพื่อเล่นเพลง
        self.player = DeezerPlayer()
        # ตัวแปรเก็บสถานะการเล่นเพลง
        self.is_playing = False
        # เวลาเริ่มต้นการเล่นเพลง
        self.start_time = 0
        # ตัวแปรเก็บ event ของ Clock สำหรับอัพเดท progress bar
        self.progress_event = None

        # รายการภาพพื้นหลังที่สามารถสลับได้
        self.background_images = [
            "Images/background.png",
            "Images/background20.jpg",
            "Images/background21.png",
            "Images/background22.jpg",
            "Images/background23.png",
            "Images/background24.png",
            "Images/background25.jpg",
            "Images/background26.png",
            "Images/background27.png",
            "Images/background28.png",
            "Images/background29.jpg",
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
        # ดัชนีของภาพพื้นหลังปัจจุบัน
        self.current_background_index = 0

        # กำหนดภาพพื้นหลังเริ่มต้น
        with self.canvas.before:
            # กำหนดสีพื้นหลังเริ่มต้น (สีขาว)
            self.bg_color = Color(1, 1, 1, 1)
            # สร้างสี่เหลี่ยมที่มีภาพพื้นหลัง
            self.bg_rect = Rectangle(
                source=self.background_images[self.current_background_index], size=self.size, pos=self.pos
            )

    def on_size(self, *args):
        """
        อัพเดทขนาดและตำแหน่งของพื้นหลังเมื่อขนาดหน้าจอเปลี่ยน
        """
        self.bg_rect.size = self.size
        self.bg_rect.pos = self.pos

    def emoji_select(self, mood, button):
        """
        จัดการการเลือก emoji ของอารมณ์

        Args:
            mood (str): อารมณ์ที่เลือก
            button: ปุ่ม emoji ที่ถูกกด
        """
        # สร้าง animation เมื่อปุ่มถูกกด (ขยายแล้วหดกลับ)
        anim = Animation(size=(90, 90), duration=0.1, t="out_quad") + Animation(
            size=(80, 80), duration=0.1, t="out_quad"
        )
        # เริ่ม animation บนปุ่มที่ถูกกด
        anim.start(button)
        # บันทึกอารมณ์ที่เลือก
        self.tracker.track_mood(mood)

    def submit_mood(self, *args):
        """
        จัดการการส่งข้อมูลอารมณ์และคำอธิบาย
        """
        # ดึงข้อความจาก text input
        text = self.text_input.text
        if text:
            # บันทึกคำอธิบายอารมณ์
            self.tracker.track_text(text)
            # ขอคำแนะนำเพลงตามอารมณ์
            self.get_music_recommendation()

    def get_music_recommendation(self):
        """
        ขอคำแนะนำเพลงตามอารมณ์ที่บันทึกไว้และเล่นเพลงนั้น
        """
        # ดึงข้อมูลอารมณ์ทั้งหมด
        mood_data = self.tracker.get_mood_data()
        if mood_data:
            try:
                # ขอคำแนะนำเพลงจาก music service
                response = suggest_music(mood_data[0])
                # แยกชื่อเพลงและชื่อศิลปิน
                track, artist = split_text(response)
                # แสดงชื่อเพลงและศิลปินบนหน้าจอ
                self.ids.track_name_label.text = f"{track}\nby {artist}"
                # เล่นเพลงตัวอย่างและเริ่ม progress bar เมื่อเพลงเริ่มเล่น
                self.player.play_preview(None, track, artist, on_play=lambda x: self.start_progress())
                # แสดงภาพแผ่นเสียง
                self.show_disk_animation(True)
                # ล้างข้อความใน text input
                self.text_input.text = ""
                # กำหนดสถานะการเล่นเพลงเป็น True
                self.is_playing = True
            except Exception as e:
                print(f"Error suggesting music: {e}")

    def change_background(self):
        """
        เปลี่ยนภาพพื้นหลังไปยังภาพถัดไปในรายการ
        """
        # เพิ่มดัชนีและวนกลับเมื่อถึงท้ายรายการ
        self.current_background_index = (self.current_background_index + 1) % len(self.background_images)
        # ดึงพาธของภาพพื้นหลังใหม่
        image_path = self.background_images[self.current_background_index]
        # เปลี่ยนภาพพื้นหลังใน Canvas
        self.bg_rect.source = image_path

    def show_disk_animation(self, show=True):
        """
        ควบคุมการแสดงภาพแผ่นเสียง (disk.gif)

        Args:
            show (bool): True เพื่อแสดง, False เพื่อซ่อน
        """
        # ตรวจสอบว่ามี widget ที่มี id เป็น "disk_image" หรือไม่
        if hasattr(self.ids, "disk_image"):
            # กำหนดความโปร่งใส (1 = แสดง, 0 = ซ่อน)
            self.ids.disk_image.opacity = 1 if show else 0

        # ล้างชื่อเพลงและศิลปินเมื่อซ่อนแผ่นเสียง
        if not show and hasattr(self.ids, "track_name_label"):
            self.ids.track_name_label.text = "Let's start your day with some great music!"

    def exit_app(self):
        """
        ออกจากแอปพลิเคชัน
        """
        App.get_running_app().stop()

    def start_progress(self):
        """
        เริ่มการอัพเดท progress bar สำหรับการเล่นเพลง
        """
        # รีเซ็ต progress bar
        self.ids.progress_bar.value = 0
        # รีเซ็ตเวลาที่แสดง
        self.ids.time_label.text = "0:00 / 0:30"
        # บันทึกเวลาเริ่มต้น
        self.start_time = Clock.get_time()

        # ยกเลิก event เดิม (ถ้ามี)
        if hasattr(self, "progress_event") and self.progress_event:
            Clock.unschedule(self.progress_event)
        # กำหนดให้ update_progress ทำงานทุก 0.1 วินาที
        self.progress_event = Clock.schedule_interval(self.update_progress, 0.1)

    def update_progress(self, dt):
        """
        อัพเดท progress bar และเวลาที่แสดง

        Args:
            dt: เวลาที่ผ่านไปจากการเรียกครั้งล่าสุด (ส่งโดย Clock)
        """
        # คำนวณเวลาที่ผ่านไป
        elapsed = Clock.get_time() - self.start_time
        # ถ้าเวลาไม่เกิน 30 วินาที (ความยาวของเพลงตัวอย่าง)
        if elapsed <= 30:
            # อัพเดทค่า progress bar
            self.ids.progress_bar.value = elapsed

            # แปลงเวลาเป็นรูปแบบ นาที:วินาที
            elapsed_min = int(elapsed) // 60
            elapsed_sec = int(elapsed) % 60
            # อัพเดทข้อความแสดงเวลา
            self.ids.time_label.text = f"{elapsed_min}:{elapsed_sec:02d} / 0:30"
        else:
            # รีเซ็ต progress bar เมื่อเพลงจบ
            self.reset_progress_bar()

    def reset_progress_bar(self):
        """
        รีเซ็ต progress bar และข้อความแสดงเวลา
        """
        # รีเซ็ตค่า progress bar เป็น 0
        self.ids.progress_bar.value = 0
        # รีเซ็ตข้อความแสดงเวลา
        self.ids.time_label.text = "0:00 / 0:30"

        # ยกเลิกการทำงานของ Clock event
        if hasattr(self, "progress_event") and self.progress_event:
            Clock.unschedule(self.progress_event)
            self.progress_event = None


class MoodTrackerApp(MDApp):
    """
    คลาสหลักของแอปพลิเคชัน MoodTracker
    """

    def build(self):
        """
        สร้าง UI หลัก

        Returns:
            MoodSelect: อินสแตนซ์ของหน้า UI หลัก
        """
        return MoodSelect()

    def stop_app(self):
        """
        หยุดการทำงานของแอปพลิเคชัน
        """
        self.stop()

    def on_request_close(self, *args):
        """
        จัดการเหตุการณ์เมื่อมีการร้องขอให้ปิดแอปพลิเคชัน

        Returns:
            bool: True เพื่อยอมรับการปิด
        """
        self.stop()
        return True


# จุดเริ่มต้นของแอปพลิเคชัน
if __name__ == "__main__":
    MoodTrackerApp().run()
