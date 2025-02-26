from openai import OpenAI
from config import get_deepseek_key
import os
key = get_deepseek_key()
client = OpenAI(api_key=key, base_url="https://api.deepseek.com")
def suggest_music(mood_and_text):
    print(mood_and_text[0],mood_and_text[1])
    prompt = f"แนะนำเพลงไทยจากโดยให้เหมาะกับความรู้สึก '{mood_and_text[0]}' และวิเคราะห์จากข้อความ: {mood_and_text[1]} ตอบแค่ชื่อเพลง 1 เพลง."
    response = client.chat.completions.create(
    model="deepseek-chat",
    messages=[
        # {"role": "system", "content": "You are a helpful assistant"},
        {"role": "user", "content": prompt},
    ],
    stream=False
    )
    recommended_song = response.choices[0].message['content']
    return recommended_song
