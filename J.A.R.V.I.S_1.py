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

# Настройка голоса (поиск всех русских голосов)
ru_voices = []
voices = engine.getProperty('voices')
for voice in voices:
    if 'ru' in voice.languages or 'russian' in voice.name.lower() or 'ru_ru' in voice.id.lower():
        ru_voices.append(voice)
        
# Устанавливаем первый найденный русский голос по умолчанию
if ru_voices:
    engine.setProperty('voice', ru_voices[0].id)
    
def change_voice(gender):
    """
    Функция для смены голоса на мужской или женский.
    Успех зависит от установленных голосов в ОС (например, Ирина и Павел).
    """
    if not ru_voices:
        print("Русские голоса не найдены.")
        return
        
    if gender == "male":
        for v in ru_voices:
            # Пытаемся найти мужской голос (Павел)
            if 'pavel' in v.name.lower() or 'муж' in v.name.lower():
                engine.setProperty('voice', v.id)
                print("Установлен мужской голос.")
                return
        # Если явного мужского нет, пробуем поставить второй из списка
        if len(ru_voices) > 1:
            engine.setProperty('voice', ru_voices[1].id)
            print("Установлен альтернативный голос.")
        else:
            print("В системе доступен только один русский голос.")
            
    elif gender == "female":
        for v in ru_voices:
            # Пытаемся найти женский голос (Ирина)
            if 'irina' in v.name.lower() or 'жен' in v.name.lower():
                engine.setProperty('voice', v.id)
                print("Установлен женский голос.")
                return
        if len(ru_voices) > 0:
            engine.setProperty('voice', ru_voices[0].id)

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
    
    # Словарь программ для открытия (настроено для Windows)
    # Чтобы добавить свои, напишите название и путь к .exe файлу
    PROGRAMS = {
        "блокнот": "notepad.exe",
        "калькулятор": "calc.exe",
        "проводник": "explorer.exe",
        "браузер": "start chrome" # Для открытия Google Chrome
    }
    
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

        # --- НОВЫЕ КОМАНДЫ: Смена голоса ---
        elif 'включи мужской голос' in query or 'поставь мужской голос' in query:
            change_voice("male")
            speak("Теперь я говорю так. Надеюсь, вам нравится.")
            
        elif 'включи женский голос' in query or 'поставь женский голос' in query:
            change_voice("female")
            speak("Голос успешно изменен на женский.")
            
        # --- НОВЫЕ КОМАНДЫ: Открытие программ ---
        elif 'запусти' in query or 'открой программу' in query:
            # Ищем название программы из словаря в том, что сказал пользователь
            found = False
            for prog_name, prog_path in PROGRAMS.items():
                if prog_name in query:
                    speak(f"Запускаю {prog_name}")
                    os.system(prog_path)
                    found = True
                    break
            
            if not found:
                speak("Извините, я не знаю такую программу. Добавьте её в мой словарь.")

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