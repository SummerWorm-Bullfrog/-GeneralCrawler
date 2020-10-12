# *_*coding:utf-8 *_*
import re
import yq_worker.utils.tools as tools
from yq_worker.video_judgment.base import Base
class BjNews(Base):
    def is_video(self, p):
        regx = '//p[@id="video"]//a/@href'
        result = tools.xpath_parser(p._html, regx, fetch_one=True)
        image_url = "http://img.tbnimg.com/icon/bjnews_114.png"
        if result:
            return True
