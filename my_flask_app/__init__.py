# my_flask_app/__init__.py (最终全兼容版)

import os
from flask import Flask
from .extensions import db, migrate, login_manager

def create_app(): # 工厂函数
    
    app = Flask(__name__)

    # --- 核心配置 ---
    app.config['SECRET_KEY'] = 'a_very_secret_and_random_string_please_change_me'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['POSTS_PER_PAGE'] = 5

    # --- 数据库配置 (智能适配线上和本地) ---
    # 1. 优先从环境变量获取 DATABASE_URL
    database_url = os.environ.get('DATABASE_URL')
    
    if database_url:
        # 线上环境 (Railway)
        
        # 2. 检查 Railway 提供的 URL 格式，确保它能被 PyMySQL 驱动识别
        #    Railway 的 MySQL 环境变量可能是 "mysql://..." 格式
        if database_url.startswith("mysql://"):
            database_url = database_url.replace("mysql://", "mysql+pymysql://", 1)
            
        app.config['SQLALCHEMY_DATABASE_URI'] = database_url
        print("--- Connecting to PRODUCTION database (MySQL on Railway) ---")
    else:
        # 本地开发环境
        # 3. 如果没有环境变量，则使用写死在代码里的本地数据库连接字符串
        app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@localhost:3306/my_flask_blog_db'
        print("--- Connecting to LOCAL development database (MySQL on localhost) ---")

    # --- 初始化扩展 ---
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    
    # --- 设置登录管理器 ---
    login_manager.login_view = 'auth.login'
    login_manager.login_message = '请先登录'
    login_manager.login_message_category = 'info'
    
    # --- 在应用上下文中注册蓝图和加载器 ---
    #    这可以避免在导入时就执行蓝图代码，是一种更安全的做法
    with app.app_context():
        from . import main, auth, blog # 导入蓝图模块

        app.register_blueprint(main.main_bp)
        app.register_blueprint(auth.auth_bp)
        app.register_blueprint(blog.blog_bp)
        
        from .models import User
        @login_manager.user_loader
        def load_user(user_id):
            return User.query.get(int(user_id))
 
    return app