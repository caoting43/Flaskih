# -*- coding: utf-8 -*-
# flake8: noqa

from qiniu import Auth, put_data, etag
import qiniu.config

# 需要填写你的 Access Key 和 Secret Key
access_key = 'U9PYOMGxYwhURn4JcNX95miGHuiIVo7kSNjl9dMm'
secret_key = 'eM7YXKiqZraMQg6-N56t1YEK6TsQmpQuO7x6Mupn'


def storage(file_data):
    """
    上传图片到七牛
    :param file_data: 要上传的文件数据
    :return:
    """
    # 构建鉴权对象
    q = Auth(access_key, secret_key)

    # 要上传的空间
    bucket_name = 'my-puspace'

    # 生成上传 Token，可以指定过期时间等
    token = q.upload_token(bucket_name, None, 3600)

    ret, info = put_data(token, None, file_data)

    if info.status_code == 200:
        # 表示上传成功
        print(1)
        return ret.get("key")
    else:
        # 上传失败
        print(2)
        raise Exception("上传七牛失败")


if __name__ == '__main__':
    with open("./1.jpg", "rb") as f:
        file_data = f.read()
        storage(file_data)
