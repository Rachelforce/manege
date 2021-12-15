from telebot import types, TeleBot
from telebot.types import InputMediaPhoto


class Answer:
    def __init__(self, text, state):
        self.text = text
        self.state = state


class State:
    def __init__(self, phrase, answers, photos=None):
        self.phrase = phrase
        self.answers = answers
        self.keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        self.photos = photos
        for el in self.answers:
            self.keyboard.add(el)

    def check_answer(self, user, text):
        if text in self.answers:
            bot.send_message(user, self.answers[text].text, reply_markup=self.keyboard, parse_mode='Markdown')
            user_state[user] = self.answers[text].state

    def process_state(self, user):
        if self.photos:
            bot.send_media_group(user, self.photos)
        bot.send_message(user, self.phrase, reply_markup=self.keyboard, parse_mode='Markdown')


class TextState(State):
    def __init__(self, phrase, answers, true_answer, photos=None):
        self.true_answer = true_answer
        super().__init__(phrase, answers, photos)

    def check_answer(self, user, text):
        if text in self.answers:
            bot.send_message(user, self.answers[text].text, reply_markup=self.keyboard, parse_mode='Markdown')
            user_state[user] = self.answers[text].state
        elif text == self.true_answer:
            bot.send_message(user, "✅ Верно")
            user_state[user] += 1
        else:
            bot.send_message(user, "❌ Не верно")


TOKEN = '5002248438:AAEKWkH7es4Z5Y-4dx9WjtQalWbSbsy5jG4'
bot = TeleBot(TOKEN)

user_state = {}
states = list(range(8))

states[0] = State("📋 Вы в главном меню", {
    "🧩 Начать квест": Answer("Вы Начали квест.", 1),
    "🎧 Прослушать аудиогид по выставке":
        Answer("https://izi.travel/en/browse/76ad97a7-3969-4427-a0c7-08b20490d65f?lang=ru", 0),
    "🎵 Послушать саундтрек к выставке":
        Answer("https://batagov.lnk.to/pokoiiradost", 0)
})

states[1] = State(
    "Перед тем, как начать квест, предлагаем вам ознакомиться с основной [информацией](https://telegra.ph/Mezhmuzejnyj-vystavochnyj-proekt-Pokoj-i-Radost-12-09) о выставке.",
    {
        "➡️Далее": Answer("Начали!", 2),
        "✖️Выход": Answer("✖️Выход", 0)
    },
)

states[2] = State(
    "Выбрать 3 картины, по ним краткая информация и вопросы к каждой. Нужно выбрать верный вариант",
    {
        "Ответ 1": Answer("❌ Не верно", 2),
        "Ответ 2": Answer("✅ Верно!", 3),
        "Ответ 3": Answer("❌ Не Верно!", 2),
        "✖️Выход": Answer("✖️Выход", 0)
    },
    [InputMediaPhoto(
        "https://downloader.disk.yandex.ru/preview/fab60992e44aabd16ff2adb7fcfa0b7c324ccd47c8e20cb5029d8e01a0b332e2/61b75c93/Hjn4m-wXOYrmpEF122iuJx_x_h9wvyWxUIe_ey95botkc_a-HMz1pNWKuHBgtrVqmSOdoSKyWUorppGJJvVltw%3D%3D?uid=0&filename=DSC00926.jpg&disposition=inline&hash=&limit=0&content_type=image%2Fjpeg&owner_uid=0&tknv=v2&size=882x927"), ]
)
states[3] = TextState(
    "Загадана какая-то картина и нужно найти ее и отправить ответ: автор, название картины. ответ - 123",
    {"✖️Выход": Answer("✖️Выход", 0)},
    "123", [InputMediaPhoto(
        "https://downloader.disk.yandex.ru/preview/fab60992e44aabd16ff2adb7fcfa0b7c324ccd47c8e20cb5029d8e01a0b332e2/61b75c93/Hjn4m-wXOYrmpEF122iuJx_x_h9wvyWxUIe_ey95botkc_a-HMz1pNWKuHBgtrVqmSOdoSKyWUorppGJJvVltw%3D%3D?uid=0&filename=DSC00926.jpg&disposition=inline&hash=&limit=0&content_type=image%2Fjpeg&owner_uid=0&tknv=v2&size=882x927"), ]

)


@bot.message_handler(commands=['start'])
def command_help(message):
    user = message.chat.id
    user_state[user] = 0
    bot.send_message(user,
                     "Добро пожаловать в телеграм-бот, который был создан специально для выставки «Покой и Радость» участниками программы для подростков Манеж Junior.",
                     reply_markup=states[0].keyboard)


@bot.message_handler(content_types=['text'])
def default_command(message):
    user = message.chat.id
    text = message.text
    if user not in user_state:
        user_state[user] = 0
    states[user_state[user]].check_answer(user, text)
    states[user_state[user]].process_state(user)


bot.polling()
