# Step 1: Import the 'requests' library we installed yesterday.
# This gives us the tools to talk to APIs.
import requests

# Step 2: Define the API's address (the "waiter's" location).
# This specific URL gives us a random cat fact.
api_url = "https://catfact.ninja/fact"

print("Contacting the API...")

# Step 3: Make the API call.
# We use requests.get() to ask the waiter for the data.
# The server's entire response is stored in the 'response' variable.
response = requests.get(api_url)

print("Response received!")

# Step 4: Parse the JSON data.
# The server sends data in JSON format. The .json() method
# turns that raw text into a Python dictionary we can easily use.
data = response.json()

# Step 5: Extract the specific piece of data we want.
# Looking at the JSON example above, the fact is stored
# under the key "fact".
fact = data['fact']

# Step 6: Print the final result in a friendly format.
print("------------------------------------")
print(f"Here is a random cat fact: {fact}")
print("------------------------------------")