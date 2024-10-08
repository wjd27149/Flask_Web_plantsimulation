# __init__.py : 初始化文件，创建Flask应用
from flask import Flask
from .views import blue
from .exts import init_exts
import os
import sys
import io

def creat_app():
    app = Flask(__name__)

    # 注册蓝图
    app.register_blueprint(blueprint=blue)

    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, write_through=True)
    # 配置数据库
    # db_uri = 'sqlite:///sqlite3.db'
    db_uri = 'mysql+pymysql://root: @localhost:3306/bookdb' # mysql的配置
    app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # 禁止对象追踪修改
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'optional-default-value')

    # 初始化插件
    init_exts(app=app)

    return app

