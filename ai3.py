import openai
import sounddevice as sd
import soundfile as sf
import pyttsx3
import speech_recognition as sr
import datetime
import time
from playsound import playsound
import requests

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
    print("I'm listening... Speak now.")
    
    duration = 5  # 5 saniye boyunca sesi kaydedin
    sample_rate = 44100

    print("Speak...")
    myrecording = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=2)
    sd.wait()
    sf.write("user_input.wav", myrecording, sample_rate)

    # Ses dosyasını metne çevirin
    recognizer = sr.Recognizer()
    with sr.AudioFile("user_input.wav") as source:
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
    engine.say(response_text)
    engine.runAndWait()

def speak_weather(weather_data):
    # API'den gelen hava durumu verilerini kullanarak sesli olarak bildirin
    weather_description = weather_data["daily"]["weathercode"]
    temperature_max = weather_data["daily"]["temperature_2m_max"]
    temperature_min = weather_data["daily"]["temperature_2m_min"]
    precipitation_sum = weather_data["daily"]["precipitation_sum"]

    weather_info = f"Today's weather: {weather_description},\nMaximum temperature: {temperature_max}°C,\nMinimum temperature: {temperature_min}°C,\nTotal precipitation: {precipitation_sum} mm."
    speak(weather_info)

def set_alarm(alarm_time):
    while True:
        current_time = datetime.datetime.now().strftime("%H:%M")
        if current_time == alarm_time:
            # Alarmı tetikle ve alarm sesini çal
            playsound("C:/Users/asimb/Desktop/alarm_sound.mp3")  # alarm_sound.mp3 dosyasının doğru yolunu belirtin
            speak("It's time to wake up sir! Good morning. get up too you asshole")
            return True  # Alarm çaldı, True döndürerek hava durumu bilgisini söyleyeceğimizi belirtiyoruz.
        time.sleep(1)  # Her saniye kontrol et

if __name__ == "__main__":
    speak("Hello! I'm Jarvis, how can I assist you?")
    alarm_time = "08:00"  # Alarmı istediğiniz saat olarak ayarlayın (24 saat formatında)
    alarm_triggered = set_alarm(alarm_time)
    if alarm_triggered:
                    api_url = "https://api.open-meteo.com/v1/forecast?latitude=41.0138&longitude=28.9497&hourly=temperature_2m,relativehumidity_2m,apparent_temperature,precipitation_probability,soil_temperature_0cm&daily=weathercode,temperature_2m_max,temperature_2m_min,apparent_temperature_max,apparent_temperature_min,sunrise,uv_index_max,uv_index_clear_sky_max,precipitation_sum,rain_sum,showers_sum,precipitation_hours,precipitation_probability_max,windspeed_10m_max,windgusts_10m_max,winddirection_10m_dominant,shortwave_radiation_sum,et0_fao_evapotranspiration&timezone=auto&start_date=2023-08-05&end_date=2023-08-12"
                    response = requests.get(api_url)
                    weather_data = response.json()
                    speak_weather(weather_data)           
    while True:
        user_input = listen_to_user()
        if user_input:
            if "stop" in user_input.lower():
                print("Shutting down Jarvis...")
                speak("Goodbye!")
                break
          #  elif "weather" in user_input.lower():
                # Alarmı ayarla ve çaldığında hava durumu bilgisini söyle
                
            else:
                jarvis_response_text = jarvis_response(user_input)
                speak(jarvis_response_text)
