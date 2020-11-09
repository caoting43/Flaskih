from flask import Flask, session
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session


import redis

app = Flask(__name__)


class Config(object):
    """配置信息"""
    DEBUG = True

    SECRET_KEY = "AJHSDJHAJKSHDJKASHD"

    # 数据库
    SQLALCHEMY_DATABASE_URI = "mysql://root:root1234@127.0.0.1:3306/ihome_python04"
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    REDIS_HOST = "127.0.0.1"
    REDIS_PORT = 6379

    # flask_session的配置
    SESSION_TYPE = "redis"
    SESSION_REDIS = redis.StrictRedis(host=REDIS_HOST,port=REDIS_PORT)
    SESSION_USE_SIGNER = True  # 对cookie中的session_id进行影藏处理
    PERMANENT_SESSION_LIFETIME = 86400 # session数据的有效期  单位秒

app.config.from_object(Config)

# 数据库
db = SQLAlchemy(app)

# 创建redis连接对象
redis_store = redis.StrictRedis(host=Config.REDIS_HOST, port=Config.REDIS_PORT)

# 利用flask_session，将session数据保存到redis中
Session(app)


@app.route("/index")
def index():
    return "index page"


if __name__ == '__main__':
    app.run()
