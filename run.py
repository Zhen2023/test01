# run.py (最终部署调试版)

import os
from my_flask_app import create_app, db
from flask_migrate import upgrade

# 创建 Flask 应用实例
app = create_app()

# --- 部署时的数据库迁移逻辑 ---
# 在应用上下文中执行数据库迁移
with app.app_context():
    try:
        # 这个函数等同于 flask db upgrade 命令
        upgrade()
        # 在部署日志中打印成功信息
        print("--- Database migration check/upgrade completed. ---")
    except Exception as e:
        # 在部署日志中打印失败信息
        print(f"--- Database migration failed: {e} ---")


# --- 运行服务器 ---
if __name__ == "__main__":
    # Railway 会通过环境变量 PORT 告诉我们应该监听哪个端口
    # 如果在本地运行，PORT 不存在，我们就用默认的 5000
    port = int(os.environ.get("PORT", 5000))
    
    # 启动 Flask 自带的开发服务器
    # host='0.0.0.0' 是必须的，让服务器可以被外部访问
    # debug=False 在生产环境中更安全，但为了调试我们可以先设为 True
    app.run(host='0.0.0.0', port=port, debug=True)