from dotenv import load_dotenv
import os

load_dotenv()

def get_deepseek_key():
    return os.getenv("DEEPSEEK_API_KEY")
