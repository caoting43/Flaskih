from . import api
from ihome.utils.commons import login_required
from flask import g, current_app, request, jsonify
from ihome.utils.response_code import RET
from ihome.utils.image_storage import storage
from ihome.models import Area
from ihome import db, constants


@api.route("/areas")
def get_area_info():
    """获取城区信息"""

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

    return jsonify(errno=RET.OK, errmsg="OK", data=area_dict_li)
