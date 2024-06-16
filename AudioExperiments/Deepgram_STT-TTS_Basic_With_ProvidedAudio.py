from deepgram import (
    DeepgramClient,
    SpeakOptions,
    LiveTranscriptionEvents,
    LiveOptions,
)
import httpx
from dotenv import load_dotenv
import os

# URL for the realtime streaming audio you would like to transcribe

# STT - from recorded audio
#----------------------------------
# main.py (python example)

import os
from dotenv import load_dotenv

from deepgram import (
    DeepgramClient,
    PrerecordedOptions,
    FileSource,
)

load_dotenv(os.getcwd()+"/local.env")

# Path to the audio file
#AUDIO_FILE = "original_audio/rise-and-shine-203779.mp3"
AUDIO_URL = {"url": "https://dpgr.am/spacewalk.wav"}
API_KEY = os.getenv("DEEPGRAM_API_KEY")

#------------------**********-----------------

#STT - Save to file - working code
#----------------------------------

# def main():
#     try:
#         # STEP 1 Create a Deepgram client using the API key
#         deepgram = DeepgramClient(API_KEY)

#         # with open(AUDIO_FILE, "rb") as file:
#         #     buffer_data = file.read()

#         # payload: FileSource = {
#         #     "buffer": buffer_data,
#         # }

#         #STEP 2: Configure Deepgram options for audio analysis
#         options = PrerecordedOptions(
#             model="nova-2",
#             smart_format=True,
#         )

#         # STEP 3: Call the transcribe_file method with the text payload and options
#         #response = deepgram.listen.prerecorded.v("1").transcribe_file(payload, options)
#         response = deepgram.listen.prerecorded.v("1").transcribe_url(AUDIO_URL, options)

#         # STEP 4: Print the response
#         print(response.results.channels[0].alternatives[0].transcript)
#         #print(response.to_json(indent=4))

#     except Exception as e:
#         print(f"Exception: {e}")


# if __name__ == "__main__":
#     main()


#----------------------------------

#------------------**********-----------------

#TTS - Save to file - working code
#----------------------------------

SPEAK_OPTIONS = {"text": "Hello, how can I help you today?"}
filename = "AudioExperiments/output.wav"


def main():
    try:
        # STEP 1: Create a Deepgram client using the API key from environment variables
        deepgram = DeepgramClient(api_key=os.getenv("DEEPGRAM_API_KEY"))

        # STEP 2: Configure the options (such as model choice, audio configuration, etc.)
        options = SpeakOptions(
            model="aura-asteria-en",
            encoding="linear16",
            container="wav"
        )

        # STEP 3: Call the save method on the speak property
        response = deepgram.speak.v("1").save(filename, SPEAK_OPTIONS, options)
        print(response.to_json(indent=4))

    except Exception as e:
        print(f"Exception: {e}")


if __name__ == "__main__":
    main()


#----------------------------------