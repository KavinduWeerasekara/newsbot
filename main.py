# main.py

import os
import openai
from dotenv import load_dotenv
import pydantic # Import pydantic
import instructor # <-- 1. Import instructor

load_dotenv()

# Step 1: Define our Pydantic data schema.
# This is our "form" with the required fields.
# We are telling Pydantic that 'name' must be a string, 'age' must be an
# integer, and 'color' must be a string.

class Cat(pydantic.BaseModel):
    name: str
    age: int
    color: str

# Use the instructor client which is patched by Pydantic
# This adds the 'response_model' parameter to the create call 

client = instructor.patch(openai.OpenAI(api_key = os.getenv("OPENAI_API_KEY")))

print("Asking the AI for structured data about a cat...")

try:
    # Step 2: Use the 'response_model' parameter.
    # We tell the API call to format its response according to our Cat schema.

    cat_response = client.chat.completions.create(
        model = "gpt-3.5-turbo",
        response_model = Cat, # This is the magic line
        messages = [
            {"role": "user", "content": "Generate data for a cat named Mittens"}
        ]
    )

    # Step 3: Work with the validated data.
    # The response is now a Pydantic object, not just a dictionary.
    # We can access the data like attributes.

    print("________________________________________")
    print("Succussfully received and validated cat data")
    print(f"Name: {cat_response.name}")
    print(f"Age: {cat_response.age}")
    print(f"Color: {cat_response.color}")
    print("________________________________________")

except Exception as e:
    print(f"An error occurred: {e}")