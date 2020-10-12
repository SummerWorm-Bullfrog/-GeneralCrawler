# *_*coding:utf-8 *_*
import re
import yq_worker.utils.tools as tools
from yq_worker.video_judgment.base import Base
class Sina(Base):
    def is_video(self, p):
        video_regx1 = "swfOutsideUrl:'(.*?)',"
        video_regx2 = "video-play-count"
        img_regx1 = "pic: '(.*?)',"
        # print(p._html)
        result1 = tools.get_info(p._html, video_regx1, fetch_one=True)
        if video_regx2 in p._html:
            return True

        image_url = tools.get_info(p._html, img_regx1, fetch_one=True)
        if result1:
            return True

