# *_*coding:utf-8 *_*
import re
import yq_worker.utils.tools as tools
import yq_worker.utils.tools as tools
from yq_worker.video_judgment.base import Base
class WangYi(Base):
    def is_video(self, p):
        regx = 'video/mp4'
        result = tools.get_info(p._html, regx, fetch_one=True)
        if result:
            return True
