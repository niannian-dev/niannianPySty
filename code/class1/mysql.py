# import pymysql

# db_confing = {
#     'host': 'localhost',   # 服务器地址
#     'port': 3306,          # MySQL 端口
#     'user': 'root',        # 用户名
#     'password': '123456'    # 密码
# }

# conn = pymysql.Connect(**db_confing)

# print(conn.get_server_info)

# conn.close()


from pymysql import Connection

#构建到mysql数据库链接

conn = Connection(
    host="localhost",
    port=3306,
    user="root",
    password="123456",
    # autocommit=True # 自动提交事务
)

print(conn.get_server_info())


cursor = conn.cursor()
conn.select_db("jdbc")    # 选择数据库jdbc

count = cursor.execute("select * from t_user")
print(count)

users = cursor.fetchall()   # 获取所有结果集
print(users)

for user in users:
    print(user)

print('-'*30)

# cursor.execute("Create Table if not exists py_mysql(id INT, info VARCHAR(255))")‘


cursor.execute("insert into py_mysql(id, info) values(1, 'hello')")

# 提交事务
conn.commit()

cursor.execute("select * from py_mysql")
result = cursor.fetchall()
print(result)


conn.close()
