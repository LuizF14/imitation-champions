import time
import uuid

import gradio as gr

from services.conversation_service import ConversationService

def start_gradio():
    service = ConversationService()
    def respond(message, history, thread_id):
        result = service.execute(message, thread_id)
        partial = ""
        for part in result.messages:
            time.sleep(1)
            partial += (part if not partial else f"\n{part}")
            yield partial

    with gr.Blocks() as demo:
        thread_id = gr.State(f"gradio-{uuid.uuid4().hex[:8]}")

        gr.ChatInterface(
            fn=respond,
            additional_inputs=[thread_id],
            title="Pinky",
        )

    demo.launch()


if __name__ == "__main__":
    start_gradio()