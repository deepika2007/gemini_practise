from google import genai 
from dotenv import load_dotenv
import os
import time
from datetime import datetime
import random

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY is not set in the environment variables.")

client = genai.Client(api_key=GEMINI_API_KEY)

# store chats 
history=[]
MAX_HISTORY= 20

system_prompt = """You are a helpful Full stack lead that provides information about the tech related questions."""

print("=" * 50)

def get_current_time():
    return datetime.now().strftime('%I:%M:%S')

def motivation():
    quotes=["i can do", "i have to do", "i will do", "i did it"]
    return random.choice(quotes)


def route_tool(query):
    query = query.lower()

    if "time" in query:
        return "time"
    elif "motivation" in query or "quote" in query:
        return "quote"

    return "gemini"

while True:
    user_input = input("User: ")
    if user_input.lower() in ["exit", "quit", "bye"]:
        print("Exiting the chat.")
        break

    tool = route_tool(user_input)
    if tool =="time":
        result = get_current_time()
        print(f'Assitant: Current time {result}')
    elif tool=='quote':
        result = motivation()
        print(f"Assitant: Quote: {result}")

    else:
        response = client.models.generate_content(
            model='gemini-3.6-flash',
            contents= user_input
        )
        print(f"Assitant: GEMINI: {response.text}")

