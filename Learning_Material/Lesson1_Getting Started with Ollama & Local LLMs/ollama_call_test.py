import ollama

MODEL = "qwen3"

# 1. Pull the model locally
print(f"Fetching model {MODEL}...")
ollama.pull(MODEL)

# 2. Define the prompt and message
user_prompt = "what is comfy ui? explain in two sentences."
message = [
    {
        "role": "user",
        "content": user_prompt
    }
]

# 3. Generate a response using the chat method
# response = ollama.chat(model=MODEL, messages=message)
stream = ollama.chat(model=MODEL, messages=message, stream=True)

# 4. Print the result
# Option 1: wait for the full text
# print(response["message"]["content"])

# Option 2: stream the text
for chunk in stream:
    print(chunk["message"]["content"], end="", flush=True)
