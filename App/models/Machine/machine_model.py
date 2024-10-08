from ...exts import db      #确保你使用的导入语句与文件结构相匹配。例如，如果 ext 在上s上级目录的 extensions 文件夹中，用三个.

# 定义一个基础类
class BaseMachine(db.Model):
    __tablename__ = 'base_machine'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    time = db.Column(db.Float, unique=True)
    name = db.Column(db.Integer, default=1)
    type = db.Column(db.String(30))   # 假设 'True' 表示男
    state = db.Column(db.Integer, default=0)
    material = db.Column(db.String(30))

# 动态创建模型和表
def create_machine_tables(prefix='machine', count=10):
    for i in range(1, count + 1):
        class_name = f"{prefix}{i}"
        globals()[class_name] = type(class_name, (BaseMachine,), {
            "__tablename__": f"{prefix}_{i}"
        })
        db.Model.query_class = db.Query  # 确保所有新模型都能使用查询

# # 创建10个表
# create_machine_tables('machine', 10)