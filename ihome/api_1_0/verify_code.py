# coding:utf-8

from . import api
from ihome.utils.captcha.captcha import captcha
from ihome import redis_store, constants
from flask import current_app, jsonify, make_response, request
from ihome.utils.response_code import RET
from ihome.models import User
import random
from ronglian_sms_sdk import SmsSDK
import sys


@api.route("/image_codes/<image_code_id>")
def get_image_code(image_code_id):
    """
    前端获取验证码
    :return:    验证码图片  异常：返回json
    """
    # 业务逻辑处理
    # 生产验证码图片
    # 名字，真是文本，图片数据
    name, text, image_data = captcha.generate_captcha()

    # 将验证码真实值与编号保存到redis中，设置有效期
    # redis数据类型：字符串 列表  哈希  set
    # "key"：xxx
    # 使用哈希维护有效期的时候只能整体设置
    # image_codes:{"":"","":""}

    # redis_store.set("image_code_%s" % image_code_id, text)
    # redis_store.expire("image_code_%s" % image_code_id, constants.IMAGE_CODE_REDIS_EXPIRES)
    #                       名字                          有效期                             记录值
    try:
        redis_store.setex("image_code_%s" % image_code_id, constants.IMAGE_CODE_REDIS_EXPIRES, text)
        current_app.logger.error("***************************")
        current_app.logger.error("获取图片中。。。")
    except Exception as e:
        # 记录日志
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg="save image code id failed")
    # 返回图片
    resp = make_response(image_data)
    resp.headers["Content-Type"] = "image/jpg"
    return resp


# GET /api/v1.0/sms_codes/<mobile>?image_code=xxxx&image_code_id=xxxx
# @api.route("/sms_codes/<re(r'1[34578]\d{9}'):mobile>")
@api.route("/sms_codes/<re(r'1[34578]\d{9}'):mobile>")
def get_sms_code(mobile):
    """获取短信验证码"""

    # 获取参数
    image_code = request.args.get("image_code")
    image_code_id = request.args.get("image_code_id")
    # 校验参数
    if not all([image_code, image_code_id]):
        # 表示参数不完整
        return jsonify(errno=RET.PARAMERR, errmsg="参数不完整")

    # 业务逻辑处理
    # 从redis中取出真实的图片验证码
    try:
        real_image_code = redis_store.get("image_code_%s" % image_code_id)
        if real_image_code is not None:
            real_image_code = str(real_image_code, encoding='utf-8')
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg="redis数据库异常")
    current_app.logger.debug("************************************")
    current_app.logger.debug("正在获取验证码。。。：{}".format(real_image_code))
    # 判断图片验证码是否过期
    if real_image_code is None:
        # 表示图片验证码没有或者过期
        return jsonify(errno=RET.NODATA, errmsg="图片验证码失效")

    # 删除redis中的图片验证码，防止用户使用同一个图片验证码验证多次
    try:
        redis_store.delete("image_code_%s" % image_code_id)
    except Exception as e:
        current_app.logger.error(e)

    # 与用户填写的值进行对比
    if real_image_code.lower() != image_code.lower():
        # 表示用户填写错误
        current_app.logger.debug("************************************")
        current_app.logger.debug("real_image_code：{}".format(real_image_code.lower()))
        current_app.logger.debug("image_code：{}".format(image_code.lower()))
        return jsonify(errno=RET.DATAERR, errmsg="图片验证码错误")

    # 判断对于这个手机号的操作，在60秒内没有之前的记录，如果有，则认为用户操作频繁，不接受处理
    try:
        send_flag = redis_store.get("send_sms_code_%s" % mobile)
    except Exception as e:
        current_app.logger.error(e)
    else:
        if send_flag is not None:
            # 表示在60秒内有过发送记录
            return jsonify(errno=RET.REQERR, errmsg="请求过于频繁，请60秒之后再试")

    # 判断手机号是否存在
    try:
        user = User.query.filter_by(mobile=mobile).first()
    except Exception as e:
        current_app.logger.error(e)
    else:
        if user is not None:
            # 表示手机号已存在
            return jsonify(errno=RET.DATAEXIST, errmsg="手机号已存在")

    # 如果手机号不存在，则生成短信验证码
    sms_code = "%06d" % random.randint(0, 999999)

    # 保存真实的短信验证码
    try:
        redis_store.setex("sms_code_%s" % mobile, constants.SMS_CODE_REDIS_EXPIRES, sms_code)
        # 保存发送给这个手机号的记录，防止用户在60s内再次出发发送短信操作
        redis_store.setex("send_sms_code_%s" % mobile, constants.SEND_SMS_CODE_INTERVAL, 1)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg="保存短信验证码异常")

    # 发送短信
    def send_message():
        accId = '8a216da874af5fff0174b997014c04eb'
        accToken = '91ca470532d049d9ae2bc3726d9036c4'
        appId = '8a216da874af5fff0174b997025604f2'
        sdk = SmsSDK(accId, accToken, appId)
        tid = '1'
        # mobile = '18168580698'
        datas = (sms_code, round(constants.SMS_CODE_REDIS_EXPIRES / 60))
        resp = sdk.sendMessage(tid, mobile, datas)
        # print(resp)
        return resp

    try:
        result = send_message()
        result = eval(result)
        print(result["statusCode"])
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.THIRDERR, errmsg="发送异常")

    # 返回值
    if result["statusCode"] == "000000":
        # 发送成功
        return jsonify(errno=RET.OK, errmsg="发送成功")
    else:
        current_app.logger.error(result["statusCode"])
        return jsonify(errno=RET.THIRDERR, errmsg="发送失败")
