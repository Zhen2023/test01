from my_flask_app import create_app
app = create_app()

# 运行应用
if __name__ == "__main__":
    app.run(debug=True)