import pandas as pd
from fastapi import FastAPI
from sqlalchemy import create_engine, engine
from api import config


def get_mysql_conn() -> engine.base.Connection:
    address = (
        f"mysql+pymysql://{config.MYSQL_DATA_USER}:{config.MYSQL_DATA_PASSWORD}"
        f"@{config.MYSQL_DATA_HOST}:{config.MYSQL_DATA_PORT}/{config.MYSQL_DATA_DATABASE}"
    )
    engine = create_engine(address)
    connect = engine.connect()
    return connect


app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/ptt-line-message")
def get_user_message():
    # sql = f"""
    # select * from TaiwanStockPrice
    # where StockID = '{stock_id}'
    # and Date>= '{start_date}'
    # and Date<= '{end_date}'
    # """
    # 构建插入数据的 SQL 语句
    sql = """
    INSERT INTO ptt_database.lineUser (userID, crawlURL) VALUES ('test', 'test')
    """
    mysql_conn = get_mysql_conn()
    # 执行 SQL 语句
    with mysql_conn.cursor() as cursor:
        cursor.execute(sql)
        mysql_conn.commit()
    # data_df = pd.read_sql(sql, con=mysql_conn)
    return {"Hello": "World"}


@app.get("/taiwan_stock_price")
def taiwan_stock_price(
    stock_id: str = "",
    start_date: str = "",
    end_date: str = "",
):
    sql = f"""
    select * from TaiwanStockPrice
    where StockID = '{stock_id}'
    and Date>= '{start_date}'
    and Date<= '{end_date}'
    """
    mysql_conn = get_mysql_conn()
    data_df = pd.read_sql(sql, con=mysql_conn)
    data_dict = data_df.to_dict("records")
    return {"data": data_dict}
