# 服务器端,socket_server
import socket

# 创建socket对象
sock_server = socket.socket()

# 绑定ip和端口
sock_server.bind(('127.0.0.1', 8080))

# 监听连接  backlog参数指定最大连接数
sock_server.listen(1)

# 等待连接,返回二元组
# accept 方法会阻塞,直到有客户端连接
result = sock_server.accept()

conn = result[0]    # 连接对象
addr = result[1]    # 客户端地址

# print(conn)
# print(addr)

# 接收客户端发送的数据,缓冲区大小为1024字节
# recv 方法会阻塞,直到有客户端发送数据
# recv 方法返回的是字节类型的数据,通过 decode 方法解码为字符串类型
data : str = conn.recv(1024)
# 接收数据后,需要解码
print('客户端发送的数据为' , data.decode('utf-8'))

# 发送数据给客户端
conn.send('hello client'.encode('utf-8'))

# 关闭连接
conn.close()
sock_server.close()
