from dotenv import load_dotenv
import os

load_dotenv()


# def get_openai_key():
#     return os.getenv('OPENAI_API_KEY')
def get_deepseek_key():
    return os.getenv("DEEPSEEK_API_KEY")
