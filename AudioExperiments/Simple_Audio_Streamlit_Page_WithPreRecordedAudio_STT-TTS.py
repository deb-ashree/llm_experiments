##--- Audio STT & TTS with Recorded Audio ---##
import os
from pathlib import Path
from openai import OpenAI
import streamlit as st
import warnings
from dotenv import load_dotenv

load_dotenv(os.getcwd()+"/local.env")
parent_folder = "AudioExperiments/"
# Ignore DeprecationWarning
#warnings.filterwarnings("ignore", category=DeprecationWarning)

st.title("Audio Bot Experiments")

os.makedirs(parent_folder+"text",  exist_ok=True)
os.makedirs(parent_folder+"audio",  exist_ok=True)
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
client = OpenAI()

afile = st.file_uploader("Upload Audio : ", type=["wav","mp3","m4a"])
st.markdown(''' *:grey[You can find some samples to download here] https://pixabay.com/music/search/vocal%20samples/*''')
print(afile)
print(type(afile))
st.audio(afile)

text_file_path = os.path.join(parent_folder+"text/", "audio-text.txt")
created_audio_file_path = os.path.join(parent_folder+"audio/", "text-audio.mp3")

def read_text():
    with open(text_file_path, 'r') as file:
        text= file.read()
    return text
def transcribe_audio():
    transcription = client.audio.transcriptions.create(
    model="whisper-1", 
    file=afile)
    print(os.getcwd())
    return transcription.text

def back_to_audio():
    with client.audio.speech.with_streaming_response.create(
    model="tts-1",
    voice="alloy",
    input=read_text()
    ) as  response:
        response.stream_to_file(created_audio_file_path)

if st.sidebar.button("Transcribe audio to text"):
    content = transcribe_audio()
    print("Content :\n"+content)
    st.text_area("Audio Text ", content, height=500)
    with open(text_file_path, 'w') as file:
        file.writelines(content) 
        print(content)
    st.markdown("Convert audio to text done")

if st.sidebar.button("Convert text to audio"):
    back_to_audio()
    st.subheader(''' :rainbow["Here you go...!"]''', divider='blue')
    st.markdown("**Convert text to audio**")
    print(created_audio_file_path)
    st.audio(created_audio_file_path)
    st.markdown("**Play original audio**")
    print(afile)
    st.audio(afile)
    st.markdown("**The converted text of the audio**")
    st.markdown(read_text())

