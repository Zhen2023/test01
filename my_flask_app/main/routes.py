# main/routes.py
from flask import render_template,redirect,url_for
from . import main_bp
from my_flask_app.models import User,Post

@main_bp.route('/')
def index():
    return redirect(url_for('blog.posts'))

@main_bp.route('/user/<string:username>')
def user_profile(username):
    user = User.query.filter_by(username=username).first_or_404()

    user_posts = sorted(user.posts,key=lambda p:p.create_time,reverse=True)
    return render_template('main/user_profile.html',user=user,posts=user_posts)