import importlib
import typing
import requests
import json
from loguru import logger
from financialdata.backend import db
from financialdata.tasks.worker import app
from financialdata.config import (
    LINE_BOT_TOKEN
)

def sendMessage (message: str):
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
                "text": message  # 您想发送的消息内容
            }
        ]
    }

    # 发送 POST 请求
    response = requests.post(line_push_api, headers=headers, data=json.dumps(data))
    logger.info(f"Line status : , {response.status_code} : {response.text}")
    
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


# 註冊 task, 有註冊的 task 才可以變成任務發送給 rabbitmq
@app.task()
def crawler(dataset: str, parameter: typing.Dict[str, str]):
    # 使用 getattr, importlib,
    # 根據不同 dataset, 使用相對應的 crawler 收集資料
    # 爬蟲
    df = getattr(
        importlib.import_module(f"financialdata.crawler.{dataset}"),
        "crawler",
    )(parameter=parameter)
    # 上傳資料庫
    db_dataset = dict(
        taiwan_stock_price="TaiwanStockPrice",
        taiwan_futures_daily="TaiwanFuturesDaily",
    )
    # 如果 dataset 的值是 "taiwan_stock_price"，則 db_dataset.get(dataset) 將返回 "TaiwanStockPrice"，如果你給予得值不是兩項中的其中一項，他會回傳null
    db.upload_data(df, db_dataset.get(dataset), db.router.mysql_financialdata_conn)

@app.task()
# 在使用Celery時，並不是每個函數前都需要添加@app.task()裝飾器。@app.task()裝飾器是用來將一個函數變成Celery的任務（task），這樣它就可以被Celery的工作者（worker）異步執行。你只需要在你希望異步執行的函數前面加上這個裝飾器
def ptt_crawler():
    getTitleResult = json.dumps(getattr(importlib.import_module(f"financialdata.crawler.ptt_tw"), "ptt_search")())
    finalSend = db.search_ptt(getTitleResult, db.router.mysql_ptt_conn)
    sendMessage(finalSend)
    
