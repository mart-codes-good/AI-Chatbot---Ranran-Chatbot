import openai
import os
from dotenv import load_dotenv

load_dotenv()  # Load .env file

openai.api_key = os.getenv("OPENAI_API_KEY")
# Create a chat completion request

ranranbot = ranranbot = os.getenv("RANRANBOT")

# This list keeps track of user and bot responses
history = [{"role": "system", "content": ranranbot}]

def get_llm_response(user_input):

    history.append({"role": "user", "content": user_input})
    
    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",  # or "gpt-4o-mini" if that’s the variant you’re using
        messages=history,
        max_tokens=50  # Limit the response length
    )

    bot_response = response['choices'][0]['message']['content'].strip()
    history.append({"role": "system", "content": bot_response})

    # For terminal use (dev view)
    print(f"User: {user_input}")
    print(f"RanRan ChatBot: {bot_response}")

    # If more than 100 messages stored, clear list and add original chat bot prompt
    if len(history) > 100:
        history.clear()
        print("Memory Cleared!")
        history[:].append({"role": "system", "content": ranranbot})


    # Print the response
    return bot_response


