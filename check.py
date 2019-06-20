# -*- coding: utf-8 -*-
import time
import requests
import os
import locale

# locale.setlocale(locale.LC_TIME, 'ru_RU')
# os.environ['TZ'] = 'Europe/Moscow'                                          
# time.tzset()

def check(place):
    url = 'https://meteoinfo.ru/hmc-output/meteoalert/map_fed_data.php'

    html = requests.get(url).text                                            
    data = eval(html)                                                       

    places = {
              'орел': '51',
              'воронеж': '77',
              'курск': '33', 
              'калуга': '27', 
              'брянск': '7', 
              'ярославль': '81',
              'смоленск': '60',
              'тамбов': '65',
              'кострома': '36',
              'тверь': '70',
              'владимир': '75',
              'тула': '68',
              'москва': '43',
              'белгород': '6',
              'рязань': '57',
              'липецк': '38',
              'иваново': '19'
      }

    area = data[places[place]]

    intsn = {
          '0': 'Зеленый',
          '1': 'Зеленый',
          '2': 'Желтый',
          '3': 'Оранжевый',
          '4': 'Красный'      
    }
    
    areas = {
          'белгород': 'Белгородская область',
          'брянск': 'Брянская область',
          'владимир': 'Владимирская область',
          'воронеж': 'Воронежская область',
          'иваново': 'Ивановская область',
          'калуга': 'Калужская область',
          'кострома': 'Костромская область',
          'курск': 'Курская область',
          'липецк': 'Липецкая область',
          'москва': 'Московская область',
          'орел': 'Орловская область',
          'рязань': 'Рязанская область',
          'смоленск': 'Смоленская область',
          'тамбов': 'Тамбовская область',
          'тверь': 'Тверская область',
          'тула': 'Тульская область',
          'ярославль': 'Ярославская область'
    }
    length = (len(area))
    text = []
    for k in range(0, length):
          weather = area[str(k)]["3"]
          intensity = str(area[str(k)]['2'])[0]
          start_time = time.strftime('%H:%M %d %B', time.localtime(int(area[str(k)]['0'])))
          end_time = time.strftime('%H:%M %d %B', time.localtime(int(area[str(k)]['1'])))
          if int(time.strftime('%H', time.localtime(int(area[str(k)]['0'])))) == int(time.strftime('%H', time.localtime())):
                start_from = ''
          else:
                start_from = ' c ' + str(start_time)
          r = area[str(k)]['4']
          if r == '':
                remark = 'Уточнений нет'
          else:
                remark = r
          text.append('🗺️ Регион: ' + areas[str(place)] + '\n' + '⚠️ Оповещение: ' + weather + '\n' + '🕑 Период предупреждения — ' + start_from + ' до ' + end_time + '\n' + '📝 Уточнения: ' + remark + '\n' + '❗️ Уровень: ' + intsn[intensity] + '\n')
    return '\n\n'.join(text)
