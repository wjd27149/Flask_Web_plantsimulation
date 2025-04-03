import socket
import threading
import sys
import pprint
from sqlalchemy import text


def connect_Server(host, port):
    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)      #声明socket类型，同时生成链接对象
        client.connect((host, port))
        print("connect successful!")
        return client
    
    except socket.error as msg:
        print("failed to connect!")
        sys.exit(1)

def client_send(client, msg):
    client.send(msg.encode('utf-8'))

def client_recv(client):
    while True:
        data = client.recv(1024)
        data.decode('utf-8')
        print(data)
        # 处理发送过来的数据
        # divide(data)

def divide(data):
    # 直接使用split方法将字节数据拆分为数字列表
    numbers = data.split(b',')

    # 将字符串列表中的元素转换为int类型
    number1 = int(numbers[0])
    number2 = int(numbers[1])
    number3 = int(numbers[2])

    print("红色色块加工总数: ", number1)
    print("蓝色色块加工总数: ", number2)
    print("黑色色块加工总数: ", number3)
    # 打开文件，准备写入
    with open('data.txt', 'w') as file:
        # 写入数据
        file.write(f'红色色块加工总数: {number1}\n')
        file.write(f'蓝色色块加工总数: {number2}\n')
        file.write(f'黑色色块加工总数: {number3}\n')

    print("数据已保存到文件中。")

if __name__ == "__main__":
    ip = "127.0.0.1"
    port = 3000
    client = connect_Server(ip, port)
    try:
        t1 = threading.Thread(target= client_send)
        t2 = threading.Thread(target= client_recv)
        t1.start()
        t2.start()
        pprint.pprint(threading.enumerate())

    except Exception as e:
        print("Error: unable to start thread.", e)
