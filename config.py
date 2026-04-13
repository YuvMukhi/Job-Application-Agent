import os
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

if not GEMINI_API_KEY or GEMINI_API_KEY == "your_gemini_key_here":
    raise ValueError("Please set a valid GEMINI_API_KEY in .env")

if not TAVILY_API_KEY or TAVILY_API_KEY == "your_tavily_key_here":
    raise ValueError("Please set a valid TAVILY_API_KEY in .env")

# Model settings
GEMINI_MODEL = "gemini-2.5-flash"  # Use Gemini Flash 2.5 for all LLM calls