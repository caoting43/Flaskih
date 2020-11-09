from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)

class Config(object):
    """配置信息"""
    DEBUG = True

    SECRET_KEY = "AJHSDJHAJKSHDJKASHD"

    # 数据库
    SQLALCHEMY_DATABASE_URI = "mysql://root:root1234@127.0.0.1:3306/ihome_python04"
    SQLALCHEMY_TRACK_MODIFICATIONS = True


app.config.from_object(Config)

db = SQLAlchemy(app)


@app.route("/index")
def index():
    return "index page"


if __name__ == '__main__':
    app.run()
