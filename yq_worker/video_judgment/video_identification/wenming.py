# *_*coding:utf-8 *_*
import re
import yq_worker.utils.tools as tools
from yq_worker.video_judgment.base import Base
class WenMing(Base):
    def is_video(self, p):
        regx1 = '//video[@id="example_video_1"]/@poster'
        regx2 = '//video[@id="example_video_1"]/source/@src'
        image_url = tools.xpath_parser(p._html, regx1, fetch_one=True)
        result = tools.xpath_parser(p._html, regx2, fetch_one=True)
        if result:
            return result
