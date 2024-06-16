##--- Audio STT & TTS with Recorded Audio ---##
import os
from pathlib import Path
from openai import OpenAI
import streamlit as st
import warnings
from dotenv import load_dotenv

load_dotenv(os.getcwd()+"/local.env")

# Ignore DeprecationWarning
#warnings.filterwarnings("ignore", category=DeprecationWarning)

st.title("A Talking Bot")

os.makedirs("text",  exist_ok=True)
os.makedirs("audio",  exist_ok=True)
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
client = OpenAI()

audio_file = st.file_uploader("Upload Audio : ", type=["wav","mp3","m4a"])
st.markdown(''' *:grey[You can find some samples to download here] https://pixabay.com/music/search/vocal%20samples/*''')
print(audio_file)
print(type(audio_file))

# upload_audio = st.button("Wish to upload")
# if upload_audio:
#     audio_file = st.file_uploader("Upload Audio : ", type=["wav","mp3","m4a"])
#     print(audio_file)
# else:
#     #Default
#     audio_file = Path(__file__).parent / "original_audio/rise-and-shine-203779.mp3"
#     print(audio_file)

text_file_path = os.path.join("text/", "audio-text.txt")
created_audio_file_path = os.path.join("audio/", "text-audio.mp3")

def read_text():
    with open(text_file_path, 'r') as file:
        text= file.read()
    return text
def transcribe_audio():
    transcription = client.audio.transcriptions.create(
    model="whisper-1", 
    file=audio_file)
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
    st.text_area("Audio Text ", content, height=500)
    with open(text_file_path, 'w') as file:
        file.writelines(content) 
    st.markdown("Convert audio to text done")

if st.sidebar.button("Convert text to audio"):
    back_to_audio()
    st.subheader(''' :rainbow["Here you go...!"]''', divider='blue')
    st.markdown("**Convert text to audio**")
    print(created_audio_file_path)
    st.audio(created_audio_file_path)
    st.markdown("**Play original audio**")
    print(audio_file)
    st.audio(audio_file)
    st.markdown("**The converted text of the audio**")
    st.markdown(read_text())

