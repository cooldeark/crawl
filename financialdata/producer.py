import importlib
import sys

from loguru import logger

from financialdata.backend import db
from financialdata.tasks.task import crawler, ptt_crawler
# 可以指定型別，也能讓他為null
from typing import Optional

def Update(dataset: Optional[str] = None, start_date: Optional[str] = None, end_date: Optional[str] = None):
    if dataset == "ptt_crawl":
        # 创建一个 Celery 任务。这里，crawler.s 是 Celery 的签名（signature）方法，用于创建任务而不立即执行它
        task = ptt_crawler.s()
        print(task)
        # queue 參數，可以指定要發送到特定 queue 列隊中，依照不同的queue名字可以有效管理或是分配loading重得去哪個worker做
        task.apply_async(queue="pttCrawler")
    else:
        # 拿取每個爬蟲任務的參數列表，
        # 包含爬蟲資料的日期 date，例如 2021-04-10 的台股股價，
        # 資料來源 data_source，例如 twse 證交所、tpex 櫃買中心
        parameter_list = getattr(
            # 這裡意思是經由importlib.import_module去找到 financialdata/crawler/taiwan_stock_price.py 然後使用檔案裡面的gen_task_paramter_list func，並且給與func start/end date
            importlib.import_module(f"financialdata.crawler.{dataset}"),
            "gen_task_paramter_list",
        )(start_date=start_date, end_date=end_date)
        # 用 for loop 發送任務
        for parameter in parameter_list:
            logger.info(f"{dataset}, {parameter}")
            # 2024-02-27 07:50:41.612 | INFO     | __main__:Update:27 - taiwan_stock_price, {'date': '2021-04-01', 'data_source': 'tpex'}
            
            # print(parameter_list)
            # [{'date': '2021-04-01', 'data_source': 'twse'}, {'date': '2021-04-01', 'data_source': 'tpex'}]
            
            # 创建一个 Celery 任务。这里，crawler.s 是 Celery 的签名（signature）方法，用于创建任务而不立即执行它
            task = crawler.s(dataset, parameter)
            # queue 參數，可以指定要發送到特定 queue 列隊中
            task.apply_async(queue=parameter.get("data_source", ""))
        
        #  关闭数据库连接。这通常是在完成所有数据库操作后进行清理和释放资源的标准做法。
    db.router.close_connection()


if __name__ == "__main__":
    # dataset, start_date, end_date：這三個變量分別被賦值為 sys.argv[1:] 列表中的前三個元素
    dataset, start_date, end_date = sys.argv[1:]
    Update(dataset, start_date, end_date)
