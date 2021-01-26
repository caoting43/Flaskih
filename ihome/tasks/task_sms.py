from celery import Celery
from ihome.libs.sms import send_message

celery_app = Celery("ihome", broker="redis://127.0.0.1:6379/1")


@celery_app.task
def send_sms(sms_code):
    """发送短信的异步任务"""
    send_msg = send_message(sms_code)
