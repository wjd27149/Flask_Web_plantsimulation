# 将App目录添加到项目路径，解决views里的文件导入models里的模型类时找不到models模块路径的问题
import sys,os
sys.path.append(os.getcwd() + "/APP/models")
# sys.path.append(r'C:\Users\18525\Desktop\论文\flask_demo\APP\models')
# print(sys.path)

from App import creat_app
from Clients.client import *
import threading

# 声明一个全局变量 client
client = None

app = creat_app()

def run_flask_app():
    app.run(host='127.0.0.1', port=5000, threaded=True)  # 使用多线程和调试模式 调试模式会发现有更改并且同步 
    #当 debug=True 时，Flask 开启调试模式，并且默认会启动一个重载器（reloader），这个重载器允许 Flask 在检测到代码变化时自动重新加载应用。
    # 然而，重载器依赖信号机制来检测文件的更改，并触发重新加载。这种信号处理只能在主线程中工作。

def run_flask_app_with_debug():
    app.run(host='127.0.0.1', port=5000, threaded=True, debug= True)

# def client_recv_with_context(client):
#     # 手动推送 Flask 应用的上下文
#     with app.app_context():
#         client_recv(client)

if __name__ == '__main__':

    # '''调用debug 模式'''
    run_flask_app_with_debug()

    # ip = "127.0.0.1"
    # port = 3000
    # client = connect_Server(ip, port)
    # # 存储 client 在 current_app.config 中
    # app.config['client'] = client
    # try:
    #     # 创建两个线程
    #     flask_thread = threading.Thread(target=run_flask_app)
    #     communication_thread = threading.Thread(target=client_recv_with_context, args=(client,))

    #     # 启动通信线程
    #     communication_thread.start()
    #     print("Communication thread started")


    #     # 启动 Flask 应用的线程
    #     flask_thread.start()
    #     print("Flask thread started")        

    #     # 等待线程执行完毕
    #     flask_thread.join()
    #     communication_thread.join()

    # except Exception as e:
    #     print(f"An error occurred: {e}")
