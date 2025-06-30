# my_flask_app/__init__.py

from flask import Flask, render_template, request, redirect, url_for
import os
from my_flask_app.extensions import db, migrate, login_manager

def create_app():#工厂函数
    
    app = Flask(__name__)
    #配置工厂函数中的工作室
    app.config['SECRET_KEY'] = 'a_very_secret_and_random_string_please_change_me'

   # 1. 从环境变量中获取 DATABASE_URL
    database_url = os.environ.get('DATABASE_URL')

    # 2. 如果是 PostgreSQL (Railway 会提供 postgresql://... 格式的 URL)，
    #    SQLAlchemy 1.4+ 推荐将 postgres:// 替换为 postgresql://
    if database_url and database_url.startswith("postgres://"):
        database_url = database_url.replace("postgres://", "postgresql://", 1)

    # 3. 如果环境变量存在，就用它；否则 (在本地开发时)，继续用 SQLite
    if database_url:
        app.config['SQLALCHEMY_DATABASE_URI'] = database_url
    else:
        basedir = os.path.abspath(os.path.dirname(__file__))
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'site.db')


    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['POSTS_PER_PAGE'] = 5
    # --- 在工作室里组装工具 ---
    db.init_app(app)
    migrate.init_app(app,db)
    login_manager.init_app(app)
    # --- 设置登录管理器 ---
    login_manager.login_view = 'auth.login'
    login_manager.login_message = '请先登录'
    login_manager.login_message_category = 'info'
    # --- 引入并注册蓝图 ---
    from .main import main_bp
    app.register_blueprint(main_bp)

    from .auth import auth_bp
    app.register_blueprint(auth_bp)

    from .blog import blog_bp
    app.register_blueprint(blog_bp)
    # --- 定义 user_loader ---
    # 必须在工厂函数内部导入 models，避免循环
    from .models import User
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
 
    return app

#准备启用PostgreSql数据库

# # 3. 运行应用 在工厂模式下，app.py被改成__init__.py，职责从被执行的主程序变成了仅定义工厂函数的文件，所以下面这段不能在这个文件出现，而是在run.py中出现
# if __name__ == '__main__':
#     # app.run() 启动了 Flask 内置的开发服务器。
#     # 当你运行这个脚本时，Flask 会监听本地主机的 5000 端口。
#     # debug=True 会启用调试模式，当代码有改动时服务器会自动重启，并且出错时会显示详细的错误信息。
#     # 在生产环境中，debug 模式必须关闭！
#     app = create_app()
#     app.run(debug=True)