import ollama

MODEL = "qwen3"

# 1. Define the mode behaviour, in this case a portugese tutor
system_prompt = (
    "You are a playful European Portuguese tutor for an intermediate student. "
    "Speak mostly in Portuguese with a warm, fun, encouraging tone. "
    "Explain grammar creatively using simple analogies and real-life examples. "
    "Ask short follow-up questions that make the student use the target structure. "
    "Only translate to English for very hard idioms or vocabulary. "
    "When correcting, show the corrected sentence first, then explain the rule in simple Portuguese."
    "Sometimes invent short roleplay scenes (2 to 4 lines) "
    "set in everyday contexts like cafés, work, travel, or family life in Portugal. "
)

# 2. The user input
user_input = "Oi! Eu gostaria de praticar conversação. Você pode me ajudar com o subjuntivo?"

# 3. Build the message history
messages = [
    {"role": "system", "content": system_prompt},
    {"role": "user", "content": user_input}
]

print("The tutor is constructing his answer...")

stream = ollama.chat(
    model=MODEL,
    messages=messages,
    stream=True
)

print(f"The tutor has answered your question: {user_input}, With this:")

for chunk in stream:
    print(chunk["message"]["content"], end="", flush=True)
