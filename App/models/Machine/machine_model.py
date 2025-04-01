from ...exts import db      #确保你使用的导入语句与文件结构相匹配。例如，如果 ext 在上s上级目录的 extensions 文件夹中，用三个.

class BaseMachine(db.Model):
    """机床基础信息表（主表）"""
    __tablename__ = 'base_machine'
    
    m_id = db.Column(db.Integer, primary_key=True, autoincrement=False, comment='机床ID')
    m_number = db.Column(db.String(20), nullable=False, unique=True, comment='机床编码')
    m_name = db.Column(db.String(20), nullable=False, comment='机床名称')
    m_state = db.Column(db.String(20), nullable=False, default='待机', comment='机床状态')
    m_time = db.Column(db.Float, default=0.0, comment='累计运行时间(小时)')
    m_workshop = db.Column(db.String(20), nullable=False, comment='所在车间')
    
    
    def __repr__(self):
        return f'<Machine {self.m_number}-{self.m_name}>'

