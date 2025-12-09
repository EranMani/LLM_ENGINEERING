from nicegui import ui, run
from openai import AsyncOpenAI
import os
from dotenv import load_dotenv
import random

load_dotenv()
gemini_url = "https://generativelanguage.googleapis.com/v1beta/openai/"
google_key = os.getenv("GOOGLE_API_KEY")

if not google_key:
    print("There is an issue!")

client = AsyncOpenAI(base_url=gemini_url, api_key=google_key)

RANDOM_PROMPTS = [
    "Tell me a fun fact about space.",
    "Write a haiku about a coding bug.",
    "Explain quantum physics to a 5-year-old.",
    "Roast my choice of using Python for everything.",
    "Give me a motivation quote from a pirate captain.",
    "What is the capital of Mars? (Be creative)",
]

@ui.page('/')
def main():
    with ui.column().classes("w-full min-h-screen items-center justify-center bg-slate-100"):
        with ui.card().classes('w-full max-w-lg p-6 shadow-lg items-center text-center gap-4'):
            ui.label("🎲 Gemini Randomizer").classes("text-2xl font-bold text-slate-800")

            btn = ui.button("Surprise Me!").props('icon=casino color=purple')

            ui.separator()

            with ui.scroll_area().classes("w-full h-40 bg-white rounded border p-4"):
                result_area = ui.markdown("Press the button to get a random response")

    async def generate_random_response():
        prompt = random.choice(RANDOM_PROMPTS)

        result_area.content = f"**❓ Question:** *{prompt}*\n\n---\n\n**🤖 Gemini:** Thinking..."
        btn.disable()

        try:
            response = await client.chat.completions.create(
                    model="gemini-2.5-pro",
                    messages=[{"role": "user", "content": prompt}]
                )

            answer = response.choices[0].message.content
            result_area.content = f"**❓ Question:** *{prompt}*\n\n---\n\n**🤖 Gemini:**\n\n{answer}"
        except Exception as e:
            ui.notify(f"Error: {str(e)}", type="negative")
            result_area.content += f"\n\n❌ Error: {str(e)}"

        finally:
            btn.enable()

    btn.on_click(generate_random_response)


ui.run(port=8081)
