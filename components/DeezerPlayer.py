# how can i play preview song from spotify in python
# ถาม gpt ว่าok then how can i change to use deezer (ตอนแรกจะใช้ spotify แต่spotify หยุดให้ preview url)

import requests
import tempfile
import deezer
from kivy.core.audio import SoundLoader
from kivy.app import App
from kivy.uix.button import Button
from kivy.clock import Clock


class DeezerPlayer:
    def __init__(self):
        self.sound = None
        self.on_play_callback = None

    def play_preview(self, instance, trackname, artistname, on_play=None):
        # Initialize Deezer client
        client = deezer.Client()
        print("track: ", trackname, "artistname: ", artistname)
        # Search for the track

        # Store callback for later use
        self.on_play_callback = on_play

        search_results = client.search(track=trackname, artist=artistname)

        if search_results:
            track = search_results[0]  # Get the first result
            preview_url = track.preview

            if preview_url:
                # Download the audio preview
                response = requests.get(preview_url)
                if response.status_code == 200:
                    # Create a temporary file to save the preview
                    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_file:
                        temp_file.write(response.content)
                        temp_file_path = temp_file.name

                    # Load and play the audio using Kivy's SoundLoader
                    self.sound = SoundLoader.load(temp_file_path)
                    if self.sound:
                        self.sound.bind(on_stop=self.on_sound_stop)
                        # Instead of binding on_play directly, use our own callback that will be called when sound actually starts
                        Clock.schedule_once(lambda dt: self.check_sound_playing(), 0.1)
                        self.sound.play()
                    else:
                        print("Failed to load the sound.")
                else:
                    print("Failed to download the preview.")
            else:
                print("No preview available for this track.")
        else:
            print("Track not found.")

    def on_sound_stop(self, sound):
        # เมื่อเพลงจบให้ซ่อน disk.gif
        from kivy.app import App

        app = App.get_running_app()
        if app and hasattr(app.root, "show_disk_animation"):
            # ต้องใช้ Clock เพราะอาจจะไม่ได้ทำงานบน main thread
            Clock.schedule_once(lambda dt: app.root.show_disk_animation(False), 0)
        if app and hasattr(app.root, "reset_progress_bar"):
            Clock.schedule_once(lambda dt: app.root.reset_progress_bar(), 0)

    def check_sound_playing(self):
        if self.sound and self.sound.state == "play":
            # Sound is actually playing now, call the on_play callback
            if self.on_play_callback:
                self.on_play_callback(self.sound)
        else:
            # Check again after a short delay
            Clock.schedule_once(lambda dt: self.check_sound_playing(), 0.1)


if __name__ == "__main__":
    DeezerPlayer().run()
