# *_*coding:utf-8 *_*
import re
import yq_worker.utils.tools as tools
from yq_worker.video_judgment.base import Base
class EastDay(Base):
    def is_video(self, p):
        regx = '//iframe[@name="flashimedia"]/@src'
        result = tools.xpath_parser(p._html, regx, fetch_one=True)
        image_url = "http://ej.eastday.com/images/2013newlogo/title_video.jpg"
        if result:
            return True
