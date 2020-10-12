# *_*coding:utf-8 *_*
import re
import yq_worker.utils.tools as tools
from yq_worker.video_judgment.base import Base
class Legaldaily(Base):
    def is_video(self, p):
        regx1 = '//video[@id="my_video_1"]/source/@src'
        result = tools.xpath_parser(p._html, regx1, fetch_one=True)
        image_url = 'http://www.legaldaily.com.cn/templateRes/201611/10/33946/33946/images/2016-zy-002.gif'
        if result:
            return result
