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
    sql = text("""
    INSERT INTO ptt_database.lineUser (userID, crawlURL) VALUES ('test', 'test')
    """)
    mysql_conn = get_mysql_conn()
    with mysql_conn.begin() as transaction:  # 在連接上開始一個事務
        mysql_conn.execute(sql)  # 執行 SQL 語句
        transaction.commit()  # 提交事務
    mysql_conn.close()  # 關閉連接
    return '', 200


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
