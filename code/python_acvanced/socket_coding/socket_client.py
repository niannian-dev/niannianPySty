# 客户端
import socket

# 创建socket对象
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# 连接服务器
client_socket.connect(('127.0.0.1', 8080))

# 发送数据
client_socket.send('hello server'.encode('utf-8'))

# 接收数据
data = client_socket.recv(1024)
print('服务器返回的数据为' , data.decode('utf-8'))

# 关闭socket
client_socket.close()