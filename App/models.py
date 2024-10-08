# models.py : 模型，数据库

'''
    模型      ===      数据库
    类        ——>     表结构
    类属性     ——>    表字段
    一个对象   ——>    表的一行数据
'''


from .exts import db
from werkzeug.security import generate_password_hash, check_password_hash

# 模型Model：类
# 必须继承 db.Model User才能从普通的类变成模型

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


# 机器
class BaseMachine(db.Model):
    __tablename__ = 'base_machine'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    time = db.Column(db.Float)#, unique=True
    name = db.Column(db.String(30))
    type = db.Column(db.String(30))   # 假设 'True' 表示男
    state = db.Column(db.Integer, default=0)
    material = db.Column(db.String(30))

class Material(db.Model):
    __tablename__ = 'material' 
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    time = db.Column(db.Float, unique = True)
    name = db.Column(db.String(30))
    type = db.Column(db.String(30))
    state = db.Column(db.Integer, default=0)
    machine = db.Column(db.String(30))

# 作者
class Author(db.Model):
    __tablename__ = 'author'  # 表名,如果不写表名，也会自动生成（类名小写），表名一定要小写！
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(30))
    age = db.Column(db.Integer, default=1)
    sex = db.Column(db.Boolean, default=True)   # True表示男
    email = db.Column(db.String(200))
    # 关系：Author可以调用books，Book可以反向调用my_auther
    books = db.relationship('Book', backref='my_author', lazy='dynamic')

# 中间表（书籍-出版社）
book_publish = db.Table(
    'book_publisher',
    db.Column('book_id', db.Integer, db.ForeignKey('book.id'), primary_key=True),
    db.Column('publisher_id', db.Integer, db.ForeignKey('publisher.id'), primary_key=True)
)
# 书籍
class Book(db.Model):
    __tablename__ = 'book'  # 表名
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), unique=True)
    date = db.Column(db.DateTime)   # 书籍日期
    # 1对多：外键
    author_id = db.Column(db.Integer, db.ForeignKey(Author.id))
# 出版社
class Publisher(db.Model):
    __tablename__ = 'publisher'  # 表名
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(30), unique=True)
    address = db.Column(db.String(200))
    city = db.Column(db.String(100))
    province = db.Column(db.String(100))
    country = db.Column(db.String(100))
    website = db.Column(db.String(100))
    # 多对多，关联book表，secondary是设置中间表
    books = db.relationship('Book', backref='publishers', secondary=book_publish, lazy='dynamic')

