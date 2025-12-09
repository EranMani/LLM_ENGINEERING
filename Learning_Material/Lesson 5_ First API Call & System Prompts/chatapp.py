from nicegui import ui, run
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()
# Load API key
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


class ChatApp:
    """
    This class handles the call to the api, create and update the layout
    """
    def __init__(self):
        # Init the token tracker class
        self.token_tracker = TokenTracker()

    def create_layout(self):
        """
        Define the UI layout structure
        """
        with ui.column().classes("w-full min-h-screen bg-slate-50 items-center justify-center"):

            # CHANGE 1: I changed h-[80vh] to h-[600px] for a better fixed size
            with ui.card().classes("w-full max-w-2xl h-[600px] flex flex-col p-0 shadow-xl"):
                
                # --- Header ---
                with ui.column().classes("w-full bg-slate-100 border-b p-4 gap-2"):
                    ui.label(text="Token Tracker Chat")

                    with ui.row().classes("w-full justify-between items-center"):
                        self.cost_label = ui.label(text="$0.00000").classes("text-sm font-mono text-slate-600")
                        self.token_progress_bar = ui.linear_progress(value=0).classes("w-90 h-5 rounded").style("background-color: grey;")
                        self.token_progress_bar.props("color=green track-color=grey-3")
                        ui.label(text=f"max budget: {self.token_tracker.budget_limit}").classes("text-sm font-mono text-slate-600")

                # --- Chat Area ---
                # CRITICAL FIX: This block is now indented to be INSIDE the card
                with ui.scroll_area().classes("flex-grow w-full p-4 bg-white") as self.message_container:
                    ui.label(text="Start Chatting!").classes("text-gray-400 italic self-center")

                # --- Footer ---
                # CRITICAL FIX: This block is also indented to be INSIDE the card
                with ui.row().classes("w-full p-4 bg-slate-50 border-t items-center"):
                    self.chat_input = ui.input(placeholder="Type Here..")\
                        .classes("flex-grow")\
                        .props("rounded outlined dense bg-white") \
                        .on("keydown.enter", self.send_message)

    async def send_message(self):
        user_text = self.chat_input.value

        if not user_text:
            return

        # Clear chat content
        self.chat_input.value = ''

        with self.message_container:
            ui.chat_message(text=user_text, name="You", sent=True)

        spinner = ui.spinner(size='lg')

        try:
            # io bound takes that blocking function and moves it to a background thread
            # await pauses only the specific chat function, letting the rest of the UI stay alive
            response = await run.io_bound(
                lambda: client.chat.completions.create(model="gpt-4o-mini",
                                                      messages=[{"role": "user", "content": user_text}])
            )
            
            content = response.choices[0].message.content
            usage_object = response.usage
            
            with self.message_container:
                ui.chat_message(text=content, name="Bot", sent=False)

            

            await self.token_tracker.update(usage_object)
            self.update_ui()

            self.message_container.scroll_to(percent=1.0)

        except Exception as e:
            ui.notify(f"Error: {str(e)}", type="negative")

        finally:
            spinner.delete()

    def update_ui(self):
        token_data = self.token_tracker.get_token_data()

        self.token_progress_bar.value = token_data["token_progress"]
        self.cost_label.set_text(f"${token_data["total_cost"]:.6f}")


class TokenTracker:
    """
    This class will handle the API call, create and update process of the UI
    """
    def __init__(self):
        # track total tokens use
        self.token_count = 0

        # track accumulated money spent
        self.total_cost = 0.0

        # track the token progress according to max budget
        self.token_progress = 0

        # Set a progress limit
        self.budget_limit = 5000

    async def update(self, usage_object):
        """
        Use usage object to get data about tokens and update the relevant variables
        """
        self.token_count += usage_object.total_tokens
        self.total_cost += (usage_object.total_tokens / 1_000_000) * 0.60
        self.token_progress = min(self.token_count / self.budget_limit, 1.0)
        
    def get_token_data(self):
        return {"token_count": self.token_count,
                "total_cost": self.total_cost,
                "token_progress": self.token_progress}

    

@ui.page("/")
def main():
    app = ChatApp()
    app.create_layout()
    
ui.run(port=8080)