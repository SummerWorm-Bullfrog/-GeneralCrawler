# *_*coding:utf-8 *_*
import re
import yq_worker.utils.tools as tools
from yq_worker.video_judgment.base import Base
class WeiLai(Base):
    def is_video(self, p):
        regx1 = '//iframe/@src'
        regx2 = '//embed/@src'
        result1 = tools.xpath_parser(p._html, regx1, fetch_one=True)
        if result1:
            return True
        result2 = tools.xpath_parser(p._html, regx2, fetch_one=True)
        if result2:
            return True


