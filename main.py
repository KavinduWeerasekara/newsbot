# main.py
import os
import openai
from dotenv import load_dotenv

# Load variables from the .env file into the environment
load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    raise ValueError("OPENAI_API_KEY is not set")

client = openai.OpenAI(api_key=api_key)

print("Sending a prompt to openai API...")

try:
    response = client.chat.completions.create(
        model = "gpt-3.5-turbo",
        messages = [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Write a single, short sentence about a brave cat who saves the day."}
        ]
    )

    ai_response = response.choices[0].message.content

    print("_________________________________________________")
    print(f"AI Response: {ai_response}")
    print("_________________________________________________")

except Exception as e:
    print(f"An error occurred: {e}")