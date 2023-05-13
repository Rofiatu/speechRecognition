import streamlit as st
import speech_recognition as sr
from googletrans import Translator
import sounddevice as sd

st.title("Speech Recognition App")
st.sidebar.header('About')
st.sidebar.write('This app allows you convert your speech to text and select your desired speaking language out of 10 most popular languages.')

username = st.text_input('What is your name?')
if username != '':
    st.success(f'Hello there, {username}')
context = st.text_input('Please write a brief summary of what you would like to work on today.')

# Define supported languages
supported_languages = {
    "English": "en",
    "Spanish": "es",
    "French": "fr",
    "German": "de",
    "Italian": "it",
    "Portuguese": "pt",
    "Russian": "ru",
    "Japanese": "ja",
    "Korean": "ko",
    "Chinese": "zh-CN",
    "Yoruba": "yo"
}

# Add a dropdown menu to select the language
sp_language = st.selectbox("Select your speaking language", list(supported_languages.keys()))

def chosen(language):
    if language in supported_languages.keys():
        selected_language_code = supported_languages[language]
        # print(selected_language_code)
        return selected_language_code

sp_chosen_language = chosen(sp_language)
# print(sp_chosen_language)

def preprocess():
    # Initialize recognizer class
    r = sr.Recognizer()

    # Configure the recognizer to use the selected language
    r.energy_threshold = 4000  # Adjust this value according to your microphone
    r.dynamic_energy_threshold = True
    r.pause_threshold = 1.0
    r.phrase_threshold = 0.3
    r.non_speaking_duration = 0.8
    r.operation_timeout = None
    # r.recognize_google.language = language

    # Record the speech
    with sr.Microphone(device_index=None) as source:
            r.adjust_for_ambient_noise(source)
            status_text = st.empty()
            status_text.info("Recording in progress...")
            audio = r.listen(source)
            status_text.empty()
            status_text.info("Here you go...")

    # Transcribe the speech
    try:
        text = r.recognize_google(audio, language=sp_chosen_language)
    except sr.UnknownValueError:
        st.warning("No speech detected.")
        text = ""
    return text

def display():
    your_words_in_text = ""
    record_clicked = False
    
    # add a button to trigger speech recognition
    record_b = st.button('Start recording')
    
    if record_b:
        record_clicked = True
        your_words_in_text = preprocess()
        if your_words_in_text != '':
            st.write("Transcription: ", your_words_in_text)

    with open(f'transcription.txt', 'w') as f:
        f.write(f'{username}\n\n{context}\n\n{your_words_in_text}')

    # Assume that `transcription.txt` contains the transcribed text
    with open("transcription.txt", "r") as f:
        transcribed_text = f.read()

    if record_clicked:
        if your_words_in_text != '':
            # Add a download button
            download = st.download_button(
                            label="Download Transcription",
                            data=transcribed_text,
                            file_name="transcription.txt",
                            mime="text/plain",
                            key='download'
                        )
            if download:
                st.success('File downloaded successfully!')
        else:
            st.warning('No file to download')

    return your_words_in_text

if __name__ == "__main__":
    display()
