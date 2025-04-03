# 在views.py中放路由和视图函数

from flask import Blueprint, request, render_template, url_for, redirect, flash, current_app, g, jsonify
 #后面是用views来控制数据库的，所以要在views中导入models文件                 flask db migrate 代码在这里实现
from App.models.User.user_model import *
from App.models.Machine.machine_model import *
from App.models.Material.Workpiece import *
from sqlalchemy import text

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, EmailField
from wtforms.validators import InputRequired, Email, Length

# from Clients.client import client_send
import subprocess  # 必须添加的导入
import math

import os

# 蓝图
blue = Blueprint('book', __name__)

# 用字典模拟一个简单的用户数据库（仅用于演示）
users = {
    "admin": "1",
    "user": " "
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
        db.session.query(BaseMachine).delete()
        db.session.commit()
        # flash("删除成功", 'success')
    except Exception as e:
        db.session.rollback()
        # flash(f"删除失败: {str(e)}", 'danger')

    # 重定向到machine 页面
    machines = BaseMachine.query.all()
    current_user = User.query.get(bid)
    return render_template('stat/machine.html',machines = machines,current_user = current_user)

@blue.route('/machine/add/<int:user_id>', methods=['GET', 'POST'])
def add_machine(user_id):
    if request.method == 'POST':
        try:
            # 获取表单数据
            new_machine = BaseMachine(
                m_id=request.form.get('m_id'),          # 机床ID
                m_number=request.form.get('m_number'),  # 机床编码
                m_name=request.form.get('m_name'),      # 机床名称
                m_state=request.form.get('m_state'),    # 机床状态
                m_time=0.0,                             # 初始运行时间
                m_workshop=request.form.get('m_workshop')  # 所在车间
            )
            
            db.session.add(new_machine)
            db.session.commit()
            # flash('机器添加成功', 'success')
            return redirect(url_for('book.machine_list', bid=user_id))
            
        except Exception as e:
            db.session.rollback()
            # flash(f'添加失败: {str(e)}', 'danger')

    # GET请求显示表单页面
    current_user = User.query.get(user_id)
    return render_template('stat/machine_add.html', current_user=current_user)

@blue.route('/simulation/<int:bid>', methods=['GET', 'POST'])
def sim_list(bid):
    current_user = User.query.get(bid)
    # if request.method == 'POST':
    #     form = SumForm()
    #     client_send(client= current_app.config.get('client'),msg = request.form.get('material_num'))
    #     flash(message= "Message sent successfully!", category= "success") 
    
    return render_template('simulation/sim.html',current_user = current_user)

@blue.route('/machine/delete/<int:machine_id>/<int:user_id>', methods=['POST'])
def machine_delete(machine_id,user_id):
    try:
        machine = BaseMachine.query.get_or_404(machine_id)
        db.session.delete(machine)
        db.session.commit()
        # flash('删除成功', 'success')
    except Exception as e:
        db.session.rollback()
        # flash(f'删除失败: {str(e)}', 'danger')
    # 保持原重定向方式
    return redirect(url_for('book.machine_list', bid=user_id))

# 编辑页面（GET显示表单）
@blue.route('/machine/edit/<int:machine_id>/<int:user_id>')
def machine_edit(machine_id,user_id):
    machine = BaseMachine.query.get_or_404(machine_id)
    current_user = User.query.get(user_id)
    return render_template('stat/machine_edit.html', 
                         machine=machine,
                         current_user=current_user)

# 处理编辑提交（POST更新数据）
@blue.route('/machine/update/<int:machine_id>/<int:user_id>', methods=['POST'])
def machine_update(machine_id,user_id):
    machine = BaseMachine.query.get_or_404(machine_id)
    try:
        # 更新机床信息
        machine.m_number = request.form.get('m_number')
        machine.m_name = request.form.get('m_name')
        machine.m_state = request.form.get('m_state')
        machine.m_workshop = request.form.get('m_workshop')
        machine.m_time = float(request.form.get('m_time', 0))  # 确保 m_time 是浮点数
        
        db.session.commit()
        # flash('更新成功', 'success')
    except Exception as e:
        db.session.rollback()
        # flash(f'更新失败: {str(e)}', 'danger')
    
    return redirect(url_for('book.machine_list', bid=user_id))


@blue.route('/workpiece/<int:bid>')
def workpiece_list(bid):
    pieces = Workpiece.query.all()
    current_user = User.query.get(bid)
    return render_template('workpiece/list.html', pieces=pieces, current_user=current_user)

@blue.route('/workpiece/add/<int:user_id>', methods=['GET', 'POST'])
def workpiece_add(user_id):
    if request.method == 'POST':
        try:
            # 获取表单数据
            j_id = request.form['j_id']  # 新增的工件ID字段
            j_number = request.form['j_number']
            c_name = request.form['c_name']
            p_number = request.form['p_number']
            j_quantity = int(request.form['j_quantity'])
            
            # 处理时间字段（datetime-local 格式: "YYYY-MM-DDTHH:MM"）
            j_create_date = datetime.strptime(
                request.form['j_create_date'], 
                '%Y-%m-%dT%H:%M'
            ) if request.form['j_create_date'] else None
            
            j_due_date = datetime.strptime(
                request.form['j_due_date'], 
                '%Y-%m-%dT%H:%M'
            ) if request.form['j_due_date'] else None
            
            j_remark = request.form.get('j_remark', '')

            # 创建新工件对象
            new_piece = Workpiece(
                j_id=j_id,  # 新增字段
                j_number=j_number,
                c_name=c_name,
                p_number=p_number,
                j_quantity=j_quantity,
                j_create_date=j_create_date,  # 新增字段
                j_due_date=j_due_date,
                j_remark=j_remark,
            )

            db.session.add(new_piece)
            db.session.commit()
            flash('添加成功', 'success')
            return redirect(url_for('book.workpiece_list', bid=user_id))
        except Exception as e:
            db.session.rollback()
            flash(f'添加失败: {str(e)}', 'danger')
    current_user = User.query.get(user_id)
    return render_template('workpiece/add.html', current_user=current_user)

@blue.route('/workpiece/delete/<int:j_id>/<int:user_id>', methods=['POST'])
def workpiece_delete(j_id, user_id):
    piece = Workpiece.query.get_or_404(j_id)
    db.session.delete(piece)
    db.session.commit()
    flash('删除成功', 'success')
    return redirect(url_for('book.workpiece_list', bid=user_id))


@blue.route('/operation/<int:bid>')
def operation_list(bid):
    operations = Operation.query.all()
    current_user = User.query.get(bid)
    return render_template('operation/list.html', operations=operations, current_user=current_user)

@blue.route('/operation/add/<int:user_id>', methods=['GET', 'POST'])
def operation_add(user_id):
    if request.method == 'POST':
        try:
            # 获取表单数据
            o_id = request.form['o_id']
            o_name = request.form.get('o_name', '')
            o_number = request.form.get('o_number', 0) 
            o_job_id = request.form['o_job_id']
            o_machine_name = request.form['o_machine_name']
            o_time = request.form.get('o_time')  # 加工时间
            o_index = request.form.get('o_index')  # 新增字段，默认值为0
            
            # 验证工件是否存在
            workpiece = Workpiece.query.get(o_job_id)
            if not workpiece:
                flash('错误: 指定的工件ID不存在', 'danger')
                return redirect(url_for('book.operation_list', bid=user_id))
            
            # 检查工序ID是否已存在
            if Operation.query.get(o_id):
                flash('错误: 工序ID已存在', 'danger')
                return redirect(url_for('book.operation_list', bid=user_id))
            
            # 创建新工序
            new_operation = Operation(
                o_id=o_id,
                o_name=o_name,
                o_number=o_number,
                o_job_id=o_job_id,
                o_machine_name=o_machine_name,
                o_time=o_time,
                o_index=o_index,  # 新增字段
            )
            
            db.session.add(new_operation)
            db.session.commit()
            
            flash('工序添加成功!', 'success')
        except ValueError:
            db.session.rollback()
            flash('错误: 加工时间必须是有效的数字', 'danger')
        except Exception as e:
            db.session.rollback()
            flash(f'添加失败: {str(e)}', 'danger')
    return redirect(url_for('book.operation_list', bid=user_id))

@blue.route('/operation/delete/<int:j_id>/<int:user_id>', methods=['POST'])
def operation_delete(j_id, user_id):
    operation = Operation.query.get_or_404(j_id)
    db.session.delete(operation)
    db.session.commit()
    flash('删除成功', 'success')
    return redirect(url_for('book.operation_list', bid=user_id))

@blue.route('/operation/<int:j_id>/<int:user_id>', methods=['POST'])
def operation_list_by_id(j_id, user_id):
    # 根据 workpiece_id 筛选工序
    operations = Operation.query.filter_by(o_job_id=j_id).all()
    current_user = User.query.get(user_id)
    return render_template('operation/list_by_id.html',j_id = j_id, operations=operations, current_user=current_user)

@blue.route('/schedule/a/<int:bid>')
def schedule_static(bid):
    current_user = User.query.get(bid)
    return render_template('schedule/schedule_static.html',  current_user=current_user)

@blue.route('/schedule/b/<int:bid>')
def schedule_dynamic(bid):
    current_user = User.query.get(bid)
    return render_template('schedule/schedule_dynamic.html', current_user=current_user)


@blue.route('/static_algorithm/<int:bid>', methods=['GET', 'POST'])
def static_algorithm(bid):
    result_image = None
    current_user = User.query.get(bid)
    if request.method == 'POST':
        action = request.form.get('action')
        
        if action == 'run':
            # 获取表单参数
            params = {
                'fitness_0': float(request.form.get('fitness_0')),
                'fitness_1': float(request.form.get('fitness_1')),
                'fitness_2': float(request.form.get('fitness_2')),
                'pop_size': int(request.form.get('pop_size')),
                'gene_size': int(request.form.get('gene_size')),
                'clone_size': int(request.form.get('clone_size')),
                'pc': float(request.form.get('pc')),
                'pm': float(request.form.get('pm'))
            }
            # 验证适应度权重总和≈1.0
            fitness_sum = sum(float(params[k]) for k in ['fitness_0', 'fitness_1', 'fitness_2'])
            if not math.isclose(fitness_sum, 1.0, abs_tol=0.001):
                flash(f'适应度权重总和必须等于1.0(当前: {fitness_sum:.3f})', 'danger')

            try:

                # 执行算法脚本 subprocess.run() 要求所有命令行参数都必须是字符串类型，但您直接传递了Python的float类型数值。
                cmd = [
                    'python', 'static_algorithm/Algorithm.py',
                    '--fitness_0', str(params['fitness_0']),  # 转换为字符串
                    '--fitness_1', str(params['fitness_1']),
                    '--fitness_2', str(params['fitness_2']),
                    '--pop_size', str(params['pop_size']),
                    '--gene_size', str(params['gene_size']),
                    '--clone_size', str(params['clone_size']),
                    '--pc', str(params['pc']),
                    '--pm', str(params['pm'])
                ]
                subprocess.run(cmd, check=True)
                result_image = 1
                # 假设算法生成的结果图片
                flash('算法执行成功!', 'success')


                # 获取全局client对象
                client = current_app.config.get('client')
                if not client:
                    flash('客户端连接未初始化', 'danger')
                    return redirect(url_for('book.static_algorithm', bid=bid))
                # 打开文件并读取内容
                    # 获取当前文件所在的目录
                current_directory = os.path.dirname(os.path.abspath(__file__))
                # 构建文件路径
                file_path = os.path.join(current_directory, 'static', 'static_result_chart', 'scheduling_info.txt')
                with open(file_path, 'r', encoding='utf-8') as file:
                    lines = file.readlines()

                # 将每行内容按顺序汇总成一个字符串，每行之间用逗号分隔  为了plant simulation 最后一个数据后面也要加一个”，“
                result = ','.join([line.strip() for line in lines])
                result += ","
                # 发送结果
                try:
                    client.send(result.encode('utf-8'))
                    flash(f'已发送结果: {result}', 'info')
                except Exception as send_error:
                    flash(f'结果发送失败: {str(send_error)} {result}', 'warning')
                
            except Exception as e:
                flash(f'算法执行失败: {str(e)}', 'danger')
                
    return render_template('schedule/schedule_static.html',  current_user=current_user, result_image= result_image)

@blue.route('/check_client_status')
def check_client_status():
    client = current_app.config.get('client')
    return jsonify({
        'connected': client is not None and hasattr(client, 'connected') and client.connected
    })