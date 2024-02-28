import sqlite3

# 连接到SQLite数据库
# 如果文件mydatabase.db不存在，会自动在当前目录创建这个文件
conn = sqlite3.connect('ptt_crawler.db')

# 创建一个Cursor对象，用于执行SQL语句
cursor = conn.cursor()

# 执行一条SQL语句，创建一个名为user的表
cursor.execute('CREATE TABLE IF NOT EXISTS user (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, age INTEGER)')

# 插入一条记录
cursor.execute('INSERT INTO user (name, age) VALUES (?, ?)', ('Alice', 21))

# 通过rowid来查询刚插入的记录
cursor.execute('SELECT * FROM user WHERE rowid = ?', (cursor.lastrowid,))
print(cursor.fetchone())  # 输出插入的数据

# 查询并打印所有记录
cursor.execute('SELECT * FROM user')
print(cursor.fetchall())  # 输出所有数据

# 提交事务
conn.commit()

# 关闭Cursor
cursor.close()

# 关闭Connection
conn.close()
