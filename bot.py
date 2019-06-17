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

while True:
    try:
        for event in longpoll.listen():
            if event.type == VkBotEventType.MESSAGE_NEW:
                if event.object.peer_id != event.object.from_id:
                    if event.object.text.lower().split()[0] == '!чек':
                        place = event.object.text.lower().split()[1]
                        vk.method('messages.send', {'peer_id': event.object.peer_id, 'message': data(place), 'random_id': random.randint(-2147483648, 2147483647)})
                elif event.object.peer_id == event.object.from_id:
                    if event.object.text.lower().split()[0] == '!чек':
                        place = event.object.text.lower().split()[1]
                        vk.method('messages.send', {'peer_id': event.object.from_id, 'message': data(place), 'random_id': random.randint(-2147483648, 2147483647)})
    except Exception as e:
        print(e)
        time.sleep(1)