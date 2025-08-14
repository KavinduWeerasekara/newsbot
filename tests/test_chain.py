# tests/test_chain.py
from app.chain import chain # Import the chain we want to test

# A test function must start with the word 'test_'

def test_chain_invococation():
    # 1. Arrange: Set up our input
    topic = "a happy dog"

    # 2. Act: Run the code we are testing
    result = chain.invoke({"topic": topic})

    # 3. Assert: Check if the result is what we expect
    # The 'assert' keyword is the heart of a test.
    # If the condition is true, the test passes. If false, it fails. 

    assert isinstance(result, str) # Is the result a string?
    assert len(result) > 5 # Is the string reasonably long?
    assert "dog" in result.lower() # Does the string contain 'dog'?
