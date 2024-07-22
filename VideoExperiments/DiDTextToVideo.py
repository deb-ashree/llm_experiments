import time
import requests, os
import streamlit as st
from dotenv import load_dotenv

load_dotenv(os.getcwd()+"/local.env")

st.title("Video Generation Board")

url = "https://api.d-id.com/talks"

did_api_key = os.getenv("D-ID_API_KEY")

import requests

headers = {
    "accept": "application/json",
    "content-type": "application/json",
    "Authorization" : "Basic "+ did_api_key  
}

def postCreateTalkVideo():
    print("At payload")
    payload = {
        "script": {
            "type": "text",
            "subtitles": "false",
            "input": "Hi, welcome to the video. Today we will learn more about Digital Marketing and how is a tool like Semrush useful in SEO monitoring.",
            "provider": {
                "type": "microsoft",
                "voice_id": "en-US-JennyNeural"
            },
            "ssml": "false"
        
        },
        "presenter_id": "lily-akobXDF34M",
        "driver_id": "oqNen3Q3aS",
        "source_url": "https://clips-presenters.d-id.com/lily/akobXDF34M/oqNen3Q3aS/image.png",
        "config": {
                "result_format": "mp4",
                "driver_expressions": {
                "expressions": [
                    # {
                    #     "start_frame": 0,
                    #     "expression": "surprise",
                    #     "intensity": 1.0
                    # },
                    {
                        "start_frame": 0,
                        "expression": "happy",
                        "intensity": 1.0
                    }
                ],
                "transition_frames": 20
            }
        }
    }
    print("Post payload...")
    try:
        print("Inside try..")
        post_response = requests.post(url, json=payload, headers=headers)
        print(post_response.status_code)
        if post_response.status_code == 201:
            print("Inside 201")
            print(post_response.text)
            res = post_response.json()
            id = "tlk_vmCrB0xvHj-JfIAh1fOgt"
            print("Id : "+id)
            status = "created"
            return id
    except Exception as e:
        print(e.with_traceback()) 

def getTalkVideo(id):
    fetch_url = "https://api.d-id.com/talks/"+id
    try:
        get_response = requests.get(url, headers=headers)
        print(get_response)
        if get_response.status_code == 200:
            video_url = get_response.json()["talks"][0]["result_url"]  
            print(video_url)
        return video_url
    except Exception as e:
        print(e.add_note())      
        video_url = "error"      

def main():
    id = postCreateTalkVideo()
    print(id)
    time.sleep(25)
    url= getTalkVideo(id)
    st.video(url)
    print("done")

if __name__ == "__main__":
     main()