# import socket
# import threading
# import sys
# import pprint
# from App.models.Machine.machine_model import Mac1,Mac2,Mac3,db
# from sqlalchemy import text

# # 使用字典映射来简化机器模型的选择
# machine_models = {
#     1: Mac1,
#     2: Mac2,
#     3: Mac3
# }
# def connect_Server(host, port):
#     try:
#         client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)      #声明socket类型，同时生成链接对象
#         client.connect((host, port))
#         print("connect successful!")
#         return client
    
#     except socket.error as msg:
#         print("failed to connect!")
#         sys.exit(1)

# def client_send(client, msg):
#     client.send(msg.encode('utf-8'))

# def client_recv(client):
#     # 刚连接上清除 mac1- 3 的数据
#     for i in range(1, 4):
#         # 创建实例
#         machine_model = machine_models.get(i)
#         #  先把所有存在的都清除
#         db.session.query(machine_model).delete()
#         db.session.commit()
#         # 重置自增计数器
#         # text() 函数：使用 text() 将 SQL 语句包装起来，以使 SQLAlchemy 明白这是一个原始 SQL 语句。
#         db.session.execute(text('ALTER TABLE'+ ' mac' + str(i) + ' AUTO_INCREMENT = 1;'))
#         db.session.commit()
#     while True:
#         data = client.recv(1024)
#         data.decode('utf-8')
#         # 处理发送过来的数据
#         update_db(data)
#         # divide(data)

# def update_db(data):
#     # 直接使用split方法将字节数据拆分为数字列表
#     numbers = data.split(b'!')
#     numbers = [str(num.decode('utf-8')) for num in numbers]

#     # 将字符串列表中的元素转换为int类型
#     _time = (numbers[0])
#     for i in range(1, 4):
#         _mac = numbers[i]
#         _mac_info = _mac.split(',')

#         _name = (_mac_info[0])
#         _state = (_mac_info[1])
#         _material = (_mac_info[2])
#         print(_mac_info,_name,_state,_material)

#         # 创建实例
#         machine_model = machine_models.get(i)
#         machine = machine_model(time= _time, name=_name, state= _state, material=_material)
#         # 添加到会话
#         try:
#             db.session.add(machine)
#             db.session.commit()
#         except Exception as e:
#             db.session.rollback()  # 发生错误时回滚
#             print(f"Error occurred: {e}")

# def divide(data):
#     # 直接使用split方法将字节数据拆分为数字列表
#     numbers = data.split(b',')

#     # 将字符串列表中的元素转换为int类型
#     number1 = int(numbers[0])
#     number2 = int(numbers[1])
#     number3 = int(numbers[2])

#     print("红色色块加工总数: ", number1)
#     print("蓝色色块加工总数: ", number2)
#     print("黑色色块加工总数: ", number3)
#     # 打开文件，准备写入
#     with open('data.txt', 'w') as file:
#         # 写入数据
#         file.write(f'红色色块加工总数: {number1}\n')
#         file.write(f'蓝色色块加工总数: {number2}\n')
#         file.write(f'黑色色块加工总数: {number3}\n')

#     print("数据已保存到文件中。")

# if __name__ == "__main__":
#     ip = "127.0.0.1"
#     port = 3000
#     client = connect_Server(ip, port)
#     try:
#         t1 = threading.Thread(target= client_send)
#         t2 = threading.Thread(target= client_recv)
#         t1.start()
#         t2.start()
#         pprint.pprint(threading.enumerate())

#     except Exception as e:
#         print("Error: unable to start thread.", e)
