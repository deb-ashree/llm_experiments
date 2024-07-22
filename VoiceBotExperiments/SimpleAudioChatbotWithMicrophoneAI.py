
#pip uninstall openai-whisper
#pip install git+https://github.com/openai/whisper.git


##--- Reference from Youtube modified for Start and Stop of conversation ---##
import io, re, os, sys
import streamlit as st
import speech_recognition as sr
from openai import OpenAI
from gtts import gTTS
import playsound
from langchain_community.llms import Ollama
from dotenv import load_dotenv

load_dotenv(os.getcwd()+"/local.env")
## print(os.getcwd())

os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
client = OpenAI()

#tf.io.gfile.GFile(name, mode='r')

def speak(text):
    tts = gTTS(text=text, lang="en")
    filename = "voice.mp3"

    tts.save(filename)
    playsound.playsound(filename)
    
    ## Option 2 - TBTested
	#engine = pyttsx3.init()
	#engine.say(text) 
	#engine.runAndWait()
	

def generate_audio():
    pattern = re.compile("End of chat")

    r = sr.Recognizer()
    with sr.Microphone() as source:
        
        # wait for a second to let the recognizer
        # adjust the energy threshold based on
        # the surrounding noise level 
        r.adjust_for_ambient_noise(source, duration=0.5)

        audio = r.listen(source)
        #playsound.playsound(audio)
        said = ""

        try:
            said = "You said : "+r.recognize_whisper(audio_data=audio, model="base")
            print(said)
            #type(said)
            match = re.search(pattern, said)
            if match == True:
                exit(1)
            else:
                generate_ai_response(said)
        except Exception as e:
            print("Exception : "+str(e))
    return said

def openChat(i):
    i = 1
    speak("How can I help you today!")
    return i

def generate_ai_response(text):
    ##for gpt
    #transcript = '{"role":"user", "content": {text}}'
    transcript = "Give a one line response of the query " + text

    ## for llama
    #transcript = "Give a one line summary of the query " + text
    
    print(f"\nUser: {text}", end="\r\n")

    ## With GPT
    response = client.chat.completions.create(
        model = "gpt-4",
        messages = [ {"role": "user", "content": f'{transcript}'}],
        max_tokens=200
    )
    ai_response = response.choices[0].message.content

    ## With Llama -- response is very incoherent
    # llm = Ollama(model = "llama3")
    # response = llm.invoke(transcript)
    # ai_response = response #.message.content

    print(ai_response)
    speak(ai_response)
    
    #generate_audio()

    print(f"\nResponse transcription: ", end="\r\n")

def main():
    ## Function for the initial pleasantries
    i = 0
    # if i == 0:
    #     i = openChat(i)

    container_2 = st.empty()
    button_A = container_2.button('Start')
    if button_A:
        print("A1")
        print("A2")
        container_2.empty()
        button_B = container_2.button('Stop', key='B')
        st.write('Responding')
        generate_audio()
        if button_B:
            print("B")
            print("B")
            container_2.empty()
            button_A = container_2.button('Start', key='A')
            st.write('Listening')

if __name__ == "__main__":
     main()