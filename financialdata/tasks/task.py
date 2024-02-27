import importlib
import typing

from financialdata.backend import db
from financialdata.tasks.worker import app


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
    db.upload_data(df, db_dataset.get(dataset), db.router.mysql_financialdata_conn)

@app.task()
# 在使用Celery時，並不是每個函數前都需要添加@app.task()裝飾器。@app.task()裝飾器是用來將一個函數變成Celery的任務（task），這樣它就可以被Celery的工作者（worker）異步執行。你只需要在你希望異步執行的函數前面加上這個裝飾器
def ptt_crawler():
    # 使用 getattr, importlib,
    # 根據不同 dataset, 使用相對應的 crawler 收集資料
    # 爬蟲
    # df = getattr(
    #     importlib.import_module(f"financialdata.crawler.ptt_tw"),
    #     "crawler",
    # )(parameter=parameter)
    # 上傳資料庫
    # db_dataset = dict(
    #     taiwan_stock_price="TaiwanStockPrice",
    #     taiwan_futures_daily="TaiwanFuturesDaily",
    # )
    # db.upload_data(df, db_dataset.get(dataset), db.router.mysql_financialdata_conn)
    df = getattr(importlib.import_module(f"financialdata.crawler.ptt_tw"), "test")()
    
