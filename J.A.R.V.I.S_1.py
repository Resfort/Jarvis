"""
Голосовой ассистент J.A.R.V.I.S.
Для работы требуются библиотеки:
pip install pyttsx3 SpeechRecognition wikipedia pyaudio
"""

import pyttsx3
import speech_recognition as sr
import datetime
import wikipedia
import webbrowser
import os
import sys

# Инициализация pyttsx3 для преобразования текста в речь (TTS)
engine = pyttsx3.init()

# Настройка голоса (попытка установить русский голос, если он есть в системе)
voices = engine.getProperty('voices')
for voice in voices:
    if 'ru' in voice.languages or 'russian' in voice.name.lower() or 'ru_ru' in voice.id.lower():
        engine.setProperty('voice', voice.id)
        break

# Установка скорости речи
engine.setProperty('rate', 170) 

def speak(text):
    """
    Функция для произношения переданного текста.
    """
    print(f"J.A.R.V.I.S.: {text}")
    engine.say(text)
    engine.runAndWait()

def wish_me():
    """
    Функция приветствия в зависимости от времени суток.
    """
    hour = int(datetime.datetime.now().hour)
    if hour >= 0 and hour < 12:
        speak("Доброе утро, сэр!")
    elif hour >= 12 and hour < 18:
        speak("Добрый день, сэр!")
    else:
        speak("Добрый вечер, сэр!")
        
    speak("Я Джарвис. Чем могу помочь вам сегодня?")

def take_command():
    """
    Слушает микрофон и возвращает распознанный текст.
    """
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Слушаю...")
        # Настройка паузы перед завершением прослушивания фразы
        r.pause_threshold = 1
        # Адаптация к фоновому шуму
        r.adjust_for_ambient_noise(source, duration=1) 
        
        try:
            audio = r.listen(source, timeout=5, phrase_time_limit=5)
        except sr.WaitTimeoutError:
            print("Таймаут ожидания...")
            return "None"

    try:
        print("Распознавание...")    
        # Используем Google Speech Recognition (требуется интернет)
        query = r.recognize_google(audio, language='ru-RU')
        print(f"Вы сказали: {query}\n")
    
    except sr.UnknownValueError:
        print("Извините, не расслышал. Повторите, пожалуйста.")
        return "None"
    except sr.RequestError:
        print("Ошибка сервиса распознавания. Проверьте интернет.")
        return "None"
    except Exception as e:
        print(e)
        return "None"
        
    return query.lower()

if __name__ == "__main__":
    # Устанавливаем русский язык для поиска в Википедии
    wikipedia.set_lang("ru")
    
    # Запуск приветствия
    wish_me()
    
    # Основной цикл обработки команд
    while True:
        query = take_command()
        
        if query == "None":
            continue

        # Логика обработки различных команд
        if 'википедия' in query:
            speak('Ищу в Википедии...')
            query = query.replace("википедия", "").strip()
            try:
                # Получаем 2 предложения из статьи
                results = wikipedia.summary(query, sentences=2)
                speak("Согласно Википедии")
                speak(results)
            except wikipedia.exceptions.DisambiguationError as e:
                speak("Найдено слишком много значений. Пожалуйста, уточните запрос.")
            except wikipedia.exceptions.PageError:
                speak("Извините, я не смог найти информацию по этому запросу.")

        elif 'открой youtube' in query or 'ютуб' in query:
            speak("Открываю YouTube")
            webbrowser.open("https://youtube.com")

        elif 'открой google' in query or 'гугл' in query:
            speak("Открываю Google")
            webbrowser.open("https://google.com")
            
        elif 'открой github' in query or 'гитхаб' in query:
            speak("Открываю GitHub")
            webbrowser.open("https://github.com")

        elif 'время' in query or 'который час' in query:
            strTime = datetime.datetime.now().strftime("%H:%M")    
            speak(f"Сэр, сейчас {strTime}")

        elif 'спасибо' in query:
            speak("Всегда к вашим услугам, сэр.")

        elif 'выход' in query or 'отключись' in query or 'пока' in query or 'стоп' in query:
            speak("Отключаю системы. До свидания, сэр!")
            sys.exit()
            
        else:
            # Для нераспознанных специфичных команд
            print(f"[Команда не обработана: {query}]")