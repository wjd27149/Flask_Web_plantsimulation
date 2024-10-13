from App.exts import db

class BaseMaterial(db.Model):
    __tablename__ = 'basematerial'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(30), nullable=False) # nullable 不可以为空的
    type = db.Column(db.String(30))
    sum = db.Column(db.Integer)
class BaseMat(db.Model):
    __abstract__ = True
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    time = db.Column(db.String(30), unique=True)
    name = db.Column(db.String(30))
    type = db.Column(db.String(30))
    number = db.Column(db.Integer)
    state = db.Column(db.Integer, default=0)
    machine = db.Column(db.String(30))