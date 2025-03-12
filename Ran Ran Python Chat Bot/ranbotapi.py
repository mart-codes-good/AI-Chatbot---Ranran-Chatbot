import openai
import os
from dotenv import load_dotenv

load_dotenv()  # Load .env file

openai.api_key = os.getenv("OPENAI_API_KEY")
# Create a chat completion request

ranranbot = ranranbot = os.getenv("RANRANBOT")

def get_llm_response(user_input):

    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",  # or "gpt-4o-mini" if that’s the variant you’re using
        messages=[
            {"role": "system", "content": ranranbot},  # Optional system message
            {"role": "user", "content": user_input}
        ],
        max_tokens=50  # Limit the response length
    )

    # Print the response
    return response['choices'][0]['message']['content'].strip()

