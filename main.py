from config import get_openai_key

openai_key_api = get_openai_key()


class MoodTracker:
    def __init__(self):
        self.moods = []
        self.text = []
        self.all = []

    def track_mood(self, mood: str):
        self.moods.append(mood)
        print(f"Your Mood : {mood}")

    def track_text(self, text: str):
        self.text.append(text)
        print(f"Your Shortly describe your emotions : {mood}")

    def show_moods(self):
        self.all = zip(self.moods, self.text)
        if self.moods is None:
            print("Empty")
        else:
            print("Your Moods:")
            for mood in self.all:
                print(f"- {mood}")


if __name__ == "__main__":
    tracker = MoodTracker()
    input_status = True
    while input_status:
        mood = input("Enter your mood : ")
        text = input("Enter Shortly describe your emotions : ")
        tracker.track_mood(mood)
        tracker.track_text(text)
        tracker.show_moods()
        ans = input("Do you want track again : (y/n)")
        if ans == "y":
            input_status = True
        else:
            input_status = False
