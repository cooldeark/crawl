import mysql.connector

from financialdata.config import (
    MYSQL_DATA_HOST,
    MYSQL_DATA_USER,
    MYSQL_DATA_PASSWORD
)

# 连接到MySQL服务器
conn = mysql.connector.connect(
    host = MYSQL_DATA_HOST,
    user = MYSQL_DATA_USER,
    password = MYSQL_DATA_PASSWORD
)

# 创建一个Cursor对象用于执行SQL语句
cursor = conn.cursor()

# 打开并读取SQL文件
with open('/opt/crawl/financialdata/backend/db/create_ptt_table.sql', 'r') as file:
    sql_script = file.read()

# 由于SQL脚本可能包含多个SQL命令，需要分割它们
sql_commands = sql_script.split(';')

# 执行每个SQL命令
for command in sql_commands:
    # 您可能需要检查命令是否为空字符串
    if command.strip() != '':
        cursor.execute(command)

# 打开并读取SQL文件
with open('/opt/crawl/financialdata/backend/db/create_partition_table.sql', 'r') as file:
    sql_script = file.read()

# 由于SQL脚本可能包含多个SQL命令，需要分割它们
sql_commands = sql_script.split(';')

# 执行每个SQL命令
for command in sql_commands:
    # 您可能需要检查命令是否为空字符串
    if command.strip() != '':
        cursor.execute(command)



# 提交事务
conn.commit()

# 关闭Cursor和Connection
cursor.close()
conn.close()
