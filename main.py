from components.music_service import suggest_music
class MoodTracker:
    def __init__(self):
        self.moods = []
        self.text = []
        self.all = None
    def track_mood(self,mood: str):
        self.moods.append(mood)
        print(f'Your Mood : {mood}')
    def track_text(self,text: str):
        self.text.append(text)
        print(f'Your Shortly describe your emotions : {mood}')
    def show_moods(self):
        self.all = zip(self.moods,self.text)
        if self.all is None:
            print('Empty')
        else:
            return list(self.all)
            # print('Your Moods:')
            # for mood in self.all:
            #     print(f'- {mood}')
if __name__ == '__main__':
    input_status = True
    while input_status:
        tracker = MoodTracker()
        mood = input('Enter your mood : ')
        text = input('Enter Shortly describe your emotions : ')
        tracker.track_mood(mood)
        tracker.track_text(text)
        mood = tracker.show_moods()
        response = suggest_music(mood[0])
        print(response)
        ans = input('Do you want track again : (y/n)')
        if ans == 'y':
            input_status = True
        else:
            input_status = False
