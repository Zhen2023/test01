# extensions.py

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
# 这里只创建实例，不关联 app
db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
