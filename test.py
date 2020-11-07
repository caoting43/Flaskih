# from ronglian_sms_sdk import SmsSDK
#
# accId = '8a216da874af5fff0174b997014c04eb'
# accToken = '91ca470532d049d9ae2bc3726d9036c4'
# appId = '8a216da874af5fff0174b997025604f2'
#
#
# def send_message():
#     sdk = SmsSDK(accId, accToken, appId)
#     tid = '1'
#     mobile = '18168580698'
#     datas = ('786567', '5')
#     resp = sdk.sendMessage(tid, mobile, datas)
#     # print(resp)
#     # print("1")
#     return resp
#
# result = send_message()
# result = eval(result)
# print(result["statusCode"])


from ihome.models import User
from werkzeug.security import generate_password_hash, check_password_hash


res = User.query.filter_by(mobile="18168580698").first()
print(res)
#
# result = check_password_hash(User.get("password_hash"), "123456")
# print(result)
