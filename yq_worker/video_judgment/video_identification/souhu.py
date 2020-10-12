# *_*coding:utf-8 *_*
import re
import yq_worker.utils.tools as tools
from yq_worker.video_judgment.base import Base
class SouHu(Base):
    def is_video(self, p):
        regx1 = "showVrsPlayer\((.*?)\)"
        result = tools.get_info(p._html, regx1, fetch_one=True)
        image_url = "http://css.tv.itc.cn/global/images/nav1/logo.gif"
        if result:
            return True
