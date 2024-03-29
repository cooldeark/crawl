import datetime
import time
import typing
from bs4 import BeautifulSoup
import re
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

def ptt_search():
    # 目標頁面URL
    url = 'https://www.ptt.cc/bbs/HardwareSale/index.html'

    # 發送HTTP請求
    response = requests.get(url)

    # 解析HTML內容
    soup = BeautifulSoup(response.text, 'html.parser')

    # 查找所有文章標題
    titles = soup.find_all('div', class_='title')
    # 创建一个空列表用于存储包含"iphone"的标题
    the_titles = []
    # 正则表达式，不区分大小写
    pattern = re.compile(r'2070|2080|3070|3080', re.IGNORECASE)
    
    for title in titles:
        if  pattern.search(title.text):
            the_titles.append(title.text.strip())
    # ['[賣/全國/郵寄] iPhone 15 Pro Max 256G 黑鈦', '[賣/全國/皆可] iPhone 14 Pro 256G 金', '[徵/高雄/面交] iPhone 15 128G 藍/黑', '[賣/高雄/面交] iPhone14 ProMax', '[賣/雙北/面交] iPhone 11 128G 黑色']

    return the_titles
            

