from App.exts import db

from datetime import datetime

class Workpiece(db.Model):
    __tablename__ = 'workpiece'
    j_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    j_quantity = db.Column(db.Integer, nullable=False)
    p_number = db.Column(db.String(20))
    c_name = db.Column(db.String(20))
    j_number = db.Column(db.String(20), nullable=False)
    j_state = db.Column(db.String(20), default='待加工')
    j_create_date = db.Column(db.DateTime, default=datetime.now)
    j_due_date = db.Column(db.DateTime)
    j_remark = db.Column(db.String(32))
    
    # 关联工序
    operations = db.relationship('Operation', backref='workpiece', lazy=True)


import json
from sqlalchemy import TypeDecorator, VARCHAR
class JSONEncodedDict(TypeDecorator):
    """SQLAlchemy自定义类型，实现JSON序列化"""
    impl = VARCHAR(255)  # 指定VARCHAR长度，MySQL要求必须指定
    
    def process_bind_param(self, value, dialect):
        if value is not None:
            value = json.dumps(value, ensure_ascii=False)
        return value

    def process_result_value(self, value, dialect):
        if value is not None:
            value = json.loads(value)
        return value
class Operation(db.Model):
    __tablename__ = 'operation'
    o_id = db.Column(db.Integer, primary_key=True)
    o_name = db.Column(db.String(20))
    o_number = db.Column(db.Integer)
    o_job_id = db.Column(db.Integer, db.ForeignKey('workpiece.j_id'))
    
    # 使用自定义类型存储列表
    o_time = db.Column(JSONEncodedDict)          # 存储如 [5,5]
    o_machine_name = db.Column(JSONEncodedDict)  # 存储如 ["machine1", "machine2"]
    o_index =  db.Column(JSONEncodedDict) # 加工系数
