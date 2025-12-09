from scraper import get_selenium_content
from openai import OpenAI, AsyncOpenAI
import os
from dotenv import load_dotenv
from nicegui import ui, run

load_dotenv()
client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class AIHandler:
    def __init__(self):
        pass

    def messages_for(self, website_text, tone="professional"):
        # Define the personalities
        personas = {
            "Professional": "You are a precise and formal research assistant. Provide a structured, objective summary.",
            "Pirate": "You are a 17th-century pirate captain. Summarize the text using heavy sea-slang, 'Argghs', and nautical metaphors.",
            "Snarky": "You are a sarcastic, cynical teenager. Summarize the text while making fun of it and rolling your eyes.",
            "5-Year-Old": "You are a kindergarten teacher explaining this to a 5-year-old. Use very simple words, short sentences, and emojis."
        }

        system_instruction = personas.get(tone, personas["Professional"])

        system_prompt = (
            f"{system_instruction} " 
            "Ignore navigation menus, ads, and cookies. Focus only on the main content."
        )
        
        user_prompt = (
            f"Here is the website text: \n\n{website_text}"
        )

        return [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]


class Summarizer:
    def __init__(self):
        self.ai_handler = AIHandler()

    def create_layout(self):
        with ui.column().classes("w-full min-h-screen bg-gray-100 items-center justify-center p-4"):
            with ui.card().classes("w-full max-w-3xl min-h-[700px] shadow-lg flex flex-col"):
                with ui.row().classes("w-full bg-slate-800 p-4 items-center gap-2"):
                    ui.icon("article", color="white", size="md")
                    ui.label("AI Web Summarizer").classes("text-white text-xl font-bold")

                with ui.column().classes("w-full items-center justfiy-center"):
                    with ui.row().classes("w-full items-center justify-center"):
                        self.url_input = ui.input(label="website url").classes("w-90")
                        self.tone_select = ui.select(options=["Professional", "Pirate", "Snarky", "5-Year-Old"]).classes("w-40")
                        self.summarize_button = ui.button(text="Summarize", on_click=self.run_summary)

                    ui.separator()

                    with ui.scroll_area().classes("min-h-[500px] flex-grow w-full p-4 border rounded bg-slate-500"):
                        self.result_area = ui.markdown().classes("w-full text-slate-700 leading-relaxed")

    async def run_summary(self):
        url = self.url_input.value
        tone = self.tone_select.value

        if not url:
            ui.notify("Please enter a URL!", type="warning")
            return
        
        self.result_area.content = ""
        spinner = ui.spinner(size="lg").classes("self-center")

        # Prevent double clicking
        self.summarize_button.disable()

        try:
            text = await run.io_bound(lambda: get_selenium_content(url))
            text = text [:2000]

            messages = self.ai_handler.messages_for(text, tone)

            spinner.delete()

            stream = await client.chat.completions.create(
                model="gpt-4o-mini",
                messages=messages,
                stream=True
            )

            async for chunk in stream:
                content = chunk.choices[0].delta.content
                if content:
                    self.result_area.content += content


        except Exception as e:
            ui.notify(f"Error: {str(e)}", type="negative")

        finally:
            try:
                spinner.delete()
            except:
                pass

            self.summarize_button.enable()

@ui.page('/')
def main():
    app = Summarizer()
    app.create_layout()



ui.run(port=8081)