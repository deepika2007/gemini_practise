from google import genai 
from dotenv import load_dotenv
import os

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY is not set in the environment variables.")

client = genai.Client(api_key=GEMINI_API_KEY)

# store chats 
history=[]

system_prompt = """You are a helpful Full stack lead that provides information about the tech related questions."""

while True:
    user_input = input("User: ")
    if user_input.lower() in ["exit", "quit", "bye"]:
        print("Exiting the chat.")
        break

    # Append user input to history
    history.append(f"=====================>User: {user_input}")

    conversation_context = system_prompt + "\n" 
    conversation_context +="\n".join(history)

    try:
        # Generate response using the chat model
        response = client.models.generate_content(
            model='gemini-3.6-flash',
            contents= conversation_context
        )

        # Extract the assistant's reply
        assistant_reply = response.text
        print(f"------------------>Assistant: {assistant_reply}")

        # Append assistant's reply to history
        history.append(f"Assistant: {assistant_reply}")

    except Exception as e:
        print(f"An error occurred: {e}")
