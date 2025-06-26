#auth/forms.py
from wtforms import StringField, TextAreaField, SubmitField, EmailField,BooleanField # 导入字段类型
from wtforms.validators import DataRequired, Email, EqualTo, Regexp, Length,ValidationError # 导入验证器
from flask_wtf import FlaskForm
from my_flask_app.models import User
class UserForm(FlaskForm):
    username = StringField('用户名',validators=[DataRequired(message= '用户名不能为空'),Length(min=2,max=20,message='用户名长度必须在2-20个字符之间')])
    name = StringField('姓名', validators=[DataRequired(message='姓名不能为空'),Length(min=2,max=20,message='姓名长度必须在2-20个字符之间')])
    tel = StringField('电话',validators=[DataRequired(message='电话不能为空'),Regexp(r'^1[3-9]\d{9}$',message='请输入正确的手机号码')])
    email = EmailField('邮箱',validators=[DataRequired(message='邮箱不能为空'),Email(message='请输入正确的邮箱地址')])
    note = TextAreaField('备注',validators=[Length(max=200,message='备注长度不能超过200个字符')])
    password = StringField('密码',validators=[DataRequired(message='密码不能为空'),Length(min=6,max=20,message='密码长度必须在6-20个字符之间')])
    confirm_password = StringField('确认密码',validators=[DataRequired(message='请再次输入密码'),EqualTo('password',message='两次输入的密码不一致')])
    submit = SubmitField('注册')

    def validate_username(self,username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('用户名已存在，请重新输入')

    def validate_email(self,email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('邮箱已存在，请重新输入')

class LoginForm(FlaskForm):
    username = StringField('用户名',validators=[DataRequired(message='用户名不能为空')])
    password = StringField('密码',validators=[DataRequired(message='密码不能为空'),Length(min=6,max=20,message='密码长度必须在6-20个字符之间')])
    remember = BooleanField('记住我')
    submit = SubmitField('登录')

    def validate_username(self,username):
        user = User.query.filter_by(username=username.data).first()
        if not user:
            raise ValidationError('用户名不存在，请重新输入')

    def validate_password(self,password):
        user = User.query.filter_by(username=self.username.data).first()
        if user and not user.check_password(password.data):
            raise ValidationError('密码错误，请重新输入')

class EditProfileForm(FlaskForm):
    name = StringField('姓名', validators=[DataRequired(message='姓名不能为空'),Length(min=2,max=20,message='姓名长度必须在2-20个字符之间')])
    tel = StringField('电话',validators=[DataRequired(message='电话不能为空'),Regexp(r'^1[3-9]\d{9}$',message='请输入正确的手机号码')])
    note = TextAreaField('备注',validators=[Length(max=200,message='备注长度不能超过200个字符')])
    submit = SubmitField('更细资料')