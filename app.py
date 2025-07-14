# app.py
"""
Launches the Gradio web interface for the AI Sidekick.

This script sets up the user interface, manages the application state for each
user session, and handles the interaction logic between the user and the
backend Sidekick agent.
"""
import asyncio
import gradio as gr
from core.agent import Sidekick

# --- State and Session Management ---
async def setup_session() -> Sidekick:
    """
    Initializes a new Sidekick instance for a user session.
    This function is executed once when the Gradio UI is first loaded.

    Returns:
        An initialized instance of the Sidekick agent.
    """
    sidekick = Sidekick()
    await sidekick.setup()
    return sidekick

async def reset_session() -> tuple:
    """
    Resets the current session by creating a new Sidekick instance and clearing UI fields.
    This is triggered by the 'Reset Session' button.

    Returns:
        A tuple containing empty values for the UI components and a new Sidekick instance.
    """
    gr.Info("Session has been reset.")
    new_sidekick = await setup_session()
    # Returns: message, success_criteria, chatbot_history, sidekick_instance
    return "", "", [], new_sidekick

def cleanup_resources(sidekick: Sidekick | None):
    """
    A callback function to free up resources when the Gradio app is closed or reloaded.
    This is linked to the `delete_callback` of the gr.State object.

    Args:
        sidekick: The Sidekick instance from the current session, if it exists.
    """
    print("Gradio is shutting down. Cleaning up resources...")
    if sidekick:
        try:
            # Run the async cleanup function in a new event loop
            asyncio.run(sidekick.cleanup())
        except Exception as e:
            print(f"Error during resource cleanup: {e}")

# --- Gradio UI Event Handlers ---
async def handle_message(
    sidekick: Sidekick, message: str, success_criteria: str, history: list
) -> tuple:
    """
    Processes a user's message submission by invoking the Sidekick agent.

    Args:
        sidekick: The current Sidekick instance from Gradio state.
        message: The user's input message from the textbox.
        success_criteria: The success criteria defined by the user.
        history: The current chat history from the chatbot component.

    Returns:
        A tuple containing the updated chat history and the sidekick instance.
    """
    if not message.strip():
        gr.Warning("Please enter a message before submitting.")
        return history, sidekick

    # Append the user's message to the chat history for immediate display
    history.append({"role": "user", "content": message})
    
    try:
        # Run the agent and get the updated history
        updated_history = await sidekick.run_step(history, success_criteria)
        return updated_history, sidekick
    except Exception as e:
        # Display an error message in the chat if something goes wrong
        error_message = f"An unexpected error occurred: {e}"
        print(f"Error in handle_message: {error_message}")
        history.append({"role": "assistant", "content": error_message})
        return history, sidekick

# --- Gradio UI Layout ---
with gr.Blocks(
    title="AI Sidekick",
    theme=gr.themes.Default(primary_hue="emerald", secondary_hue="emerald"),
    css=".gradio-container { max-width: 800px !important; margin: auto !important; }"
) as ui:
    
    gr.Markdown("## AI Sidekick: Your Personal Co-Worker")
    gr.Markdown(
        "Define a task and its success criteria. The agent will work on it, "
        "reflect on its own work, and continue until the task is complete or it needs your input."
    )

    sidekick_state = gr.State(delete_callback=cleanup_resources)

    chatbot = gr.Chatbot(
        label="Conversation",
        height=500,
        avatar_images=(None, "https://i.imgur.com/2hbeSot.png"),
        type="messages"
    )

    with gr.Group():
        message_input = gr.Textbox(
            show_label=False,
            placeholder="Enter your request for the Sidekick...",
            lines=3,
        )
        criteria_input = gr.Textbox(
            show_label=False,
            placeholder="Define the success criteria for this task...",
            lines=2
        )
            
    with gr.Row():
        reset_btn = gr.Button("🔄 Reset Session", variant="stop")
        submit_btn = gr.Button("▶️ Run Task", variant="primary")

    # --- Event Wiring ---
    ui.load(setup_session, inputs=None, outputs=[sidekick_state])

    submit_btn.click(
        handle_message,
        inputs=[sidekick_state, message_input, criteria_input, chatbot],
        outputs=[chatbot, sidekick_state]
    )
    
    message_input.submit(
        handle_message,
        inputs=[sidekick_state, message_input, criteria_input, chatbot],
        outputs=[chatbot, sidekick_state]
    )

    reset_btn.click(
        reset_session,
        inputs=None,
        outputs=[message_input, criteria_input, chatbot, sidekick_state]
    )

# --- Application Entry Point ---
if __name__ == "__main__":
    ui.launch(inbrowser=True)