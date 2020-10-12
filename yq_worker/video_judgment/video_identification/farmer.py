# *_*coding:utf-8 *_*
import re
import yq_worker.utils.tools as tools
from yq_worker.video_judgment.base import Base
class Farmer(Base):
    def is_video(self, p):
        regx = '//iframe/@src'
        result = tools.xpath_parser(p._html, regx, fetch_one=True)
        image_url = 'http://www.farmer.com.cn/images/%E4%B8%AD%E5%9B%BD%E5%86%9C%E4%B8%9A%E6%96%B0%E9%97%BB%E7%BD%91%E7%BA%A2%E8%89%B2LOGO.png'
        if result:
            return True
