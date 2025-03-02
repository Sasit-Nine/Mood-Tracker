# how can i play preview song from spotify in python
# ถาม gpt ว่าok then how can i change to use deezer (ตอนแรกจะใช้ spotify แต่spotify หยุดให้ preview url)

import requests
import tempfile
import deezer
from kivy.core.audio import SoundLoader
from kivy.app import App
from kivy.uix.button import Button


class DeezerPlayer(App):

    def play_preview(self, instance, trackname, artistname):
        # Initialize Deezer client
        client = deezer.Client()
        print("track: ", trackname, "artistname: ", artistname)
        # Search for the track
        track_name = trackname
        artist_name = artistname
        search_results = client.search(track=track_name, artist=artist_name)

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
                    sound = SoundLoader.load(temp_file_path)
                    if sound:
                        sound.play()
                    else:
                        print("Failed to load the sound.")
                else:
                    print("Failed to download the preview.")
            else:
                print("No preview available for this track.")
        else:
            print("Track not found.")


if __name__ == "__main__":
    DeezerPlayer().run()
