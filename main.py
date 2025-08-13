# Step 1: Import our new tools.
# 'asyncio' is for running async code, 'httpx' is for async web requests.
import asyncio
import httpx

# The same API address as before.
api_url = "https://catfact.ninja/fact"

# Step 2: Define an 'async' function.
# The 'async def' tells Python this function can be paused
# and resumed while it's "waiting" for things like API calls.
async def get_cat_fact(client):
    # We 'await' the response. This is the "pause and wait" point.
    response = await client.get(api_url)
    data = response.json()
    return data['fact'] # Return just the fact text.

# This is our main function that will run the whole program.
async def main():
    print("Requesting 5 cat facts at the same time...")

    # Step 3: Create an async client.
    # 'async with' creates a client that can be reused for all our requests.
    async with httpx.AsyncClient() as client:
        # Step 4: Prepare all the tasks.
        # We create a list of "tasks" to run. Each task is a call
        # to our get_cat_fact function.
        tasks = [get_cat_fact(client) for _ in range(5)]

        # Step 5: Run all tasks concurrently.
        # 'asyncio.gather' is the magic that runs all the tasks in our
        # list at the same time and waits for them all to finish.
        facts = await asyncio.gather(*tasks)

    print("------------------------------------")
    # Loop through the list of facts we received and print each one.
    for i, fact in enumerate(facts, 1):
        print(f"Fact {i}: {fact}")
    print("------------------------------------")

# Step 6: Run our main async function.
# This is the line that kicks off the entire program.
if __name__ == "__main__":
    asyncio.run(main())