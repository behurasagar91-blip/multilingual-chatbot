
import streamlit as st
from groq import Groq
from gtts import gTTS
from io import BytesIO
import sqlite3
import uuid

# Page configuration
st.set_page_config(
    page_title="Multilingual AI Chatbot",
    page_icon="🌐",
    layout="centered"
)

# Groq API connection
client = Groq(
    api_key=st.secrets["GROQ_API_KEY"]
)

# Database
def get_db():
    return sqlite3.connect("chat_history.db")

def init_db():
    with get_db() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                chat_id TEXT,
                role TEXT,
                content TEXT
            )
        """)

def save_message(chat_id, role, content):
    with get_db() as conn:
        conn.execute(
            "INSERT INTO messages (chat_id, role, content) VALUES (?, ?, ?)",
            (chat_id, role, content)
        )

def get_messages(chat_id):
    with get_db() as conn:
        rows = conn.execute(
            "SELECT role, content FROM messages WHERE chat_id=? ORDER BY id",
            (chat_id,)
        ).fetchall()
    return [{"role": r, "content": c} for r, c in rows]

# Initialize database
init_db()

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

# Session state
if "chat_id" not in st.session_state:
    st.session_state.chat_id = str(uuid.uuid4())

# Sidebar
with st.sidebar:
    st.title("💬 Chat History")

    if st.button("➕ New Chat"):
        st.session_state.chat_id = str(uuid.uuid4())
        st.rerun()

# Main interface
st.title("🌐 Multilingual AI Chatbot")
st.write("Chat with AI in your favourite language!")

language = st.selectbox(
    "Choose your language:",
    list(languages.keys())
)

# Display previous messages
chat_id = st.session_state.chat_id

for message in get_messages(chat_id):
    with st.chat_message(message["role"]):
        st.write(message["content"])

# User input
user_input = st.chat_input("Type your message here...")

if user_input:
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

                completion = client.chat.completions.create(
                    model="openai/gpt-oss-120b",
                    messages=messages,
                    temperature=0.7
                )

                answer = completion.choices[0].message.content

                save_message(chat_id, "assistant", answer)
                st.write(answer)

                # Generate speech
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

    except Exception as e:
        st.error(f"Error: {e}")
