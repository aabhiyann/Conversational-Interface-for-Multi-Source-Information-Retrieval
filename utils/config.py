import os
from dotenv import load_dotenv

def load_config():
    load_dotenv()

    OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
    if not OPENAI_API_KEY:
        raise ValueError("OPENAI_API_KEY environment variable is not set in the .env file.")

    return {"OPENAI_API_KEY": OPENAI_API_KEY}