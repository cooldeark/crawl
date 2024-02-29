import time
import typing

from loguru import logger
from sqlalchemy import engine
from financialdata.backend.db import clients


def check_alive(connect: engine.base.Connection):
    connect.execute("SELECT 1 + 1")


def check_connect_alive(
    connect: engine.base.Connection,
    connect_func: typing.Callable,
):
    if connect:
        try:
            check_alive(connect)
            return connect
        except Exception as e:
            logger.info(
                f"""
                {connect_func.__name__} reconnect, error: {e}
                """
            )
            time.sleep(1)
            try:
                connect = connect_func()
            except Exception as e:
                logger.info(
                    f"""
                    {connect_func.__name__} connect error, error: {e}
                    """
                )
            return check_connect_alive(connect, connect_func)


class Router:
    def __init__(self):
        self._mysql_financialdata_conn = clients.get_mysql_financialdata_conn()
        self._mysql_ptt_conn = clients.get_mysql_ptt_conn()

    def check_mysql_financialdata_conn_alive(self):
        self._mysql_financialdata_conn = check_connect_alive(
            self._mysql_financialdata_conn,
            clients.get_mysql_financialdata_conn,
        )
        return self._mysql_financialdata_conn
    
    def check_mysql_ptt_conn_alive(self):
        self._mysql_ptt_conn = check_connect_alive(
            self._mysql_ptt_conn,
            clients.get_mysql_ptt_conn,
        )
        return self._mysql_ptt_conn

    @property
    def mysql_financialdata_conn(self):
        return self.check_mysql_financialdata_conn_alive()
    
    @property
    # 這裡 mysql_ptt_conn 被 @property 裝飾，這意味着你可以像訪問屬性一樣來訪問 mysql_ptt_conn，而不需要在其後加上括號來調用它。當你訪問這個屬性時，實際上會執行 check_mysql_ptt_conn_alive() 方法，並返回該方法的結果。
    def mysql_ptt_conn(self):
        return self.check_mysql_ptt_conn_alive()

    def close_connection(self):
        self._mysql_financialdata_conn.close()
