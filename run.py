# run.py (最终部署版)
import os
from my_flask_app import create_app, db
from flask_migrate import upgrade

app = create_app()

with app.app_context():
    try:
        upgrade()
        print("--- Database upgrade successful. ---")
    except Exception as e:
        print(f"--- Database upgrade failed: {e} ---")

if __name__ == "__main__":
    app.run(debug=True)