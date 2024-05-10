from datetime import date, datetime
import math
from wechatpy import WeChatClient
from wechatpy.client.api import WeChatMessage, WeChatTemplate
import requests
import os
import random

today = datetime.now()
today.strftime("%Y-%m-%d")
start_date = os.environ['START_DATE']
city = os.environ['CITY']
birthday = os.environ['BIRTHDAY']

app_id = os.environ["APP_ID"]
app_secret = os.environ["APP_SECRET"]

user_id = os.environ["USER_ID"]
template_id = os.environ["TEMPLATE_ID"]


#def get_weather():
#  url = "http://autodev.openspeech.cn/csp/api/v2.1/weather?openId=aiuicus&clientType=android&sign=android&city=" + city
#  res = requests.get(url).json()
#  weather = res['data']['list'][0]
#  return weather['weather'], math.floor(weather['temp'])

def get_weather():
    response = requests.get("http://t.weather.sojson.com/api/weather/city/101021300")
    
    if response.status_code == 200:
        data = response.json()
        
        for day in data['data']['forecast']:
            if day['ymd'] == today:
                date = day['date']
                high_temp = int(day['high'].split()[1][:-1])  # 提取最高气温的数值部分
                low_temp = int(day['low'].split()[1][:-1])  # 提取最低气温的数值部分
                weather_type = day['type']
                
                average_temp = (high_temp + low_temp) / 2
                
                result = {
                    'weather_type': weather_type,
                    'temperature': average_temp
                }
                
                return result
    
    return None



def get_count():
  delta = today - datetime.strptime(start_date, "%Y-%m-%d")
  return delta.days

def get_birthday():
  next = datetime.strptime(str(date.today().year) + "-" + birthday, "%Y-%m-%d")
  if next < datetime.now():
    next = next.replace(year=next.year + 1)
  return (next - today).days

def get_words():
  words = requests.get("https://api.shadiao.pro/chp")
  if words.status_code != 200:
    return get_words()
  return words.json()['data']['text']

def get_random_color():
  return "#%06x" % random.randint(0, 0xFFFFFF)


client = WeChatClient(app_id, app_secret)

wm = WeChatMessage(client)
wea, temperature = get_weather()
data = {"weather":{"value":wea},"temperature":{"value":temperature},"love_days":{"value":get_count()},"birthday_left":{"value":get_birthday()},"words":{"value":get_words(), "color":get_random_color()}}
res = wm.send_template(user_id, template_id, data)
print(res)
