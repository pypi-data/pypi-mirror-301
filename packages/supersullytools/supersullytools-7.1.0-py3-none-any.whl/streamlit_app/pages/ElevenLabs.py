import os

import requests
import streamlit as st


class Urls:
    voices_url = "https://api.elevenlabs.io/v1/voices"
    tts_url = "https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}/stream"


headers = {
    "Accept": "application/json",
    "xi-api-key": os.environ["ELEVEN_LABS_API_TOKEN"],
    # "Content-Type": "application/json",
}

if st.button("View Voices Ids"):
    response = requests.get(Urls.voices_url, headers=headers)

    data = response.json()

    for voice in data["voices"]:
        st.write(f"{voice['name']}; {voice['voice_id']}")

with st.form("TTS"):
    voice_id = st.text_input("Voice Id")
    content = st.text_area("TTS Content", height=150)
    if st.form_submit_button("Generate") and voice_id and content:
        tts_url = Urls.tts_url.format(VOICE_ID=voice_id)
        # Construct the URL for the Text-to-Speech API request

        # Set up headers for the API request, including the API key for authentication

        # Set up the data payload for the API request, including the text and voice settings
        data = {
            "text": content,
            "model_id": "eleven_multilingual_v2",
            "voice_settings": {"stability": 0.5, "similarity_boost": 0.8, "style": 0.0, "use_speaker_boost": True},
        }

        # Make the POST request to the TTS API with headers and data, enabling streaming response
        response = requests.post(tts_url, headers=headers, json=data, stream=True)

        # Check if the request was successful
        CHUNK_SIZE = 1024  # Size of chunks to read/write at a time

        if response.ok:
            # Collect the chunks into a single bytes object
            audio_data = b"".join(response.iter_content(chunk_size=CHUNK_SIZE))
            # Use st.audio with the combined binary data
            st.audio(audio_data, format="audio/mp3", autoplay=True)
            # # Open the output file in write-binary mode
            # with open(OUTPUT_PATH, "wb") as f:
            #     # Read the response in chunks and write to the file
            #     for chunk in response.iter_content(chunk_size=CHUNK_SIZE):
            #         f.write(chunk)
            # Inform the user of success
        else:
            # Print the error message if the request was not successful
            st.error(response.text)
