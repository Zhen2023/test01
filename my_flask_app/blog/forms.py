#blog/forms.py

from wtforms import StringField, TextAreaField, SubmitField # 导入字段类型
from wtforms.validators import DataRequired, Length # 导入验证器
from flask_wtf import FlaskForm


class PostForm(FlaskForm):
    title = StringField('标题',validators=[DataRequired(message='标题不能为空'),Length(max=100,message='标题长度不能超过100个字符')])
    content = TextAreaField('内容',validators=[DataRequired(message='内容不能为空')])
    tags_string = StringField('标签',validators=[Length(max = 100,message='标签长度不能超过100个字符')])
    submit = SubmitField('提交')

class CommentForm(FlaskForm):
    content = TextAreaField('发表你的看法吧',validators=[DataRequired(message='评论内容不能为空'),Length(max=500,message='评论内容长度不能超过500个字符')])
    submit = SubmitField('提交')
