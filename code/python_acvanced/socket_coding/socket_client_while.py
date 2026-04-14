# 客户端socket循环发送数据
import socket

# 创建socket对象
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# 连接服务器
client_socket.connect(('127.0.0.1', 8080))

while True:
    intput_data = input('请输入发送的数据,exit 退出:')
    if intput_data == 'exit':
        client_socket.send('客户端退出'.encode('utf-8'))
        break
    client_socket.send(intput_data.encode('utf-8'))

    # 接收数据
    data = client_socket.recv(1024)
    print('服务器返回的数据为:' , data.decode('utf-8'))

# 关闭socket
client_socket.close()