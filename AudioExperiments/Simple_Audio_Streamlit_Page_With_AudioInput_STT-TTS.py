##--- Audio STT & TTS with Audio Input ---##
import io
import streamlit as st
from audio_recorder_streamlit import audio_recorder
import os
from openai import OpenAI
import base64 
from dotenv import load_dotenv

load_dotenv(os.getcwd()+"/local.env")

## TBC - audiorecorder doesn't load - https://developer.mozilla.org/en-US/docs/Web/API/MediaDevices/getUserMedia 
## To get this working, start, stop and again restart the streamlit commend, it will work in the previously opened webpage

audio_bytes = audio_recorder(
    text="",
    recording_color="#e8b62c",
    neutral_color="#6aa36f",
    icon_name="microphone-lines",
    icon_size="2x",
    #unsafe_allow_html=True
)

# TB tried if needed - audiorecorder(start_prompt="Start recording", stop_prompt="Stop recording", pause_prompt="", show_visualizer=True, key=None):

# Inject custom CSS to set the width of the sidebar
st.markdown(
    """
    <style>
        section[data-testid="stSidebar"] {
            width: 200px !important; # Set the width to your desired value
        }
    </style>
    """,
    unsafe_allow_html=True,
)

sidebar_bg_img = '''
<style>
body {
background-image: "blue-violet-sidebar2.jpeg"   #url("https://images.unsplash.com/photo-1542281286-9e0a16bb7366");
background-size: cover;
}
</style>
'''
def setBgImage(png_file):
    with open(png_file, 'rb') as f:
        data = base64.b64encode(f.read()).decode()
    page_bg_img = '''
                    <style>
                    body {
                        background-image: url("data:image/jpeg;base64,%s");
                        background-size: cover;
                    }
                    </style>
                    ''' % data
    st.sidebar.image(page_bg_img, use_column_width=True)
    return 

def sidebarBgColour(wch_colour): 
    my_colour = f"<style> .stApp {{background-color: {wch_colour};}} </style>"
    st.sidebar(my_colour, unsafe_allow_html=True)

st.sidebar.image("blue-violet-sidebar2.jpeg", use_column_width=True)

if audio_bytes:
    audio_file = open(os.getcwd()+"/AudioExperiments/original_audio/received_audio.mp3", "wb") 
    audio_file.write(audio_bytes)
    ##st.audio(audio_bytes, format="audio/mp3")
    print(type(audio_file))

os.makedirs("text",  exist_ok=True)
os.makedirs("audio",  exist_ok=True)
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
client = OpenAI()

text_file_path = os.path.join(os.getcwd()+"/AudioExperiments/text/", "audio-text.txt")
created_audio_file_path = os.path.join(os.getcwd()+"/AudioExperiments/audio/", "text-audio.mp3")

def read_text():
    with open(text_file_path, 'r') as file:
        text= file.read()
    return text

def transcribe_audio():
    transcription = client.audio.transcriptions.create(
    model="whisper-1", 
    file=open(audio_file.name,"rb"))
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
    st.audio(open(audio_file.name,"rb"))
    st.markdown("**The converted text of the audio**")
    st.markdown(read_text())


## Other trial for creating the sound file
#from pydub import AudioSegment
#import soundfile as sf
#audio_file = AudioSegment.from_raw(io.BytesIO(audio_bytes), audio_bytes.count).export("original_audio/received_audio.mp3", format='mp3')
#audio_file, samplerate = sf.read(io.BytesIO(audio_bytes))
#recording.export('new.mp3', format='mp3') # for export 
#play(recording) # for play  --> #from pydub.playback import play    