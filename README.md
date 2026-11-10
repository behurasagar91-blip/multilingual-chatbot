# 🌐 Multilingual AI Chatbot

An AI-powered chatbot that allows users to communicate in multiple languages. It uses Groq AI to generate responses and Google Text-to-Speech (gTTS) to convert responses into audio.

## 🚀 Live Demo

**Try the chatbot here:**

[Open Multilingual AI Chatbot](https://multilingual-chatbot-xxvspydmc5usyrcjdlwusz.streamlit.app/)

## 📌 Project Overview

The Multilingual AI Chatbot is designed to make communication easier for users who prefer different languages. Users can select a language, enter a question and receive an AI-generated response with audio output.

## ✨ Features

- 🌍 Multiple language support
- 🤖 AI-powered responses using Groq
- 🔊 Text-to-speech functionality
- 💬 Interactive chat interface
- 🗂️ Chat history stored using SQLite
- ☁️ Online deployment using Streamlit Community Cloud

## 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| Python | Main programming language |
| Streamlit | User interface |
| Groq API | AI response generation |
| gTTS | Text-to-speech |
| SQLite | Chat history storage |
| GitHub | Source code management |
| Streamlit Cloud | Cloud deployment |

## 💻 Run Locally

### 1. Clone the repository

```bash
git clone https://github.com/behurasagar91-blip/multilingual-chatbot.git
```

### 2. Open the project folder

```bash
cd multilingual-chatbot
```

### 3. Install dependencies

```bash
py -3.13 -m pip install -r requirements.txt
```

### 4. Configure your API key

Create a file named `.streamlit/secrets.toml` and add:

```toml
GROQ_API_KEY = "YOUR_GROQ_API_KEY"
```

Replace the placeholder with your own Groq API key. Never upload this file to GitHub.

### 5. Run the application

```bash
py -3.13 -m streamlit run app.py
```

## ☁️ Deployment

This application is deployed using Streamlit Community Cloud and uses the Groq API for AI responses.

## 👨‍💻 Developer

**Sagar Kumar**

BCA Student | Multilingual AI Chatbot Project

GitHub: [behurasagar91-blip](https://github.com/behurasagar91-blip)

---

⭐ If you find this project useful, feel free to explore the repository!
