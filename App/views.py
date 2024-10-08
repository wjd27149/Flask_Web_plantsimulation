# 在views.py中放路由和视图函数

from flask import Blueprint, request, render_template, url_for, redirect, flash, current_app, g
from .models import * #后面是用views来控制数据库的，所以要在views中导入models文件

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, EmailField
from wtforms.validators import InputRequired, Email, Length

# 蓝图
blue = Blueprint('book', __name__)

# 用字典模拟一个简单的用户数据库（仅用于演示）
users = {
    "admin": "1",
    "user": " "
}

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
        # 删除 BaseMachine 表中的所有记录
        db.session.query(BaseMachine).delete()
        db.session.commit()
        flash("All records deleted successfully", "success")
    except Exception as e:
        db.session.rollback()
        flash(f"Error: {str(e)}", "danger")

    # 重定向到machine 页面
    machines = BaseMachine.query.all()
    current_user = User.query.get(bid)
    return render_template('stat/machine.html',machines = machines,current_user = current_user)

@blue.route('/material/<int:bid>')
def material_list(bid):
    materials = Material.query.all()
    current_user = User.query.get(bid)
    return render_template('stat/material.html',materials = materials,current_user = current_user)

@blue.route('/simulation/<int:bid>', methods=['GET', 'POST'])
def sim_list(bid):
    current_user = User.query.get(bid)
    if request.method == 'POST':
        form = SumForm()
        return redirect(url_for('book.sim_list',current_user = current_user, sum = "20", bid = current_user.id))

    return render_template('simulation/sim.html',current_user = current_user)

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
    return render_template('publisher_detail.html', publisher=publisher)
