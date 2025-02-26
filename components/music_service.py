from openai import OpenAI
from config import get_deepseek_key
import os
key = get_deepseek_key()
client = OpenAI(api_key=key, base_url="https://api.deepseek.com")
def suggest_music(mood_and_text):
    prompt = f"""
    คุณเป็นผู้ช่วยแนะนำเพลงไทยให้เหมาะสมกับอารมณ์ของผู้ใช้
    โดยเพลงที่แนะนำต้องเป็นเพลงไทยที่ตรงกับอารมณ์ '{mood_and_text[0]}' และเนื้อหาของข้อความ: "{mood_and_text[1]}"
    ตอบแค่ชื่อเพลง 1 เพลงเท่านั้น โดยไม่ต้องอธิบายหรือให้คำตอบเพิ่มเติม
    """
    print(prompt)
    response = client.chat.completions.create(
    model="deepseek-chat",
    messages=[
        # {"role": "system", "content": "You are a helpful assistant"},
        {"role": "user", "content": prompt},
    ],
    stream=False
    )
    recommended_song = response.choices[0].message.content
    return recommended_song
