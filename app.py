from App import creat_app
from Clients.client import *
import threading

app = creat_app()

def run_flask_app():
    app.run(host='127.0.0.1', port=5000, threaded=True)  # 使用多线程和调试模式 调试模式会发现有更改并且同步 
    #当 debug=True 时，Flask 开启调试模式，并且默认会启动一个重载器（reloader），这个重载器允许 Flask 在检测到代码变化时自动重新加载应用。
    # 然而，重载器依赖信号机制来检测文件的更改，并触发重新加载。这种信号处理只能在主线程中工作。

def run_flask_app_with_debug():
    app.run(host='127.0.0.1', port=5000, threaded=True, debug= True)

def client_recv_with_context(client):
    # 手动推送 Flask 应用的上下文
    with app.app_context():
        client_recv(client)

if __name__ == '__main__':

    ip = "127.0.0.1"
    port = 3000
    client = connect_Server(ip, port)
    
    '''调用debug 模式'''
    run_flask_app_with_debug()
    '''
    try:
        # 创建两个线程
        flask_thread = threading.Thread(target=run_flask_app)
        communication_thread = threading.Thread(target=client_recv_with_context, args=(client,))
        send_thread = threading.Thread(target= client_send)



        # 启动通信线程
        communication_thread.start()
        print("Communication thread started")
        send_thread.start()
        print("Send thread started")

        # 启动 Flask 应用的线程
        flask_thread.start()
        print("Flask thread started")        

        # 等待线程执行完毕
        flask_thread.join()
        communication_thread.join()
        send_thread.join()

    except Exception as e:
        print(f"An error occurred: {e}")'''
