from App.exts import db
class Material(db.Model):
    __tablename__ = 'material' 
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    time = db.Column(db.Float, unique = True)
    name = db.Column(db.String(30))
    type = db.Column(db.String(30))
    state = db.Column(db.Integer, default=0)
    machine = db.Column(db.String(30))