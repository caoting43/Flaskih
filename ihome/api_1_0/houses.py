from . import api
from ihome.utils.commons import login_required
from flask import g, current_app, request, jsonify
from ihome.utils.response_code import RET
from ihome.utils.image_storage import storage
from ihome.models import Area
from ihome import db, constants, redis_store
import json


@api.route("/areas")
def get_area_info():
    """获取城区信息"""
    # 尝试冲redis中读取数据
    try:
        resp_json = redis_store.get("area_info")
    except Exception as e:
        current_app.logger.error(e)
    else:
        if resp_json is not None:
            # redis有缓存数据
            current_app.logger.info("hit redis area_info")
            return resp_json, 200, {"Content-Type": "application/json"}

    # 查询数据库，读取城区信息
    try:
        all_li = Area.query.all()
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg="数据库异常")

    area_dict_li = list()
    # 将对象转换成字典
    for area in all_li:
        area_dict_li.append(area.to_dict())

    # 将对象转换为字典
    resp_dict = dict(errno=RET.OK, errmsg="OK", data=area_dict_li)
    resp_json = json.dumps(resp_dict)

    # 将数据保存到redis中
    try:
        redis_store.setex("area_info", constants.AREA_INFO_REDIS_CACHE_EXPIRES, resp_json)
    except Exception as e:
        current_app.logger.error(e)

    return resp_json, 200, {"Content-Type": "application/json"}
