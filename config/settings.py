import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Environment variables
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
SERVER_URL = os.getenv("SERVER_URL")
SESSION_COOKIE = os.getenv("SESSION_COOKIE")

if not OPENAI_API_KEY or not SERVER_URL or not SESSION_COOKIE:
    raise ValueError("Missing required environment variables in .env file")
