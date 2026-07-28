from google import genai 
from dotenv import load_dotenv
import os
import time

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
while True:
    user_input = input("User: ")
    if user_input.lower() in ["exit", "quit", "bye"]:
        print("Exiting the chat.")
        break

    # Append user input to history
    history.append(f"User: {user_input}")

    if len(history) > MAX_HISTORY:
        history = history[-MAX_HISTORY:]

    conversation_context = system_prompt + "\n" 
    conversation_context +="\n".join(history)

    start_time= time.time()
    full_response=""
    try:
        # Generate response using the chat model
        stream = client.models.generate_content_stream(
            model='gemini-3.6-flash',
            contents= conversation_context
        )

        for chunk in stream:
            if chunk.text:
                full_response+= chunk.text
                print(chunk.text, end="", flush=True)

        end_time= time.time()
        total_time= round(end_time-start_time, 2)

        print(f"\n Response Time is {total_time} Seconds")


        # Extract the assistant's reply
        assistant_reply = full_response
        print("=" * 50)
        print(f"Assistant: {assistant_reply}")

        # Append assistant's reply to history
        history.append(f"Assistant: {assistant_reply}")

    except Exception as e:
        print(f"An error occurred: {e}")
