from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.core.window import Window
from kivymd.uix.picker import MDDatePicker
from kivy.uix.label import Label
from kivymd.uix.button import MDRaisedButton
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout

Window.size = (360, 640)

class MoodTrackerApp(MDApp):
    def build(self):
        return Builder.load_file("kivy_ui.kv")

if __name__ == "__main__":
    MoodTrackerApp().run()
