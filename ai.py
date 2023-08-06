#openai.api_key = "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"

import openai
import sounddevice as sd
import soundfile as sf
import pyttsx3
import speech_recognition as sr
from gtts import gTTS
import os

# GPT-3 API anahtarınızı buraya girin
openai.api_key = "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"

# Sesli çıkış için konuşma motoru oluşturun
engine = pyttsx3.init()

def jarvis_response(input_text):
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=input_text,
        max_tokens=100
    )
    return response.choices[0].text.strip()

def listen_to_user():
    print("I'm listening... Press 'Enter' for voice input.")
    input("Press 'Enter' to continue.")

    filename = "user_input.wav"
    duration = 5  # 5 saniye boyunca sesi kaydedin
    sample_rate = 44100

    print("Speak...")
    myrecording = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=2)
    sd.wait()
    sf.write(filename, myrecording, sample_rate)

    # Ses dosyasını metne çevirin
    recognizer = sr.Recognizer()
    with sr.AudioFile(filename) as source:
        audio = recognizer.listen(source)

    try:
        user_input = recognizer.recognize_google(audio, language="en-US")
        print("You said: " + user_input)
        return user_input
    except sr.UnknownValueError:
        print("Sorry, I couldn't understand. Please repeat.")
        return listen_to_user()
    except sr.RequestError as e:
        print("Speech services are not working; {0}".format(e))
        return None

def speak(response_text):
    print("Jarvis says: " + response_text)
    #tts = gTTS(text=response_text, lang="en")  1
    #tts.save("jarvis_response.mp3")            1
    #os.system("start jarvis_response.mp3")     1

    engine.say(response_text)
    engine.runAndWait()

    

if __name__ == "__main__":
    #print("Hello! I'm Jarvis, how can I assist you?")
    speak("Hello! I'm Jarvis, how can I assist you?")
    while True:
        user_input = listen_to_user()
        if user_input:
            if "stop" in user_input.lower():
                print("Shutting down Jarvis...")
                speak("Goodbye!")
                break
            else:
                jarvis_response_text = jarvis_response(user_input)
                speak(jarvis_response_text)
