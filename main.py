from datetime import date, datetime
import math
from wechatpy import WeChatClient
from wechatpy.client.api import WeChatMessage, WeChatTemplate
import requests
import os
import random

#获取appid和模板id
app_id = os.environ["APP_ID"]
app_secret = os.environ["APP_SECRET"]

user_id = os.environ["USER_ID"]
template_id = os.environ["TEMPLATE_ID"]

#--------------------自定义部分开始
#获取一些信息（在secret里设置）
today = datetime.now()
start_date = os.environ['START_DATE'] #开始恋爱的日期
city = os.environ['CITY'] #城市（在获取中天气被使用）
birthday = os.environ['BIRTHDAY'] #生日

#获取天气
def get_weather():
  url = "http://autodev.openspeech.cn/csp/api/v2.1/weather?openId=aiuicus&clientType=android&sign=android&city=" + city
  res = requests.get(url).json()
  weather = res['data']['list'][0]
  return weather['weather'], math.floor(weather['temp'])

#获取相恋时长
def get_count():
  delta = today - datetime.strptime(start_date, "%Y-%m-%d")
  return delta.days

#获取生日
def get_birthday():
  next = datetime.strptime(str(date.today().year) + "-" + birthday, "%Y-%m-%d")
  if next < datetime.now():
    next = next.replace(year=next.year + 1)
  return (next - today).days

#获取一段话
def get_words():
  words = requests.get("https://api.shadiao.pro/chp")
  if words.status_code != 200:
    return get_words()
  return words.json()['data']['text']

def get_random_color():
  return "#%06x" % random.randint(0, 0xFFFFFF)

#---------------------自定义部分结束

client = WeChatClient(app_id, app_secret)

wm = WeChatMessage(client)
wea, temperature = get_weather()

#发送的数据
data = {
  "weather":{"value":wea},
  "temperature":{"value":temperature},
  "love_days":{"value":get_count()},
  "birthday_left":{"value":get_birthday()},
  "words":{"value":get_words(), "color":get_random_color()}
}

#发送模板消息
res = wm.send_template(user_id, template_id, data)
print(res)
