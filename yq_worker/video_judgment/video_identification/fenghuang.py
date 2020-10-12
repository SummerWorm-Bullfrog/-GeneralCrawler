# *_*coding:utf-8 *_*
import re
import yq_worker.utils.tools as tools
from yq_worker.video_judgment.base import Base

class Ifeng(Base):
    def is_video(self, p):
        regx1 = '"videoPlayUrl": "(.*?)"'
        regx2 = '"videoLargePoster": "(.*?)",'
        result = tools.get_info(p._html, regx1, fetch_one=True)
        image_url = tools.get_info(p._html, regx2, fetch_one=True)
        if result:
            return result
        regx3 = '"videoPlayUrl":"(.*?)",'
        result2 = tools.get_info(p._html, regx3, fetch_one=True)
        if result2:
            return True
