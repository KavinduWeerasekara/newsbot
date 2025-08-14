# main.py

import os
import openai
from dotenv import load_dotenv
import pydantic # Import pydantic
import instructor # <-- 1. Import instructor
import logging # Import the logging library
from tenacity import retry, stop_after_attempt, wait_fixed # Import tenacity

# --- Setup ---

load_dotenv()

# Step 1: Configure the logger
# This sets up a basic logbook that prints messages to your terminal.

logging.basicConfig(
    level = logging.INFO, # Set the minimum level of messages to show
    format = "%(asctime)s - %(levelname)s - %(message)s" # Set the format of the log messages
)

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


# Step 2: Add the retry "decorator"
# A decorator (@) is like a hat you put on a function to give it extra powers.
# This one tells the function to retry 3 times, waiting 2 seconds between attempts if it fails.

@retry(wait=wait_fixed(2), stop=stop_after_attempt(3))
def create_cat_completion() -> Cat:

    """Creates a cat completion and handles retries."""

    logging.info("attempting to call openai API...")

    cat_response = client.chat.completions.create(
            model = "gpt-3.5-turbo",
            response_model = Cat, # This is the magic line
            messages = [
                {"role": "user", "content": "Generate data for a cat named Mittens"}
            ]
        )
    logging.info("Successfully received and validated data.")

    return cat_response
    
def main():
    try:
        # Step 2: Use the 'response_model' parameter.
        # We tell the API call to format its response according to our Cat schema.

        # Step 3: Call our new, robust function
        final_cat = create_cat_completion()

        
        # Step 3: Work with the validated data.
        # The response is now a Pydantic object, not just a dictionary.
        # We can access the data like attributes.

        print("________________________________________")
        print("Succussfully received and validated cat data")
        print(f"Name: {final_cat.name}")
        print(f"Age: {final_cat.age}")
        print(f"Color: {final_cat.color}")
        print("________________________________________")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()