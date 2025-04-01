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

class Operation(db.Model):
    __tablename__ = 'operation'
    o_id = db.Column(db.Integer, primary_key=True)
    o_name = db.Column(db.String(20))
    o_number = db.Column(db.Integer)
    o_job_id = db.Column(db.Integer, db.ForeignKey('workpiece.j_id'))
    o_time = db.Column(db.Integer)
    o_machine_name = db.Column(db.String(20))
