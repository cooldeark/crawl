import typing
import json
import pandas as pd
import pymysql
from loguru import logger
from sqlalchemy import engine


def update2mysql_by_pandas(
    df: pd.DataFrame,
    table: str,
    mysql_conn: engine.base.Connection,
):
    if len(df) > 0:
        try:
            df.to_sql(
                name=table,
                con=mysql_conn,
                if_exists="append",
                index=False,
                chunksize=1000,
            )
        except Exception as e:
            logger.info(e)
            return False
    return True


def build_update_sql(
    colname: typing.List[str],
    value: typing.List[str],
):
    update_sql = ",".join(
        [
            ' `{}` = "{}" '.format(
                colname[i],
                str(value[i]),
            )
            for i in range(len(colname))
            if str(value[i])
        ]
    )
    return update_sql


def build_df_update_sql(
    table: str, df: pd.DataFrame
) -> typing.List[str]:
    logger.info("build_df_update_sql")
    df_columns = list(df.columns)
    sql_list = []
    for i in range(len(df)):
        temp = list(df.iloc[i])
        value = [
            pymysql.converters.escape_string(
                str(v)
            )
            for v in temp
        ]
        sub_df_columns = [
            df_columns[j]
            for j in range(len(temp))
        ]
        update_sql = build_update_sql(
            sub_df_columns, value
        )
        # SQL 上傳資料方式
        # DUPLICATE KEY UPDATE 意思是
        # 如果有重複，就改用 update 的方式
        # 避免重複上傳
        sql = """INSERT INTO `{}`({})VALUES ({}) ON DUPLICATE KEY UPDATE {}
            """.format(
            table,
            "`{}`".format(
                "`,`".join(
                    sub_df_columns
                )
            ),
            '"{}"'.format(
                '","'.join(value)
            ),
            update_sql,
        )
        sql_list.append(sql)
    return sql_list


def update2mysql_by_sql(
    df: pd.DataFrame,
    table: str,
    mysql_conn: engine.base.Connection,
):
    sql = build_df_update_sql(table, df)
    commit(
        sql=sql, mysql_conn=mysql_conn
    )


def commit(
    sql: typing.Union[
        str, typing.List[str]
    ],
    mysql_conn: engine.base.Connection = None,
):
    logger.info("commit")
    try:
        trans = mysql_conn.begin()
        if isinstance(sql, list):
            for s in sql:
                try:
                    mysql_conn.execution_options(
                        autocommit=False
                    ).execute(
                        s
                    )
                except Exception as e:
                    logger.info(e)
                    logger.info(s)
                    break

        elif isinstance(sql, str):
            mysql_conn.execution_options(
                autocommit=False
            ).execute(
                sql
            )
        trans.commit()
    except Exception as e:
        trans.rollback()
        logger.info(e)


def upload_data(
    df: pd.DataFrame,
    table: str,
    mysql_conn: engine.base.Connection,
):
    if len(df) > 0:
        # 直接上傳
        if update2mysql_by_pandas(
            df=df,
            table=table,
            mysql_conn=mysql_conn,
        ):
            pass
        else:
            # 如果有重複的資料
            # 使用 SQL 語法上傳資料
            update2mysql_by_sql(
                df=df,
                table=table,
                mysql_conn=mysql_conn,
            )


def search_ptt(title_keyword: str, mysql_conn: engine.base.Connection):

    get_title_keyword = json.loads(title_keyword)
    needSendToUser = []

    try:
        for eachTitle in get_title_keyword:
            query = f"select * from (SELECT * FROM mobiles order by id DESC limit 25) as latestRecords  WHERE title LIKE '%{eachTitle}%';"
            result_df = pd.read_sql(query, con=mysql_conn)
            # 如果没有找到匹配的结果，添加一条新记录
            if result_df.empty:
                # 如果找不到，代表是新的人po上來，要跟我們說
                needSendToUser.append(eachTitle)

                # 创建一个包含新记录数据的 DataFrame
                # id & createTime系統會自動幫忙建
                new_record = pd.DataFrame({
                    'title': [f'{eachTitle}'],
                })
            # 将新记录插入数据库
            new_record.to_sql('mobiles', con=mysql_conn, if_exists='append', index=False)
        return json.dumps(needSendToUser)

        # 下面是讓你知道，如果失敗也要回傳pd.DataFrame()，因為這樣也能追蹤為啥失敗
        # if len(result_df) > 0:
        #     logger.info(f"Found results for keyword '{title_keyword}':\n{result_df}")
        #     return result_df
        # else:
        #     logger.info(f"No results found for keyword '{title_keyword}'.")
        #     return pd.DataFrame()

    except Exception as e:
        logger.error(f"Error searching for keyword '{title_keyword}': {e}")
        return pd.DataFrame()

