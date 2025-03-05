from openai import OpenAI
from config import get_deepseek_key
import os

key = get_deepseek_key()
client = OpenAI(api_key=key, base_url="https://api.deepseek.com")


def suggest_music(mood_and_text):
    prompt = f"""
You are an assistant that recommends international songs based on the user's mood and text.
Please suggest a well-known **English song released in 2010 or later** that matches the mood '{mood_and_text[0]}' and is relevant to the following text: "{mood_and_text[1]}". 
Only respond with the title of **one real song** that actually exists, without any additional explanation or information.
Make sure the song is popular and officially released after 2010.
"""

    print(prompt)
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            # {"role": "system", "content": "You are a helpful assistant"},
            {"role": "user", "content": prompt},
        ],
        stream=False,
    )
    recommended_song = response.choices[0].message.content
    return recommended_song
