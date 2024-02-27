import datetime
import time
import typing
from bs4 import BeautifulSoup

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
    return the_titles

