from datetime import date, datetime
import math
from wechatpy import WeChatClient
from wechatpy.client.api import WeChatMessage, WeChatTemplate
import requests
import os
import random

today_date = datetime.now().date()
today = today_date.strftime("%Y-%m-%d")
# start_date = os.environ['START_DATE']
# city = os.environ['CITY']
# birthday = os.environ['BIRTHDAY']
# app_id = os.environ["APP_ID"]
# app_secret = os.environ["APP_SECRET"]
# user_id = os.environ["USER_ID"]
# template_id = os.environ["TEMPLATE_ID"]

start_date = "2024-04-16"
birthday = "01-16"
app_id = "wxfb7f0aaa526b0e04"
app_secret = "98f6b1380eea85e0c4053d3bb751a84e"
user_id = "osJgu6yKrvsSeCm2GUVMbRr5mguc"
template_id = "WeOCUO_orubNZwp6Gh9B4v5sXoRmMVFCc8ZRGD8a6Vk"


#def get_weather():
#  url = "http://autodev.openspeech.cn/csp/api/v2.1/weather?openId=aiuicus&clientType=android&sign=android&city=" + city
#  res = requests.get(url).json()
#  weather = res['data']['list'][0]
#  return weather['weather'], math.floor(weather['temp'])

def get_weather():
    response = requests.get("http://t.weather.sojson.com/api/weather/city/101021300")
    
    data = response.json()
    
    wendu = data['data'].get('wendu')  # 提取 data 项目中的 wendu 数据
    
    type = data['data']['forecast'][0].get('type')  # 提取 forecast 中第一天的 type 数据
            
    return type, wendu



def get_count():
  print(f"----------start date: {start_date}")
  delta = datetime.now() - datetime.strptime(start_date, "%Y-%m-%d")
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
