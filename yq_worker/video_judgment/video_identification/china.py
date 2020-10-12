# *_*coding:utf-8 *_*
import re
import yq_worker.utils.tools as tools
from yq_worker.video_judgment.base import Base
class China(Base):
    def is_video(self, p):
        regx = '//span[@id="videofile"]/@src'
        result = tools.xpath_parser(p._html, regx, fetch_one=True)
        image_url = "http://images.china.cn/images1/ch/2017video/2017video/logo.jpg"
        if result:
            return True
