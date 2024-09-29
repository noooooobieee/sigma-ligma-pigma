import telebot
from config import *
from logic import *

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def handle_start(message):
    bot.send_message(message.chat.id, "Привет! Я бот, который может показывать города на карте. Напиши /help для списка команд.")

@bot.message_handler(commands=['help'])
def handle_help(message):
    bot.send_message(message.chat.id, "Доступные команды: /start, /help, /show_city, /remember_city, /show_my_cities")


@bot.message_handler(commands=['show_city'])
def handle_show_city(message):
    city_name = message.text.split()[-1]
    coordinates = manager.get_coordinates(city_name)
    if coordinates:
        lat, lng = coordinates
        fig = plt.figure(figsize=(5, 5))
        ax = fig.add_subplot(1, 1, 1, projection=ccrs.PlateCarree())
        ax.coastlines()
        ax.gridlines()
        ax.plot(lng, lat, 'ro')  # mark city with a red dot
        ax.text(lng, lat, city_name, fontsize=10)  # add city name
        plt.savefig('city_map.png')
        bot.send_photo(message.chat.id, open('city_map.png', 'rb'))
    else:
        bot.send_message(message.chat.id, 'Такого города я не знаю. Убедись, что он написан на английском!')


@bot.message_handler(commands=['remember_city'])
def handle_remember_city(message):
    user_id = message.chat.id
    city_name = message.text.split()[-1]
    if manager.add_city(user_id, city_name):
        bot.send_message(message.chat.id, f'Город {city_name} успешно сохранен!')
    else:
        bot.send_message(message.chat.id, 'Такого города я не знаю. Убедись, что он написан на английском!')

@bot.message_handler(commands=['show_my_cities'])
def handle_show_visited_cities(message):
    cities = manager.select_cities(message.chat.id)
    if cities:
        manager.create_graph('cities_map.png', cities)
        bot.send_photo(message.chat.id, open('cities_map.png', 'rb'))
    else:
        bot.send_message(message.chat.id, 'Вы не сохранили ни одного города.')


if __name__=="__main__":
    manager = DB_Map(DATABASE)
    bot.polling()
