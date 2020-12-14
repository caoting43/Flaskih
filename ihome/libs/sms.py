# 发送短信功能

from ronglian_sms_sdk import SmsSDK
from ihome import constants

accId = '8a216da874af5fff0174b997014c04eb'
accToken = '91ca470532d049d9ae2bc3726d9036c4'
appId = '8a216da874af5fff0174b997025604f2'


def send_message(sms_code):
    sdk = SmsSDK(accId, accToken, appId)
    tid = '1'
    mobile = '18168580698'
    datas = (sms_code, round(constants.SMS_CODE_REDIS_EXPIRES / 60))
    resp = sdk.sendMessage(tid, mobile, datas)
    # print(resp)
    return resp
