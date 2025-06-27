# run.py (最终生产版)

from my_flask_app import create_app

# 创建应用实例，Gunicorn 会自动找到这个名为 'app' 的变量
app = create_app()

# 注意：这里不再有数据库迁移逻辑，也不再有 if __name__ == '__main__'