import pandas as pd
from fastapi import FastAPI, Request
from sqlalchemy import create_engine, engine, text
from api import config


def get_mysql_conn() -> engine.base.Connection:
    address = (
        f"mysql+pymysql://{config.MYSQL_DATA_USER}:{config.MYSQL_DATA_PASSWORD}"
        f"@{config.MYSQL_DATA_HOST}:{config.MYSQL_DATA_PORT}/{config.MYSQL_DATA_DATABASE}"
    )
    engine = create_engine(address)
    connect = engine.connect()
    return connect

# def check_user(userID):

#     if 條件1:
#     # 如果條件1為真，執行這裡的代碼
#     elif 條件2:
#         # 如果條件1為假但條件2為真，執行這裡的代碼
#     else:
#         # 如果條件1和條件2都為假，執行這裡的代碼


# 切記改過flaskAPI的route必須重啟server
app = FastAPI()


@app.get("/")
def read_root():
    userID = 'Ua2cde922e74b8c37942f45b54bf5388c'
    # 使用参数化查询
    sql = text("SELECT * FROM lineUser WHERE userID = :userID")
    mysql_conn = get_mysql_conn()
    result = mysql_conn.execute(sql, {'userID': userID})  # 将 userID 作为参数传递
    # 获取查询结果并转换为列表，每个元素是一个字典
    result_list = [dict(row) for row in result]
    mysql_conn.close()  # 关闭连接
    print(result_list)


@app.post("/ptt-line-message")
async def get_user_message(request: Request):
    # 異步讀取請求體中的 JSON 數據
    data = await request.json()
    getData = data['events'][0]
    user_id = getData['source']['userId']
    text = getData['message']['text']

    sql = text("""
    INSERT INTO ptt_data.lineUser (userID, crawlURL) VALUES (123, 123)
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
