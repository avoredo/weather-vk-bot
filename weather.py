import pyowm
import time
import datetime
import pytz
import timezonefinder
from geopy.geocoders import Nominatim
from t import key, geokey

owm = pyowm.OWM(key(), language='ru')
geolocator = Nominatim(user_agent=geokey())
tf = timezonefinder.TimezoneFinder()

tm = {'1': 'Утром', '2': 'Днем', '3': 'Вечером', '4': 'Ночью'}

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

def nowcast_coords(lat, long):
    observation = owm.weather_at_coords(lat, long)
    weather = observation.get_weather()
    temp = weather.get_temperature('celsius')['temp']
    location = observation.get_location().get_name()
    status = weather.get_detailed_status()
    try:
        wind_direction = wind(weather.get_wind()['deg'])
    except:
        wind_direction = wind(0)
    wind_speed = str(round(weather.get_wind()['speed'], 1))
    pressure = str(round(0.7500616827 * weather.get_pressure()['press']))
    humidity = str(weather.get_humidity())
    sunrise = str(time.strftime('%H:%M', time.localtime(weather.get_sunrise_time())))
    sunset = str(time.strftime('%H:%M', time.localtime(weather.get_sunset_time())))
    t = round(temp, 1)
    return('🏙️ В городе ' + location.title() + ' сейчас:\n🌡️ ' + str(t) + ' °C, ' + status + '.\n💨 Ветер ' + wind_speed + ' м/с, ' + wind_direction + '\n⛱️ Давление ' + pressure + ' мм рт. ст.\n💧 Влажность ' + humidity + ' %\n 🌅 Восход солнца: ' + sunrise + '\n 🌇 Закат солнца: ' + sunset)

def nowcast_userplace(place):
    observation = owm.weather_at_place(place)
    weather = observation.get_weather()
    temperature = round((weather.get_temperature('celsius')['temp']), 1)
    status = weather.get_detailed_status()
    try:
        wind_direction = wind(weather.get_wind()['deg'])
    except:
        wind_direction = wind(0)
    wind_speed = str(round(weather.get_wind()['speed'], 1))
    pressure = str(round(0.7500616827 * weather.get_pressure()['press']))
    humidity = str(weather.get_humidity())
    sunrise = str(time.strftime('%H:%M', time.localtime(weather.get_sunrise_time())))
    sunset = str(time.strftime('%H:%M', time.localtime(weather.get_sunset_time())))
    return('🏙️ В городе ' + place.title() + ' сейчас:\n🌡️ ' + str(temperature) + ' °C, ' + status + '.\n💨 Ветер ' + wind_speed + ' м/с, ' + wind_direction + '\n⛱️ Давление ' + pressure + ' мм рт. ст.\n💧 Влажность ' + humidity + ' %\n 🌅 Восход солнца: ' + sunrise + '\n 🌇 Закат солнца: ' + sunset)

def tommorow_forecast_userplace(place):
    forecaster = owm.three_hours_forecast(place)
    location = geolocator.geocode(place)
    timezone_str = tf.certain_timezone_at(lat=location.latitude, lng=location.longitude)
    timezone = pytz.timezone(timezone_str)
    tommorow = time.mktime(time.strptime((pytz.utc.localize(datetime.datetime.utcnow(), is_dst=None).astimezone(timezone)  + datetime.timedelta(days=1)).strftime('%d.%m.%Y'), '%d.%m.%Y'))
    text = ['Прогноз погоды в городе ' + place.title() + ' на ' + str(time.strftime('%d.%m.%y', time.localtime(tommorow)))]
    for i in range(4):
        t = int(tommorow + ((i + 1) * 21600))
        weather = forecaster.get_weather_at(t)
        temperature = round((weather.get_temperature('celsius')['temp']), 1)
        status = weather.get_detailed_status()
        try:
            wind_direction = wind(weather.get_wind()['deg'])
        except:
            wind_direction = wind(0)
        wind_speed = str(round(weather.get_wind()['speed'], 1))
        pressure = str(round(0.7500616827 * weather.get_pressure()['press']))
        humidity = str(weather.get_humidity())
        text.append(tm[str(i+1)] + '\n️🌡️ ' + str(temperature) + ' °C, ' + status + '.\n💨 Ветер ' + wind_speed + ' м/с, ' + wind_direction + '\n⛱️ Давление ' + pressure + ' мм рт. ст.\n💧 Влажность ' + humidity + ' %')
    return '\n\n'.join(text)

def tommorow_forecast_coords(lat, long):
    forecaster = owm.three_hours_forecast_at_coords(lat, long)
    timezone_str = tf.certain_timezone_at(lat=lat, lng=long)
    timezone = pytz.timezone(timezone_str)
    tommorow = time.mktime(time.strptime((pytz.utc.localize(datetime.datetime.utcnow(), is_dst=None).astimezone(timezone)  + datetime.timedelta(days=1)).strftime('%d.%m.%Y'), '%d.%m.%Y'))
    text = ['Прогноз погоды в этом месте на ' + str(time.strftime('%d.%m.%y', time.localtime(tommorow)))]
    for i in range(4):
        t = int(tommorow + ((i + 1) * 21600))
        weather = forecaster.get_weather_at(t)
        temperature = round((weather.get_temperature('celsius')['temp']), 1)
        status = weather.get_detailed_status()
        try:
            wind_direction = wind(weather.get_wind()['deg'])
        except:
            wind_direction = wind(0)
        wind_speed = str(round(weather.get_wind()['speed'], 1))
        pressure = str(round(0.7500616827 * weather.get_pressure()['press']))
        humidity = str(weather.get_humidity())
        text.append(tm[str(i+1)] + '\n️🌡️ ' + str(temperature) + ' °C, ' + status + '.\n💨 Ветер ' + wind_speed + ' м/с, ' + wind_direction + '\n⛱️ Давление ' + pressure + ' мм рт. ст.\n💧 Влажность ' + humidity + ' %')
    return '\n\n'.join(text)

def today_forecast_userplace(place):
    forecaster = owm.three_hours_forecast(place)
    location = geolocator.geocode(place)
    timezone_str = tf.certain_timezone_at(lat=location.latitude, lng=location.longitude)
    timezone = pytz.timezone(timezone_str)
    nowtime = int(pytz.utc.localize(datetime.datetime.utcnow(), is_dst=None).astimezone(timezone).strftime('%H'))
    if nowtime < 6:
        today = time.mktime(datetime.datetime.strptime(pytz.utc.localize(datetime.datetime.utcnow(), is_dst=None).astimezone(timezone).strftime('%d.%m.%Y'), "%d.%m.%Y").timetuple())
        text = ['Прогноз погоды в городе ' + place.title() + ' на ' + str(time.strftime('%d.%m.%y', time.localtime(today)))]
        for i in range(4):
            t = int(today + ((i + 1) * 21600))
            weather = forecaster.get_weather_at(t)
            sunrise = str(time.strftime('%H:%M', time.localtime(weather.get_sunrise_time())))
            sunset = str(time.strftime('%H:%M', time.localtime(weather.get_sunset_time())))
            temperature = round((weather.get_temperature('celsius')['temp']), 1)
            status = weather.get_detailed_status()  
            try:
                wind_direction = wind(weather.get_wind()['deg'])
            except:
                wind_direction = wind(0)
            wind_speed = str(round(weather.get_wind()['speed'], 1))
            pressure = str(round(0.7500616827 * weather.get_pressure()['press']))
            humidity = str(weather.get_humidity())
            text.append(tm[str(i+1)] + '\n️🌡️ ' + str(temperature) + ' °C, ' + status + '.\n💨 Ветер ' + wind_speed + ' м/с, ' + wind_direction + '\n⛱️ Давление ' + pressure + ' мм рт. ст.\n💧 Влажность ' + humidity + ' %')
        text.append('🌅 Солнце взойдет в ' + sunrise)
        text.append('🌇 Солнце скроется за горизонтом в ' + sunset)
        return '\n\n'.join(text)
    elif nowtime < 12:
        today = time.mktime(datetime.datetime.strptime(pytz.utc.localize(datetime.datetime.utcnow(), is_dst=None).astimezone(timezone).strftime('%d.%m.%Y'), "%d.%m.%Y").timetuple()) + 21600
        text = ['Прогноз погоды в городе ' + place.title() + ' на ' + str(time.strftime('%d.%m.%y', time.localtime(today)))]
        for i in range(3):
            t = int(today + ((i + 1) * 21600))
            weather = forecaster.get_weather_at(t)
            sunset = str(time.strftime('%H:%M', time.localtime(weather.get_sunset_time())))
            temperature = round((weather.get_temperature('celsius')['temp']), 1)
            status = weather.get_detailed_status()
            try:
                wind_direction = wind(weather.get_wind()['deg'])
            except:
                wind_direction = wind(0)
            wind_speed = str(round(weather.get_wind()['speed'], 1))
            pressure = str(round(0.7500616827 * weather.get_pressure()['press']))
            humidity = str(weather.get_humidity())
            text.append(tm[str(i+2)] + '\n️🌡️ ' + str(temperature) + ' °C, ' + status + '.\n💨 Ветер ' + wind_speed + ' м/с, ' + wind_direction + '\n⛱️ Давление ' + pressure + ' мм рт. ст.\n💧 Влажность ' + humidity + ' %')
        text.append('🌇 Солнце скроется за горизонтом в ' + sunset)
        return '\n\n'.join(text)
    elif nowtime < 18:
        today = time.mktime(datetime.datetime.strptime(pytz.utc.localize(datetime.datetime.utcnow(), is_dst=None).astimezone(timezone).strftime('%d.%m.%Y'), "%d.%m.%Y").timetuple()) + (21600*2)
        text = ['Прогноз погоды в городе ' + place.title() + ' на ' + str(time.strftime('%d.%m.%y', time.localtime(today)))]
        for i in range(2):
            t = int(today + ((i + 1) * 21600))
            weather = forecaster.get_weather_at(t)
            sunset = str(time.strftime('%H:%M', time.localtime(weather.get_sunset_time())))
            temperature = round((weather.get_temperature('celsius')['temp']), 1)
            status = weather.get_detailed_status()
            try:
                wind_direction = wind(weather.get_wind()['deg'])
            except:
                wind_direction = wind(0)
            wind_speed = str(round(weather.get_wind()['speed'], 1))
            pressure = str(round(0.7500616827 * weather.get_pressure()['press']))
            humidity = str(weather.get_humidity())
            text.append(tm[str(i+3)] + '\n️🌡️ ' + str(temperature) + ' °C, ' + status + '.\n💨 Ветер ' + wind_speed + ' м/с, ' + wind_direction + '\n⛱️ Давление ' + pressure + ' мм рт. ст.\n💧 Влажность ' + humidity + ' %')
        text.append('🌇 Солнце скроется за горизонтом в ' + sunset)
        return '\n\n'.join(text)
    else:
        today = time.mktime(datetime.datetime.strptime(pytz.utc.localize(datetime.datetime.utcnow(), is_dst=None).astimezone(timezone).strftime('%d.%m.%Y'), "%d.%m.%Y").timetuple()) + (21600*3)
        text = ['Прогноз погоды в городе ' + place.title() + ' на ' + str(time.strftime('%d.%m.%y', time.localtime(today)))]
        for i in range(1):
            t = int(today + ((i + 1) * 21600))
            weather = forecaster.get_weather_at(t)
            sunset = str(time.strftime('%H:%M', time.localtime(weather.get_sunset_time())))
            temperature = round((weather.get_temperature('celsius')['temp']), 1)
            status = weather.get_detailed_status()
            try:
                wind_direction = wind(weather.get_wind()['deg'])
            except:
                wind_direction = wind(0)
            wind_speed = str(round(weather.get_wind()['speed'], 1))
            pressure = str(round(0.7500616827 * weather.get_pressure()['press']))
            humidity = str(weather.get_humidity())
            text.append(tm[str(i+4)] + '\n️🌡️ ' + str(temperature) + ' °C, ' + status + '.\n💨 Ветер ' + wind_speed + ' м/с, ' + wind_direction + '\n⛱️ Давление ' + pressure + ' мм рт. ст.\n💧 Влажность ' + humidity + ' %')
        text.append('🌇 Солнце скроется за горизонтом в ' + sunset)
        return '\n\n'.join(text)

def today_forecast_coords(lat, long):
    forecaster = owm.three_hours_forecast_at_coords(lat, long)
    timezone_str = tf.certain_timezone_at(lat=lat, lng=long)
    timezone = pytz.timezone(timezone_str)
    nowtime = int(pytz.utc.localize(datetime.datetime.utcnow(), is_dst=None).astimezone(timezone).strftime('%H'))
    if nowtime < 6:
        today = time.mktime(datetime.datetime.strptime(pytz.utc.localize(datetime.datetime.utcnow(), is_dst=None).astimezone(timezone).strftime('%d.%m.%Y'), "%d.%m.%Y").timetuple())
        text = ['Прогноз погоды в этом месте на ' + str(time.strftime('%d.%m.%y', time.localtime(today)))]
        for i in range(4):
            t = int(today + ((i + 1) * 21600))
            weather = forecaster.get_weather_at(t)
            sunrise = str(time.strftime('%H:%M', time.localtime(weather.get_sunrise_time())))
            sunset = str(time.strftime('%H:%M', time.localtime(weather.get_sunset_time())))
            temperature = round((weather.get_temperature('celsius')['temp']), 1)
            status = weather.get_detailed_status()
            try:
                wind_direction = wind(weather.get_wind()['deg'])
            except:
                wind_direction = wind(0)
            wind_speed = str(round(weather.get_wind()['speed'], 1))
            pressure = str(round(0.7500616827 * weather.get_pressure()['press']))
            humidity = str(weather.get_humidity())
            text.append(tm[str(i+1)] + '\n️🌡️ ' + str(temperature) + ' °C, ' + status + '.\n💨 Ветер ' + wind_speed + ' м/с, ' + wind_direction + '\n⛱️ Давление ' + pressure + ' мм рт. ст.\n💧 Влажность ' + humidity + ' %')
            text.append('🌅 Солнце взойдет в ' + sunrise)
        text.append('🌇 Солнце скроется за горизонтом в ' + sunset)
        return '\n\n'.join(text)
    elif nowtime < 12:
        today = time.mktime(datetime.datetime.strptime(pytz.utc.localize(datetime.datetime.utcnow(), is_dst=None).astimezone(timezone).strftime('%d.%m.%Y'), "%d.%m.%Y").timetuple()) + 21600
        text = ['Прогноз погоды в этом месте на ' + str(time.strftime('%d.%m.%y', time.localtime(today)))]
        for i in range(3):
            t = int(today + ((i + 1) * 21600))
            weather = forecaster.get_weather_at(t)
            sunset = str(time.strftime('%H:%M', time.localtime(weather.get_sunset_time())))
            temperature = round((weather.get_temperature('celsius')['temp']), 1)
            status = weather.get_detailed_status()
            try:
                wind_direction = wind(weather.get_wind()['deg'])
            except:
                wind_direction = wind(0)
            wind_speed = str(round(weather.get_wind()['speed'], 1))
            pressure = str(round(0.7500616827 * weather.get_pressure()['press']))
            humidity = str(weather.get_humidity())
            text.append(tm[str(i+2)] + '\n️🌡️ ' + str(temperature) + ' °C, ' + status + '.\n💨 Ветер ' + wind_speed + ' м/с, ' + wind_direction + '\n⛱️ Давление ' + pressure + ' мм рт. ст.\n💧 Влажность ' + humidity + ' %')
            text.append('🌇 Солнце скроется за горизонтом в ' + sunset)
        return '\n\n'.join(text)
    elif nowtime < 18:
        today = time.mktime(datetime.datetime.strptime(pytz.utc.localize(datetime.datetime.utcnow(), is_dst=None).astimezone(timezone).strftime('%d.%m.%Y'), "%d.%m.%Y").timetuple()) + (21600*2)
        text = ['Прогноз погоды в этом месте на ' + str(time.strftime('%d.%m.%y', time.localtime(today)))]
        for i in range(2):
            t = int(today + ((i + 1) * 21600))
            weather = forecaster.get_weather_at(t)
            sunset = str(time.strftime('%H:%M', time.localtime(weather.get_sunset_time())))
            temperature = round((weather.get_temperature('celsius')['temp']), 1)
            status = weather.get_detailed_status()
            try:
                wind_direction = wind(weather.get_wind()['deg'])
            except:
                wind_direction = wind(0)
            wind_speed = str(round(weather.get_wind()['speed'], 1))
            pressure = str(round(0.7500616827 * weather.get_pressure()['press']))
            humidity = str(weather.get_humidity())
            text.append(tm[str(i+3)] + '\n️🌡️ ' + str(temperature) + ' °C, ' + status + '.\n💨 Ветер ' + wind_speed + ' м/с, ' + wind_direction + '\n⛱️ Давление ' + pressure + ' мм рт. ст.\n💧 Влажность ' + humidity + ' %')
            text.append('🌇 Солнце скроется за горизонтом в ' + sunset)
        return '\n\n'.join(text)
    else:
        today = time.mktime(datetime.datetime.strptime(pytz.utc.localize(datetime.datetime.utcnow(), is_dst=None).astimezone(timezone).strftime('%d.%m.%Y'), "%d.%m.%Y").timetuple()) + (21600*3)
        text = ['Прогноз погоды в этом месте на ' + str(time.strftime('%d.%m.%y', time.localtime(today)))]
        for i in range(1):
            t = int(today + ((i + 1) * 21600))
            weather = forecaster.get_weather_at(t)
            sunset = str(time.strftime('%H:%M', time.localtime(weather.get_sunset_time())))
            temperature = round((weather.get_temperature('celsius')['temp']), 1)
            status = weather.get_detailed_status()
            try:
                wind_direction = wind(weather.get_wind()['deg'])
            except:
                wind_direction = wind(0)
            wind_speed = str(round(weather.get_wind()['speed'], 1))
            pressure = str(round(0.7500616827 * weather.get_pressure()['press']))
            humidity = str(weather.get_humidity())
            text.append(tm[str(i+4)] + '\n️🌡️ ' + str(temperature) + ' °C, ' + status + '.\n💨 Ветер ' + wind_speed + ' м/с, ' + wind_direction + '\n⛱️ Давление ' + pressure + ' мм рт. ст.\n💧 Влажность ' + humidity + ' %')
            text.append('🌇 Солнце скроется за горизонтом в ' + sunset)
        return '\n\n'.join(text)  

