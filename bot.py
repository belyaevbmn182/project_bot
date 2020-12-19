import telebot
import requests
import random
import datetime


bot = telebot.TeleBot('1491893559:AAGPvYgAqUjbHtrQ3RygHtGCQFL8n9TQQII')
url = ('http://newsapi.org/v2/top-headlines?'
       'country=us&'
       'apiKey=da5eb0d561a04504aa7c2f99fde19cd1')

weather = ('api.openweathermap.org/data/2.5/weather?q={city name}&appid={c15ad7544f8834d6b25659bb6a203b3c}')

request_done = 0

keyboard1 = telebot.types.ReplyKeyboardMarkup(True, True)
keyboard1.row('Погода', 'Новости')
keyboard1.row('Время', 'Музыка')

keyboard2 = telebot.types.ReplyKeyboardMarkup(True, True)
keyboard2.row('Россия', 'США')
keyboard2.row('Великобритания')

@bot.message_handler(commands=['start'])

def start_message(message):
    bot.send_message(message.chat.id, 'Привет, ты написал мне /start.', reply_markup = keyboard1)
    
try:
    
    @bot.message_handler(content_types=['text'])
    def send_text(message):
        global request_done
        
        
        if message.text.lower() == 'погода':
            bot.send_message(message.chat.id, 'Погоду в каком городе вы хотите узнать?', reply_markup = None)
            request_done = 2
        
        elif request_done == 2 and len(message.text.lower()) > 0:
            weather = (f'http://api.openweathermap.org/data/2.5/weather?q={message.text.lower()}&appid=c15ad7544f8834d6b25659bb6a203b3c')
            response = requests.get(weather)
            m = response.json()
            if 'message' in m:
                bot.send_message(message.chat.id, 'Город не найден. Попробуйте ещё раз.', reply_markup = keyboard1)
            else:
                bot.send_message(message.chat.id, f'Информация о городе {message.text}:', reply_markup = keyboard1)
                bot.send_message(message.chat.id, f'Погода: {m["weather"][0]["main"]}', reply_markup = keyboard1)
                tempC = round(int(m["main"]["temp"])) - 273
                bot.send_message(message.chat.id, f'Температура: {tempC} C°', reply_markup = keyboard1)
                bot.send_message(message.chat.id, f'Скорость ветра: {m["wind"]["speed"]} м/сек', reply_markup = keyboard1)
                request_done = 0
            
        elif message.text.lower() == 'время':
            bot.send_message(message.chat.id, 'Время в каком городе вы хотите узнать?', reply_markup = None)
            request_done = 3
        
        elif request_done == 3 and len(message.text.lower()) > 0:
            weather = (f'http://api.openweathermap.org/data/2.5/weather?q={message.text.lower()}&appid=c15ad7544f8834d6b25659bb6a203b3c')
            response = requests.get(weather)
            m = response.json()
            if 'message' in m:
                bot.send_message(message.chat.id, 'Город не найден. Попробуйте ещё раз.', reply_markup = keyboard1)
            else:
                k = int(m["timezone"]) // 3600
                u = str(datetime.datetime.now())
                u = u.split(' ')[1].split(':')[:2]
                u[0] = int(u[0]) - 3
                u[1] = int(u[1])
                u[0] += k
                bot.send_message(message.chat.id, f'Время в городе {message.text}: {u[0]}:{u[1]}', reply_markup = keyboard1)
                request_done = 0
            
        elif message.text.lower() == 'музыка':
            bot.send_message(message.chat.id, 'Переходи по ссылке и наслаждайся новыми плейлистами каждый день в Яндекс.Музыке. \n https://music.yandex.ru/users/yamusic-daily/playlists/64843208')
            
        elif message.text.lower() == 'новости':
            bot.send_message(message.chat.id, 'Новости какой страны вы хотите увидеть?', reply_markup = keyboard2)
            request_done = 1
            
        elif message.text.lower() == 'россия' and request_done == 1:
            url = ('http://newsapi.org/v2/top-headlines?'
            'country=ru&'
            'apiKey=da5eb0d561a04504aa7c2f99fde19cd1')
            response = requests.get(url)
            x = response.json()
            a = random.randint(0, len(x['articles'])-1)
            bot.send_message(message.chat.id, x['articles'][a]['title'])
            bot.send_message(message.chat.id, x['articles'][a]['description'])
            bot.send_photo(message.chat.id, x['articles'][a]['urlToImage'], reply_markup = keyboard1)
            request_done = 0
            
        elif message.text.lower() == 'сша' and request_done == 1:
            url = ('http://newsapi.org/v2/top-headlines?'
            'country=us&'
            'apiKey=da5eb0d561a04504aa7c2f99fde19cd1')
            response = requests.get(url)
            x = response.json()
            a = random.randint(0, len(x['articles'])-1)
            bot.send_message(message.chat.id, x['articles'][a]['title'])
            bot.send_message(message.chat.id, x['articles'][a]['description'])
            bot.send_photo(message.chat.id, x['articles'][a]['urlToImage'], reply_markup = keyboard1)
            request_done = 0
        
        elif message.text.lower() == 'великобритания' and request_done == 1:
            url = ('http://newsapi.org/v2/top-headlines?'
            'country=gb&'
            'apiKey=da5eb0d561a04504aa7c2f99fde19cd1')
            response = requests.get(url)
            x = response.json()
            a = random.randint(0, len(x['articles'])-1)
            bot.send_message(message.chat.id, x['articles'][a]['title'])
            bot.send_message(message.chat.id, x['articles'][a]['description'])
            bot.send_photo(message.chat.id, x['articles'][a]['urlToImage'], reply_markup = keyboard1)
            request_done = 0       
            

    bot.polling()

except BaseException:
    pass