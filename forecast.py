import pyowm
from t import key
import time

owm = pyowm.OWM(key(), language='ru')

def wind(deg):
    if(deg>337.5): 
        return 'С'
    elif(deg>292.5):
        return 'СЗ'
    elif(deg>247.5):
        return 'З'
    elif(deg>202.5):
        return 'ЮЗ'
    elif(deg>157.5):
        return 'Ю'
    elif(deg>122.5):
        return 'ЮВ'
    elif(deg>67.5):
        return 'В'
    elif(deg>22.5):
        return 'СВ'
    else: 
        return('С')

def nowcast(lat, long):
    place = owm.weather_at_coords(lat, long)
    weather = place.get_weather()
    temp = weather.get_temperature('celsius')['temp']
    location = place.get_location().get_name()
    status = weather.get_detailed_status()
    wind_direction = wind(weather.get_wind()['deg'])
    wind_speed = str(round(weather.get_wind()['speed'], 1))
    pressure = str(round(0.7500616827 * weather.get_pressure()['press']))
    humidity = str(weather.get_humidity())
    sunrise = str(time.strftime('%H:%M', time.localtime(weather.get_sunrise_time())))
    sunset = str(time.strftime('%H:%M', time.localtime(weather.get_sunset_time())))
    t = round(temp, 1)
    return('🏙️ В городе ' + location + ' сейчас:\n🌡️ ' + str(t) + ' °C, ' + status + '.\n💨 Ветер ' + wind_speed + ' м/с, ' + wind_direction + '\n⛱️ Давление ' + pressure + ' мм рт. ст.\n💧 Влажность ' + humidity + ' %\n 🌅 Восход солнца: ' + sunrise + '\n 🌇 Закат солнца: ' + sunset)
