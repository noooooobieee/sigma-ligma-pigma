import config
import telebot
import random

API_TOKEN = config.token

bot = telebot.TeleBot(API_TOKEN)

words = ["апельсин", "банан", "вишня", "груша", "дыня", "ежевика", "жимолость", "зизифус", "ирис", "кактус"]

# Handle '/start' and '/help'
@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    bot.reply_to(message, "щаотапвпоыщ")


# Handle '/игра' command
@bot.message_handler(commands=['игра'])
def start_game(message):
    bot.reply_to(message, """\
Отправь мне слово, и я отвечу словом, начинающимся с последней буквы вашего слова.\
""")


# Handle all other messages with content_type 'text' (content_types defaults to ['text'])
@bot.message_handler(func=lambda message: True)
def play_game(message):
    word = message.text.lower()
    if word:
        last_letter = word[-1]
        response_word = random.choice([w for w in words if w.startswith(last_letter)])
        bot.reply_to(message, response_word)


bot.infinity_polling()