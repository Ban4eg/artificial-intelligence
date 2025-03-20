import re
import random
import datetime

DAYS_RU = {
    "Monday": "понедельник",
    "Tuesday": "вторник",
    "Wednesday": "среда",
    "Thursday": "четверг",
    "Friday": "пятница",
    "Saturday": "суббота",
    "Sunday": "воскресенье",
}
# Определяем словарь шаблонов и ответов
responses = {
    r"привет": "Привет! Чем могу помочь?",
    r"как тебя зовут\??": "Меня зовут ассистент Олег. Рад знакомству!",
    r"как дела\??": "Отлично! А когда вы написали, стало еще лучше! Как у вас дела?",
    r"хорошо": "Это здорово! Я за вас очень рад! Если у вас есть какие-нибудь вопросы, обращайтесь, буду рад помочь!",
    r"спасибо": "Рад, что смог помочь! Обращайтесь еще, если будут вопросы!",
    r"что ты умеешь\??": "Я могу отвечать на вопросы о времени, дне недели, числе месяца, своих функциях и делать простые арифметические операции, такие как сложение, умножение, вычитание и деление(для этого введите 'сколько будет ...?'.",
    r"который час\??": lambda _: datetime.datetime.now().strftime("Сейчас %H:%M."),
    r"какое сегодня число\??": lambda _: datetime.datetime.now().strftime("Сегодня %d.%m.%Y."),
    r"какой сегодня день недели\??": lambda _: f"Сегодня {DAYS_RU[datetime.datetime.now().strftime('%A')]}.",

    r"сколько будет (?P<num1>\d+)\s*\+\s*(?P<num2>\d+)\??": lambda m: f"{int(m.group('num1')) + int(m.group('num2'))}",
    r"сколько будет (?P<num1>\d+)\s*-\s*(?P<num2>\d+)\??": lambda m: f"{int(m.group('num1')) - int(m.group('num2'))}",
    r"сколько будет (?P<num1>\d+)\s*\*\s*(?P<num2>\d+)\??": lambda m: f"{int(m.group('num1')) * int(m.group('num2'))}",
    r"сколько будет (?P<num1>\d+)\s*/\s*(?P<num2>\d+)\??": lambda m: (
        "Ошибка: деление на ноль!" if int(m.group("num2")) == 0 else f"{int(m.group('num1')) / int(m.group('num2'))}"
    ),
}





def chatbot_response(text):
    text = text.lower()
    for pattern, response in responses.items():
        match = re.search(pattern, text)
        if match:
            if callable(response):
                return response(match)
            elif "{location}" in response:
                return response.format(location=match.group("location"))
            else:
                return response
    return random.choice(["Я не понял вопроса.", "Попробуйте перефразировать.", "К сожалению, я пока не умею обрабатывать все запросы, попробуйте ввести другой вопрос.",])

if __name__ == "__main__":
    print("Введите 'выход' для завершения диалога.")
    while True:
        user_input = input("Вы: ")
        if user_input.lower() == "выход":
            print("Бот: До свидания!")
            break
        print("Бот:", chatbot_response(user_input))
