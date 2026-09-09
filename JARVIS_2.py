import pyttsx3  # Преобразование текста в речь
import speech_recognition as sr  # Распознавание речи
import datetime  # Дата и время
import time  # Задержки

# ------------------- ГОЛОСОВОЙ ДВИЖОК ------------------- #
def Speak(text):
    rate = 150
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[0].id)
    engine.setProperty('rate', rate + 50)
    engine.say(text)
    engine.runAndWait()

r = sr.Recognizer()
keywords = [("джарвис", 1), ("эй джарвис", 1), ("джарвис слушай", 1)]
source = sr.Microphone()

# ------------------- ОСНОВНОЕ РАСПОЗНАВАНИЕ ------------------- #
def recognize_main(recognizer, audio):
    try:
        data = recognizer.recognize_google(audio, language="ru-RU").lower()
        print("Вы сказали: " + data)

        if "как дела" in data:
            Speak("У меня всё отлично. А как у вас?")
        elif "хорошо" in data:
            Speak("Рад это слышать. Тогда зачем я вам понадобился?")
        elif "плохо" in data:
            Speak("Очень жаль это слышать.")
        elif "привет" in data or "здравствуй" in data:
            Speak("Здравствуйте. Чем могу помочь?")
        elif "который час" in data or "сколько времени" in data:
            current_time = datetime.datetime.now().strftime("%H:%M")
            Speak(f"Сейчас {current_time}.")
        elif "какая сегодня дата" in data or "какое сегодня число" in data:
            now = datetime.datetime.now()
            months = [
                "января", "февраля", "марта", "апреля", "мая", "июня",
                "июля", "августа", "сентября", "октября", "ноября", "декабря"
            ]
            current_date = f"{now.day} {months[now.month - 1]} {now.year} года"
            Speak(f"Сегодня {current_date}.")

        elif "выход" in data or "выйти" in data or "пока" in data:
            Speak("До свидания.")
            exit()
        else:
            Speak("Извините, я не понял. Повторите, пожалуйста.")

    except sr.UnknownValueError:
        print("Джарвис не понял вашу команду.")
    except sr.RequestError as e:
        print(f"Не удалось обратиться к сервису распознавания речи Google: {e}")

if __name__ == "__main__":
    print("Ожидание ключевого слова...")
    r.listen_in_background(source, recognize_main)
    while True:
        time.sleep(1)