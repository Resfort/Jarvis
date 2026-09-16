
import pyttsx3
import speech_recognition as sr


def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait() 

def listen_command():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Слушаю...")
        audio = recognizer.listen(source)
    try:
        command = recognizer.recognize_google(audio, language="ru-RU")
        print(f"Вы сказали: {command}")
        return command.lower()
    except sr.UnknownValueError:
        print("Не удалось распознать речь.")
        return ""
    except sr.RequestError:
        print("Ошибка сервиса распознавания речи.")
        return ""

speak("Привет! Я Джарвис, твой голосовой помощник.")