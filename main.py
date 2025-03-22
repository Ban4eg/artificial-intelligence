import re
import random
import datetime
import webbrowser
import requests  # Для работы с API

with open("chat_log.txt", "w", encoding="utf-8") as log_file:
    log_file.write("Лог чата\n")
    log_file.write("=" * 40 + "\n")

API_KEY = "16096f9c40048c4f62d4bdba2b5f73ce"

DAYS_RU = {
    "Monday": "понедельник",
    "Tuesday": "вторник",
    "Wednesday": "среда",
    "Thursday": "четверг",
    "Friday": "пятница",
    "Saturday": "суббота",
    "Sunday": "воскресенье",
}

responses = {
    r"привет": [
        "Привет! Как у вас дела?",
        "Здравствуйте! Чем могу помочь?",
        "Приветствую! Хорошего дня!"
    ],
    r"как тебя зовут\??": [
        "Меня зовут ассистент Олег. Рад знакомству!",
        "Я Олег, ваш виртуальный помощник.",
        "Просто Олег. Чем могу помочь?"
    ],
    r"как дела\??": [
        "Отлично! А у вас как?",
        "Прекрасно, спасибо! Как у вас?",
        "Замечательно! Надеюсь, у вас тоже всё хорошо!",
        "Хорошо, спасибо! Как у вас?",
        "Отлично! Рад вас слышать!"
    ],
    r"хорошо": [
        "Это здорово! Если есть вопросы, спрашивайте!",
        "Рад за вас! Чем могу помочь?",
        "Замечательно! Если что-то нужно, обращайтесь!"
    ],
    r"спасибо": [
        "Рад помочь!",
        "Обращайтесь ещё!",
        "Всегда рад помочь!"
    ],
    r"что ты умеешь\??": [
        "Я могу отвечать на вопросы о времени, дне недели, числе месяца и делать простые расчёты.",
        "Я умею рассказывать про дату, время и решать простые арифметические примеры."
    ],
    r"который час\??": lambda _: datetime.datetime.now().strftime("Сейчас %H:%M."),
    r"какое сегодня число\??": lambda _: datetime.datetime.now().strftime("Сегодня %d.%m.%Y."),
    r"какой сегодня день недели\??": lambda _: f"Сегодня {DAYS_RU[datetime.datetime.now().strftime('%A')]}.",

    r"погода в (.+)": lambda m: get_weather(m.group(1)),
}


def log_dialog(user_input, bot_response):
    with open("chat_log.txt", "a", encoding="utf-8") as log_file:
        log_file.write(f"Пользователь: {user_input}\n")
        log_file.write(f"Бот: {bot_response}\n")
        log_file.write("-" * 40 + "\n")


def search_web(query):
    url = f"https://www.google.com/search?q={query}"
    webbrowser.open(url)
    return f"Открываю браузер с результатами поиска: {query}"


def get_weather(city):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric&lang=ru"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        temp = data["main"]["temp"]
        weather_desc = data["weather"][0]["description"]
        return f"В городе {city} сейчас {weather_desc} при температуре {temp}°C."
    else:
        return "Не удалось получить информацию о погоде. Попробуйте другой город."


def chatbot_response(text):
    text = text.lower()

    match = re.search(r"поиск\s+(.+)", text, re.IGNORECASE)
    if match:
        query = match.group(1)
        response = search_web(query)
        log_dialog(text, response)
        return response

    for pattern, response in responses.items():
        match = re.search(pattern, text)
        if match:
            if callable(response):
                bot_response = response(match)
            elif isinstance(response, list):
                bot_response = random.choice(response)
            else:
                bot_response = response

            log_dialog(text, bot_response)
            return bot_response

    bot_response = random.choice([
        "Я не понял вопроса.",
        "Попробуйте перефразировать.",
        "К сожалению, я пока не умею обрабатывать все запросы, попробуйте ввести другой вопрос."
    ])
    log_dialog(text, bot_response)
    return bot_response


if __name__ == "__main__":
    print("Введите 'выход' для завершения диалога.")
    while True:
        user_input = input("Вы: ")
        if user_input.lower() == "выход":
            print("Бот: До свидания!")
            log_dialog(user_input, "До свидания!")
            break
        bot_reply = chatbot_response(user_input)
        print("Бот:", bot_reply)
