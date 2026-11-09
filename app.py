
import streamlit as st
import requests
import sqlite3
import uuid
import os
from gtts import gTTS
from io import BytesIO

OLLAMA_URL = "http://host.docker.internal:11434/api/chat"
MODEL = "qwen2.5:3b"
DB_PATH = "/tmp/chat_history.db"

def get_db():
    return sqlite3.connect(DB_PATH)

def init_db():
    with get_db() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS chats (
                id TEXT PRIMARY KEY,
                title TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                chat_id TEXT,
                role TEXT,
                content TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

def create_chat():
    chat_id = str(uuid.uuid4())
    with get_db() as conn:
        conn.execute(
            "INSERT INTO chats (id, title) VALUES (?, ?)",
            (chat_id, "New Chat")
        )
    return chat_id

def get_chats():
    with get_db() as conn:
        return conn.execute(
            "SELECT id, title FROM chats ORDER BY created_at DESC"
        ).fetchall()

def get_messages(chat_id):
    with get_db() as conn:
        rows = conn.execute(
            "SELECT role, content FROM messages WHERE chat_id = ? ORDER BY id",
            (chat_id,)
        ).fetchall()
    return [{"role": role, "content": content} for role, content in rows]

def save_message(chat_id, role, content):
    with get_db() as conn:
        conn.execute(
            "INSERT INTO messages (chat_id, role, content) VALUES (?, ?, ?)",
            (chat_id, role, content)
        )

        if role == "user":
            conn.execute(
                """UPDATE chats SET title = ?
                   WHERE id = ? AND title = 'New Chat'""",
                (content[:40], chat_id)
            )

# Start application
init_db()

st.set_page_config(
    page_title="Multilingual AI Chatbot",
    page_icon="🌍",
    layout="centered"
)

if "chat_id" not in st.session_state:
    st.session_state.chat_id = create_chat()

# Language options
languages = {
    "English": "en",
    "Hindi": "hi",
    "Kannada": "kn",
    "Tamil": "ta",
    "Telugu": "te",
    "Malayalam": "ml",
    "Marathi": "mr",
    "Bengali": "bn",
    "Spanish": "es",
    "French": "fr",
    "German": "de",
    "Japanese": "ja"
}

# Sidebar and history
with st.sidebar:
    st.title("💬 Chat History")

    if st.button("➕ New Chat", use_container_width=True):
        st.session_state.chat_id = create_chat()
        st.rerun()

    st.divider()

    for chat_id, title in get_chats():
        label = title or "New Chat"

        if st.button(
            label[:35],
            key=f"chat_{chat_id}",
            use_container_width=True
        ):
            st.session_state.chat_id = chat_id
            st.rerun()

    st.divider()
    language = st.selectbox(
        "Choose your language:",
        list(languages.keys())
    )

# Main chatbot
st.title("🌍 Multilingual AI Chatbot")
st.write("Chat with AI in your favourite language!")

# Display saved messages
for message in get_messages(st.session_state.chat_id):
    with st.chat_message(message["role"]):
        st.write(message["content"])

# User input
user_input = st.chat_input("Type your message here...")

if user_input:
    chat_id = st.session_state.chat_id

    save_message(chat_id, "user", user_input)

    with st.chat_message("user"):
        st.write(user_input)

    try:
        with st.chat_message("assistant"):
            with st.spinner("AI is thinking..."):

                messages = [
                    {
                        "role": "system",
                        "content": (
                            f"You are a helpful multilingual assistant. "
                            f"Always respond in {language}. "
                            "Give clear and useful answers."
                        )
                    }
                ] + get_messages(chat_id)

                response = requests.post(
                    OLLAMA_URL,
                    json={
                        "model": MODEL,
                        "messages": messages,
                        "stream": False
                    },
                    timeout=180
                )

                response.raise_for_status()
                answer = response.json()["message"]["content"]

                save_message(chat_id, "assistant", answer)
                st.write(answer)

                try:
                    audio_buffer = BytesIO()
                    speech = gTTS(
                        text=answer,
                        lang=languages[language]
                    )
                    speech.write_to_fp(audio_buffer)
                    audio_buffer.seek(0)

                    st.audio(audio_buffer, format="audio/mp3")

                except Exception:
                    st.info("Text response is available, but speech could not be generated.")

    except requests.exceptions.RequestException as e:
        st.error(f"Could not connect to Ollama: {e}")

    except Exception as e:
        st.error(f"Error: {e}")
