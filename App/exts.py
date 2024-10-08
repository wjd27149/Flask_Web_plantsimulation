from flask_sqlalchemy import SQLAlchemy # ORM（对象关系映射）
from flask_migrate import Migrate   # 数据迁移

db = SQLAlchemy()
migrate = Migrate()

def init_exts(app):
    db.init_app(app=app)
    migrate.init_app(app=app,db=db)
