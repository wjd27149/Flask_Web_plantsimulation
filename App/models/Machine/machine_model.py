from ...exts import db      #确保你使用的导入语句与文件结构相匹配。例如，如果 ext 在上s上级目录的 extensions 文件夹中，用三个.

# 定义机器总表 BaseMachine
class BaseMachine(db.Model):
    __tablename__ = 'basemachine'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(30), nullable=False)
    type = db.Column(db.String(30))

    # # Relationship to each machine type       不能 一对一 因为 mac1 是和事件有关的表 应该表对表
    # mac1 = db.relationship('Mac1', backref='base_machine', uselist=False)
    # mac2 = db.relationship('Mac2', backref='base_machine', uselist=False)
    # mac3 = db.relationship('Mac3', backref='base_machine', uselist=False)

# 定义一个基础类
class BaseMac(db.Model):
    __abstract__  = True
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    time = db.Column(db.String(30), unique=True)
    name = db.Column(db.String(30))    # 代表plant simulation 里面flow的名字
    type = db.Column(db.String(30))   # 假设 'True' 表示男
    state = db.Column(db.String(30))
    material = db.Column(db.String(30))

class Mac1(BaseMac):
    __tablename__ = "mac1"
    type = db.Column(db.String(30), default="A")

class Mac2(BaseMac):
    __tablename__ = "mac2"
    type = db.Column(db.String(30), default="B")

class Mac3(BaseMac):
    __tablename__ = "mac3"
    type = db.Column(db.String(30), default="C")



# # 动态创建模型和表
# def create_machine_tables(prefix='machine', count=10):
#     for i in range(1, count + 1):
#         class_name = f"{prefix}{i}"
#         globals()[class_name] = type(class_name, (BaseMachine,), {
#             "__tablename__": f"{prefix}_{i}"
#         })
#         db.Model.query_class = db.Query  # 确保所有新模型都能使用查询

# # 创建10个表
# create_machine_tables('machine', 10)