import streamlit as st
import whisper
from gtts import gTTS
from pydub import AudioSegment
import os

# Load Whisper model
@st.cache_resource()
def load_model():
    return whisper.load_model("small")

model = load_model()

# Streamlit UI
st.title("🎙️ Speech-to-Text & Text-to-Speech App")
st.write("Upload an audio file, transcribe it, and generate speech output.")

uploaded_file = st.file_uploader("Upload an audio file", type=["mp3", "wav", "m4a"]) 

if uploaded_file is not None:
    file_path = "temp_audio.mp3"
    with open(file_path, "wb") as f:
        f.write(uploaded_file.read())
    
    # Convert to WAV if needed
    if uploaded_file.name.endswith(".m4a"):
        audio = AudioSegment.from_file(file_path, format="m4a")
        file_path = "converted_audio.wav"
        audio.export(file_path, format="wav")
    
    st.audio(file_path, format='audio/mp3')
    
    # Transcription
    with st.spinner("Transcribing..."):
        result = model.transcribe(file_path)
        transcribed_text = result["text"]
    
    st.subheader("📝 Transcribed Text:")
    st.write(transcribed_text)
    
    # Text-to-Speech (TTS)
    if st.button("🔊 Generate Speech"):
        tts = gTTS(transcribed_text, lang="en")
        tts.save("output.mp3")
        st.audio("output.mp3", format="audio/mp3")
    
    # Cleanup
    os.remove(file_path)
