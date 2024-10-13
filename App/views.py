# 在views.py中放路由和视图函数

from flask import Blueprint, request, render_template, url_for, redirect, flash, current_app, g
from App.models.User.books import * #后面是用views来控制数据库的，所以要在views中导入models文件                 flask db migrate 代码在这里实现
from App.models.User.user_model import *
from App.models.Machine.machine_model import *
from App.models.Material.material_model import *
from sqlalchemy import text

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, EmailField
from wtforms.validators import InputRequired, Email, Length

from Clients.client import client_send

# 蓝图
blue = Blueprint('book', __name__)

# 用字典模拟一个简单的用户数据库（仅用于演示）
users = {
    "admin": "1",
    "user": " "
}

machine_models = {
    1: Mac1,
    2: Mac2,
    3: Mac3
}
machine_names = ["压接1","压接2","压接3"]
machine_types = ["A","B","C"]
class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), Length(min=4, max=25)])
    email = StringField('Email', validators=[InputRequired(), Email()])
    password = PasswordField('Password', validators=[InputRequired()])
    submit = SubmitField('Register')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])
    submit = SubmitField('Login')

class SumForm(FlaskForm):
    num1 = StringField("Num1")
    num2 = StringField("Num2")
    submit = SubmitField('Sum')

@blue.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        form = LoginForm()
        user = User.query.filter_by(username=form.username.data).first()
        current_app.logger.info('f{} This is a log message'.format(form.username.data))
        if user and user.check_password(form.password.data):
            return redirect(url_for('book.home',bid = user.id))
        else:
            flash("请重新登录",'error')
    return render_template('login.html')

@blue.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        form = RegistrationForm()
        # if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            flash('Username already exists.')
            return redirect(url_for('book.register'))
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('User created successfully. You can now login.',category='success')
        return redirect(url_for('book.login'))
    
    return render_template('register.html')

@blue.route('/home/<int:bid>')
def home(bid):
    current_user = User.query.get(bid)
    return render_template('stat/home.html',current_user = current_user)

@blue.route('/user/<int:bid>')
def user_list(bid):
    users = User.query.all()
    current_user = User.query.get(bid)
    return render_template('stat/user.html',users = users,current_user = current_user)

@blue.route('/machine/<int:bid>')
def machine_list(bid):
    machines = BaseMachine.query.all()
    current_user = User.query.get(bid)
    return render_template('stat/machine.html',machines = machines,current_user = current_user)

@blue.route('/delete_basemachine/<int:bid>', methods=['POST'])
def delete_basemachine(bid):
    try:
        # 删除 BaseMachine 表对应机器的所有记录
        # machine_models 字典的键应该是从 1 开始而不是 0 开始。
        # 根据你的代码，i 从 0 到 2 进行循环，而如果字典中没有以 0 开头的条目，get(i) 将返回 None。
        for i in range(1,4):
            machine_model = machine_models.get(i)
            db.session.query(machine_model).delete()
            db.session.commit()
        flash("All records deleted successfully", category='success')

    except Exception as e:
        db.session.rollback()
        current_app.logger.info(f"Error: {str(e)}")
        flash(f"Error: {str(e)}", category='error')

    # 重定向到machine 页面
    machines = BaseMachine.query.all()
    current_user = User.query.get(bid)
    return render_template('stat/machine.html',machines = machines,current_user = current_user)

@blue.route('/add_basemachine/<int:bid>', methods=['POST'])
def add_basemachine(bid):
    try:
        #  先把所有存在的都清除
        db.session.query(BaseMachine).delete()
        db.session.commit()
        # 重置自增计数器
        # text() 函数：使用 text() 将 SQL 语句包装起来，以使 SQLAlchemy 明白这是一个原始 SQL 语句。
        db.session.execute(text('ALTER TABLE basemachine AUTO_INCREMENT = 1;'))
        db.session.commit()
        for i in range(3):
            mac = BaseMachine(name = machine_names[i], type = machine_types[i])
            db.session.add(mac)
            db.session.commit()
        flash("All machines added successfully", category='success')
    except Exception as e:
        db.session.rollback()
        flash(f"Error: {str(e)}", category='error')

    current_user = User.query.get(bid)
    machines = BaseMachine.query.all()
    return render_template('stat/machine.html',machines = machines,current_user = current_user)

@blue.route('/machine_detail/<int:id>/<int:bid>')
def machine_detail(id,bid):
    current_user = User.query.get(bid)

    # 使用字典映射来简化机器模型的选择
    mac_model = machine_models.get(id)
    if mac_model is None:
        # 如果 id 不在字典中，返回 404 错误
        return "Machine type not found", 404
    
    mac = mac_model.query.all()  # 查询对应类型的所有机器
    return render_template('stat/show_machine.html',_id = id,machines = mac,current_user = current_user)

@blue.route('/material/<int:bid>')
def material_list(bid):
    materials = BaseMaterial.query.all()
    current_user = User.query.get(bid)
    return render_template('stat/material.html',materials = materials,current_user = current_user)

@blue.route('/simulation/<int:bid>', methods=['GET', 'POST'])
def sim_list(bid):
    current_user = User.query.get(bid)
    if request.method == 'POST':
        form = SumForm()
        client_send(client= current_app.config.get('client'),msg = request.form.get('material_num'))
        flash(message= "Message sent successfully!", category= "success") 
    
    return render_template('simulation/sim.html',current_user = current_user)


'''
@blue.route('/booklist/')
def book_list():
    books = Book.query.all()
    return render_template('book_list.html', books=books)

@blue.route('/bookdetail/<int:bid>/')   # 路由传参
def book_detail(bid):
    book = Book.query.get(bid)
    return render_template('book_detail.html', book=book)

# 作者详情
@blue.route('/authordetail/<int:aid>/')   # 路由传参
def author_detail(aid):
    author = Author.query.get(aid)
    return render_template('author_detail.html', author=author)         # 渲染 传参

# 出版社详情
@blue.route('/publisherdetail/<int:pid>/')   # 路由传参
def publisher_detail(pid):
    publisher = Publisher.query.get(pid)
    return render_template('publisher_detail.html', publisher=publisher)'''
