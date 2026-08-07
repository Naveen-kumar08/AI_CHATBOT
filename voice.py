import speech_recognition as sr
import pyttsx3


# ==========================
# Speech To Text
# ==========================

def listen_voice():

    recognizer = sr.Recognizer()

    with sr.Microphone() as source:

        print("Listening...")

        audio = recognizer.listen(
            source
        )


    try:

        text = recognizer.recognize_google(
            audio
        )

        return text


    except:

        return ""



# ==========================
# Text To Speech
# ==========================

def speak_text(text):

    engine = pyttsx3.init()

    engine.say(
        text
    )

    engine.runAndWait()