from werkzeug.routing import BaseConverter


# 定义怎则表达式
class ReConverter(BaseConverter):

    def __init__(self, url_map, reqex):
        # 调用父类的初始化方法
        super(ReConverter, self).__init__(url_map)
        # 保存正则表达式
        self.regex = reqex
