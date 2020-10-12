# *_*coding:utf-8 *_*
import re
import yq_worker.utils.tools as tools
from yq_worker.video_judgment.base import Base
class ChinaNews(Base):
    def is_video(self, p):
        regx = 'so.addVariable\("vInfo", "(.*?)"\);'
        result = tools.get_info(p._html, regx, fetch_one=True)
        image_url = 'http://i8.chinanews.com/2016cns/video/2_03.jpg'
        if result:
            return True
