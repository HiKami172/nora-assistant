from voice_assistant import VoiceAssistant
import streamlit as st

voice_assistant = VoiceAssistant()


st.title("Nora Assistant")
"""
##  Application guidance
**Nora** is your personal voice assistant that is capable of searching the internet and performing
your tasks. It's powered with OpenAI GPT-3 model, which makes it a good partner for your everyday usage.
"""

col1, col2, col3 = st.columns([1,1,1])
col2.image('assets/img/logo.jpg')
col2.button("Speak", on_click=voice_assistant.run())
