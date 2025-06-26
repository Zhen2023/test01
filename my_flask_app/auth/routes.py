#auth/route.py

from flask_login import login_required,current_user,login_user,logout_user
from . import auth_bp
from flask import flash,render_template,request,url_for,redirect
from .forms import EditProfileForm, UserForm,LoginForm
from my_flask_app.models import User
from my_flask_app.extensions import db
from werkzeug.security import generate_password_hash


@auth_bp.route('/register',methods=['POST','GET'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = UserForm()
    if form.validate_on_submit():
        username = form.username.data
        name = form.name.data
        tel = form.tel.data
        email = form.email.data
        note = form.note.data
        password = generate_password_hash(form.password.data) 
        user = User(username=username,name=name,tel=tel,email=email,note=note,password=password)
        try:
            db.session.add(user)
            db.session.commit()
            flash("注册成功，即将跳转登录页面","success")
            return redirect(url_for('auth.login'))
        except Exception as e:
            db.session.rollback()
            flash(f"注册失败：{e}","danger")
            print(f"注册时发生未知异常：{e}")
    return render_template('auth/register.html',form=form,title = '注册页面')

@auth_bp.route('/login',methods=['POST','GET'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user,remember=form.remember.data)
            next_page = request.args.get('next')
            
            flash("登录成功","success")
            print(f"用户{user.username}登录成功")
            return redirect(next_page) if next_page else redirect(url_for('main.index'))
        else:
            flash("登录失败，用户名或密码错误","danger")
            print(f"用户{form.username.data}登录失败，用户名或密码错误")
    return render_template('auth/login.html',form=form,title = '登录页面')

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash("您已成功退出登录","success")
    print(f"用户{current_user.username}退出登录")
    return redirect(url_for('main.index'))

@auth_bp.route('/edit_profile',methods=['POST','GET'])
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.name=form.name.data
        current_user.tel=form.tel.data
        current_user.note=form.note.data
        try:
            db.session.commit()
            flash("个人资料更新成功")
            return redirect(url_for('main.user_profile',username=current_user.username))

        except Exception as e:
            db.session.rollback()
            flash(f"个人资料更新失败：{e}")
    
    elif request.method == 'GET':
        form = EditProfileForm(obj=current_user)
    
    return render_template('auth/edit_profile.html',title='编辑个人资料',form=form)
