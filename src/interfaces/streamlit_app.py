import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT))

import uuid
import time
import streamlit as st

from services.conversation_service import ConversationService

BOT_NAME = "Imitation Champions" 

CHAT_CSS = """
<style>
.chat-row { display: flex; margin: 6px 0; }
.chat-row.user { justify-content: flex-end; }
.chat-row.bot { justify-content: flex-start; }

.bubble-wrap {
    max-width: 70%;
    min-width: 0;
}

.bubble {
    padding: 10px 14px;
    border-radius: 18px;
    font-size: 15px;
    line-height: 1.4;
    overflow-wrap: break-word;
    word-break: normal;
}
.bubble.user {
    background-color: #DCF8C6;
    color: #111;
    border-bottom-right-radius: 4px;
}
.bubble.bot {
    background-color: #FFFFFF;
    color: #111;
    border: 1px solid #E0E0E0;
    border-bottom-left-radius: 4px;
}
.sender-label {
    font-size: 11px;
    color: #888;
    margin: 0 8px 2px 8px;
}
</style>
"""


def init_state():
    if "thread_id" not in st.session_state:
        st.session_state.thread_id = f"streamlit-{uuid.uuid4().hex[:8]}"
    if "messages" not in st.session_state:
        st.session_state.messages = []


def render_bubble(role, content):
    css_role = "user" if role == "user" else "bot"
    label = "Você" if role == "user" else BOT_NAME
    st.markdown(
        f"""
        <div class="chat-row {css_role}">
            <div style="max-width: 70%;">
                <div class="sender-label" style="text-align: {'right' if css_role=='user' else 'left'};">{label}</div>
                <div class="bubble {css_role}">{content}</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_history():
    for msg in st.session_state.messages:
        render_bubble(msg["role"], msg["content"])


def stream_response(service, message, thread_id):
    result = service.execute(message, thread_id)
    for part in result.messages:
        yield part


def start_streamlit():
    st.set_page_config(page_title="Imitation Champions", page_icon="🤖", layout="centered")
    st.markdown(CHAT_CSS, unsafe_allow_html=True)

    service = get_service()
    init_state()

    render_history()

    user_input = st.chat_input("Digite sua mensagem...")
    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})
        render_bubble("user", user_input)

        for part in stream_response(service, user_input, st.session_state.thread_id):
            placeholder = st.empty()
            with placeholder.container():
                render_bubble("bot", part)

            st.session_state.messages.append({"role": "assistant", "content": part})
            time.sleep(0.6) 


@st.cache_resource
def get_service():
    return ConversationService()


if __name__ == "__main__":
    start_streamlit()