from datetime import date, datetime
import math
from wechatpy import WeChatClient
from wechatpy.client.api import WeChatMessage, WeChatTemplate
import requests
import os
import random
import calendar

today = datetime.now()
# start_date = os.environ['START_DATE']
# city = os.environ['CITY']
# birthday = os.environ['BIRTHDAY']
# app_id = os.environ["APP_ID"]
# app_secret = os.environ["APP_SECRET"]
# user_id = os.environ["USER_ID"]
# template_id = os.environ["TEMPLATE_ID"]

start_date = "2024-04-16"
birthday = "01-16"
btdymd = "1998-01-16"
city = "上海"
app_id = "wxfb7f0aaa526b0e04"
app_secret = "98f6b1380eea85e0c4053d3bb751a84e"
user_id = "osJgu6yKrvsSeCm2GUVMbRr5mguc"
template_id = "ROJ35p8s67vw4Ebq7FU3EtL3KHlyhpAUHMIfqtEpI6M"


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
  delta = datetime.now() - datetime.strptime(start_date, "%Y-%m-%d")
  return delta.days

def get_birthday():
  next = datetime.strptime(str(date.today().year) + "-" + birthday, "%Y-%m-%d")
  if next < datetime.now():
    next = next.replace(year=next.year + 1)
  return (next - today).days

def day_count():
    delta = datetime.now() - datetime.strptime(btdymd, "%Y-%m-%d")
    return delta.days

def get_date():
    date_obj = datetime.now()
    year = date_obj.year
    month = date_obj.month
    day = date_obj.day
    month_names = ['一', '二', '三', '四', '五', '六', '七', '八', '九', '十', '十一', '十二']
    chinese_month = month_names[month - 1]
    chinese_day = calendar.day_name[date_obj.weekday()]
    chinese_date = f"{year}年{month}月{day}日"
    return chinese_date

client = WeChatClient(app_id, app_secret)

wm = WeChatMessage(client)
wea, temperature = get_weather()
data = {
    "weather":{"value":wea},
    "date":{"value":get_date()},
    "temperature":{"value":f"{temperature}°C"},
    "love_days":{"value":get_count()},
    "count":{"value":day_count()},
    "city":{"value":city},
    "birthday_left":{"value":get_birthday()},
}
res = wm.send_template(user_id, template_id[1], data)
print(res)
