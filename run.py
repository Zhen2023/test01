# run.py (最终部署版)

import os
from my_flask_app import create_app, db
from flask_migrate import upgrade

# 创建应用实例
app = create_app()

# 在应用上下文中执行数据库迁移
with app.app_context():
    try:
        # 这个函数等同于 flask db upgrade 命令
        upgrade()
        print("--- Database migration check/upgrade completed. ---")
    except Exception as e:
        # 即使迁移失败，也打印错误并继续，让 Web 服务尝试启动
        print(f"--- Database migration failed: {e} ---")
        print("--- Continuing to start web server despite migration failure. ---")


# Gunicorn 会直接使用这个 app 对象来启动服务
# 下面的 if __name__ == '__main__': 块只在本地开发时运行
if __name__ == "__main__":
    # 在本地运行时，我们不需要从环境变量读取 PORT
    app.run(debug=True)