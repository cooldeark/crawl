import datetime
import time
import typing
from bs4 import BeautifulSoup
import json

# line sdk
# from linebot import LineBotApi
# from linebot.models import TextSendMessage

# pandas主要用在sql
import pandas as pd
import requests
from loguru import logger
from financialdata.schema.dataset import (
    check_schema,
)

from financialdata.config import (
    LINE_BOT_TOKEN
)

# 這裡的typing.Dict表示parameter是一個字典。字典的鍵（key）是字符串（str），而值（value）是一個列表（typing.List）。這個列表中的元素可以是字符串（str）、整數（int）或浮點數（float），這由typing.Union[str, int, float]表示。
# e.g.
# {
#     "key1": ["string", 10, 20.5],
#     "key2": ["another string", 30, 40.6]
# }
# 所以typing.dict 類似於 "str": ["test",1,2] , typing.list類似於 ["test",1,2]
def crawler(
    parameter: typing.Dict[
        str,
        typing.List[
            typing.Union[
                str, int, float
            ]
        ],
    ]
) -> pd.DataFrame:
    logger.info(parameter)
    date = parameter.get("date", "")
    data_source = parameter.get(
        "data_source", ""
    )
    if data_source == "twse":
        df = crawler_twse(date)
    elif data_source == "tpex":
        df = crawler_tpex(date)
    df = check_schema(
        df.copy(),
        dataset="TaiwanStockPrice",
    )
    return df

def test():
    # 目標頁面URL
    url = 'https://www.ptt.cc/bbs/mobilesales/index.html'

    # 發送HTTP請求
    response = requests.get(url)

    # 解析HTML內容
    soup = BeautifulSoup(response.text, 'html.parser')

    # 查找所有文章標題
    titles = soup.find_all('div', class_='title')
    # 创建一个空列表用于存储包含"iphone"的标题
    the_titles = []
    # 迭代每個標題，檢查是否包含"iphone"關鍵字
    for title in titles:
        if 'iphone' in title.text.lower():
            the_titles.append(title.text.strip())
    # ['[賣/全國/郵寄] iPhone 15 Pro Max 256G 黑鈦', '[賣/全國/皆可] iPhone 14 Pro 256G 金', '[徵/高雄/面交] iPhone 15 128G 藍/黑', '[賣/高雄/面交] iPhone14 ProMax', '[賣/雙北/面交] iPhone 11 128G 黑色']
    # """
    # 透過 LINE Notify 發送 LINE 訊息
    # """
    # 這裡填入你從 LINE Developers 頁面獲得的 Access Token
    # 您的 Channel Access Token
    line_channel_access_token = LINE_BOT_TOKEN

    # LINE Messaging API 的推送消息 API URL
    line_push_api = 'https://api.line.me/v2/bot/message/push'

    # 设置请求头
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {line_channel_access_token}'
    }

    # 构建请求数据
    data = {
        "to": "Ua2cde922e74b8c37942f45b54bf5388c",  # 替换为目标用户的 LINE ID，這裡現在是我自己
        "messages": [
            {
                "type": "text",
                "text": "Hello, world"  # 您想发送的消息内容
            }
        ]
    }

    # 发送 POST 请求
    response = requests.post(line_push_api, headers=headers, data=json.dumps(data))

    # 打印响应状态和内容，以便调试
    print(response.status_code, response.text)
    

    # line sdk
    # 替换为您的 Channel access token
    # line_bot_api = LineBotApi('')

    # 替换为接收者的用户ID
    # user_id = '接收者的用户ID'

    # 发送消息
    # try:
    #     line_bot_api.push_message(user_id, TextSendMessage(text='Hello, this is a message from my LINE bot!'))
    #     print("Message sent!")
    # except Exception as e:
    #     print(f"An error occurred: {e}")
            

