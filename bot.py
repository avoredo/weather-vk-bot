from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
import vk_api
import random
import time
import requests
import datetime
from vk_api import VkUpload
from bs4 import BeautifulSoup
from t import token, group
from weather import data

vk = vk_api.VkApi(token=token())
vk._auth_token()

vk.get_api()

longpoll = VkBotLongPoll(vk, group())

commands = 'Список команд:\n!чек Ваш_город - Проверить предупреждения по вашей области\n!цфо - Сводка прогнозов по ЦФО\n!карта - Прогностическая карта\n!инфо - Подробности о предупрждениях\n!легенда - Легенда карты для !карта'

text_info = 'Зелёный - оповещения о погоде не требуется\n\nЖёлтый - погода потенциально опасна\n\nОранжевый - погода опасна. Имеется вероятность стихийных бедствий, нанесения ущерба\n\n \
             Красный - погода очень опасна. Имеется вероятность крупных разрушений и катастроф'

def save_img(url):
    img_data = requests.get(url).content
    f = 'img' + str(time.time()) + '.jpg'
    with open(f, 'wb') as handler:
        handler.write(img_data)
    return(f)

def photo(file):
    upload = vk.method("photos.getMessagesUploadServer")
    r = requests.post(upload['upload_url'], files={'photo': open(file, 'rb')}).json()
    save = vk.method('photos.saveMessagesPhoto', {'photo': r['photo'], 'server': r['server'], 'hash': r['hash']})
    owner_id = save[0]["owner_id"]
    id_own = save[0]["id"]
    attachment ='photo{}_{}'.format(owner_id,id_own)
    return attachment

while True:
    try:
        for event in longpoll.listen():
            if event.type == VkBotEventType.MESSAGE_NEW:
                if event.object.peer_id != event.object.from_id:
                    if event.object.text.lower() == '!команды':
                        vk.method('messages.send', {'peer_id': event.object.peer_id, 'message': commands, 'random_id': random.randint(-2147483648, 2147483647)})
                    elif event.object.text.lower().split()[0] == '!чек':
                        place = event.object.text.lower().split()[1]
                        vk.method('messages.send', {'peer_id': event.object.peer_id, 'message': data(place), 'random_id': random.randint(-2147483648, 2147483647)})   
                    elif event.object.text.lower() == '!цфо':
                        timestamp = datetime.datetime.now().isoformat()
                        img_url = 'https://meteoinfo.ru/hmc-input/cfo/cfo_1.png'
                        pic_url = '{0}?a={1}'.format(img_url, timestamp)
                        html = requests.get('https://meteoinfo.ru/cfo').text
                        soup = BeautifulSoup(html, 'lxml')
                        cfo_text = soup.find('div', id='div_1').find_all('table')[1].text
                        vk.method('messages.send', {'peer_id': event.object.peer_id, 'message': cfo_text, 'attachment': photo(save_img(pic_url)), 'random_id': random.randint(-2147483648, 2147483647)})
                    elif event.object.text.lower() == '!карта':
                        timestamp = datetime.datetime.now().isoformat()
                        img_url = 'https://meteoinfo.ru/hmc-input/egmb/egmb.png'
                        pic_url = '{0}?a={1}'.format(img_url, timestamp)
                        vk.method('messages.send', {'peer_id': event.object.peer_id, 'message': 'Карта прогноза погоды\nДля вызова легенды карты воспользуйтесь !легенда', 'attachment': photo(save_img(pic_url)), 'random_id': random.randint(-2147483648, 2147483647)})
                elif event.object.peer_id == event.object.from_id:
                    if event.object.text.lower() == '!команды':
                        vk.method('messages.send', {'peer_id': event.object.from_id, 'message': commands, 'random_id': random.randint(-2147483648, 2147483647)})
                    elif event.object.text.lower().split()[0] == '!чек':
                        place = event.object.text.lower().split()[1]
                        vk.method('messages.send', {'peer_id': event.object.from_id, 'message': data(place), 'random_id': random.randint(-2147483648, 2147483647)})
                    elif event.object.text.lower() == '!цфо':
                        timestamp = datetime.datetime.now().isoformat()
                        img_url = 'https://meteoinfo.ru/hmc-input/cfo/cfo_1.png'
                        pic_url = '{0}?a={1}'.format(img_url, timestamp)
                        html = requests.get('https://meteoinfo.ru/cfo').text
                        soup = BeautifulSoup(html, 'lxml')
                        cfo_text = soup.find('div', id='div_1').find_all('table')[1].text
                        vk.method('messages.send', {'peer_id': event.object.from_id, 'message': cfo_text, 'attachment': photo(save_img(pic_url)), 'random_id': random.randint(-2147483648, 2147483647)})
                    elif event.object.text.lower() == '!карта':
                        timestamp = datetime.datetime.now().isoformat()
                        img_url = 'https://meteoinfo.ru/hmc-input/egmb/egmb.png'
                        pic_url = '{0}?a={1}'.format(img_url, timestamp)
                        vk.method('messages.send', {'peer_id': event.object.from_id, 'message': 'Карта прогноза погоды\nДля вызова легенды карты воспользуйтесь !легенда', 'attachment': photo(save_img(pic_url)), 'random_id': random.randint(-2147483648, 2147483647)})
    except Exception as e:
        print(e)
        time.sleep(1)