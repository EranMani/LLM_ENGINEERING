from nicegui import ui, run
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

# Create the ollama client
client = OpenAI(
    base_url="http://localhost:11434/v1",
    api_key="ollama"
)


class TranslatorLogic:
    """
    This class will handle the translation logic by sending the request to the local model
    """
    def __init__(self):
        pass

    def build_messages(self, text, target_lang):
        """Constructs the translation prompt."""
        system_prompt = (
            f"You are a professional translator. Translate the user's text into {target_lang}."
            "Output ONLY the translated text. Do not add explanations or quotes."
        )

        return [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": text}
        ]
    
    async def translate(self, text, target_lang, model_name):
        """Sends the request to the local ollama instance"""

        messages = self.build_messages(text, target_lang)

        response = await run.io_bound(
            lambda: client.chat.completions.create(
                model=model_name,
                messages=messages,
                temperature=0.3 # low temp = more accurate translation
            )
        )

        return response.choices[0].message.content
    

class TranslatorApp:
    """
    This class will create the main UI and connect the logic to elements
    """
    def __init__(self):
        self.logic = TranslatorLogic()

        self.languages = ["Spanish", "French", "German", "Japanese", "Hebrew", "Portuguese"]
        self.modles = ["llama3.2", "deepseek-r1:1.5b"]

    def create_layout(self):
        with ui.column().classes("w-full min-h-screen bg-slate-100 items-center justify-center p-4"):
            with ui.card().classes("w-full max-w-lg shadow-xl p-0 gap-0"):
                with ui.row().classes("w-full bg-blue-600 p-4 items-center justify-center"):
                    ui.icon("translate", color="white", size="md")
                    ui.label("Local AI Translator").classes("text-white text-xl font-bold")

                with ui.column().classes("w-full p-6 gap-4"):
                    ui.label("Enter text to translate:")
                    self.input_text = ui.textarea(placeholder="Type something here...")\
                        .classes("w-full").props("outlined rounded")
                    
                with ui.row().classes("w-full gap-4"):
                    self.lang_select = ui.select(self.languages, value="Japanese", label="Target Language")\
                        .classes("w-1/2")
                    
                    self.model_select = ui.select(self.modles, value="llama3.2", label="Model")\
                        .classes("w-1/2")
                    
                self.translate_btn = ui.button("Translate", icon="language").classes("w-full bg-blue-600")

                ui.separator()

                ui.label("Translation:")
                with ui.scroll_area().classes("w-full h-32 bg-slate-50 border rounded p-3"):
                    self.output_text = ui.markdown("Result will appear here..")

    async def run_translation(self):
        """Fetch the user selections and display the generated translate result"""
        text = self.input_text.value
        target = self.lang_select.value
        model = self.model_select.value

        if not text:
            ui.notify("Please enter text!", type="warning")
            return
        
        self.output_text.content = "⏳ *Translating...*"
        self.translate_btn.disable()
        spinner = ui.spinner(size="lg").classes("self-center")

        try:
            result = await self.logic.translate(text, target, model)

            self.output_text.content = result

        except Exception as e:
            self.output_text.content = f"❌ **Error:** {str(e)}"
            ui.notify("Ensure Ollama is running!", type='negative')

        finally:
            spinner.delete()
            self.translate_btn.enable()


@ui.page('/')
def main():
    app = TranslatorApp()
    app.create_layout()
    app.translate_btn.on_click(app.run_translation)

ui.run(port=8083)
        