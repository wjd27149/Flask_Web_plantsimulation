# 将App目录添加到项目路径，解决views里的文件导入models里的模型类时找不到models模块路径的问题
from collections import deque
import sys,os
sys.path.append(os.getcwd() + "/APP/models")
# sys.path.append(r'C:\Users\18525\Desktop\论文\flask_demo\APP\models')
# print(sys.path)

from App import creat_app
from Clients.client import *
import threading
from flask import request, jsonify, render_template

# 声明一个全局变量 client
client = None
received_data = deque(maxlen=10)  # 保存最近10条数据
app = creat_app()

def run_flask_app():
    app.run(host='127.0.0.1', port=5000, threaded=True)  # 使用多线程和调试模式 调试模式会发现有更改并且同步 
    #当 debug=True 时，Flask 开启调试模式，并且默认会启动一个重载器（reloader），这个重载器允许 Flask 在检测到代码变化时自动重新加载应用。
    # 然而，重载器依赖信号机制来检测文件的更改，并触发重新加载。这种信号处理只能在主线程中工作。

def run_flask_app_with_debug():
    app.run(host='127.0.0.1', port=5000, threaded=True, debug= True)

import threading

lock = threading.Lock()  # 创建全局锁

def receive_messages():
    """持续接收消息的线程"""
    while True:
        try:
            data = client.recv(1024)
            if not data:
                break
            decoded = data.decode().strip()
            parts = decoded.split(',')

            if len(parts) == 12:  
                with lock:  # 加锁
                    received_data.append({
                        'time': parts[0],
                        'completed_jobs': parts[1],
                        'completed_operation': parts[2],
                        'machine_1': f"{(float(parts[3]) * 100):.2f}%",
                        'machine_2': f"{(float(parts[4]) * 100):.2f}%",
                        'machine_3': f"{(float(parts[5]) * 100):.2f}%",
                        'machine_4': f"{(float(parts[6]) * 100):.2f}%",
                        'machine_5': f"{(float(parts[7]) * 100):.2f}%",
                        'machine_6': f"{(float(parts[8]) * 100):.2f}%",
                        'machine_7': f"{(float(parts[9]) * 100):.2f}%",
                        'total_jobs': parts[10],
                        'total_operations':parts[11]
                    })
                # print(f"Updated received_data: {received_data}")  # 确保数据存储成功
        except Exception as e:
            print(f"接收错误: {str(e)}")
            break

@app.route('/get_latest_data')
def get_latest_data():
    """前端请求最新的仿真数据"""
    with lock:  # 加锁
        if received_data:
            return jsonify(received_data[-1])  
        else:
            return jsonify({
                'time': "0.00",
                'completed_jobs': "0",
                'completed_operation': "0",
                'machine_1': "0.00%",
                'machine_2': "0.00%",
                'machine_3': "0.00%",
                'machine_4': "0.00%",
                'machine_5': "0.00%",
                'machine_6': "0.00%",
                'machine_7': "0.00%",
                'total_jobs': "0",
                'total_operations':"0"
            })
if __name__ == '__main__':

    # # '''调用debug 模式'''
    run_flask_app_with_debug()

    # ip = "127.0.0.1"
    # port = 3000
    # client = connect_Server(ip, port)
    # # 存储 client 在 current_app.config 中
    # app.config['client'] = client
    # try:
    #     # 启动一个接受线程
    #     recv_thread = threading.Thread(target=receive_messages, daemon=True)
        
    #     recv_thread.start()

    #     # 在主线程运行 Flask（可以带调试模式）
    #     app.run(host='127.0.0.1', port=5000, debug=False, threaded=True)
    # except Exception as e:
    #     print(f"An error occurred: {e}")
