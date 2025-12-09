import os
from dotenv import load_dotenv
from openai import OpenAI

# 1. Load the openai api key
load_dotenv(override=True)
api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    print("Error! No API key found!")
else:
    print("API key found! you may continue!")

# 2. Initialize the openapi client
client = OpenAI(api_key=api_key)

# Define the conversation
messages = [
    {
        "role": "user",
        "content": "explain about gen ai in two sentences"
    }
]

print("Sending request to openai...")

# 3. Make the API call
response = client.chat.completions.create(model="gpt-5-nano", messages=messages)

# 4. Get the output message
client_message = response.choices[0].message.content
print(client_message)

# 5. Print the cost of this call
print(response.usage)

