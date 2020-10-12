# *_*coding:utf-8 *_*
import re
import yq_worker.utils.tools as tools
from yq_worker.video_judgment.base import Base
class Stdaily(Base):
    def is_video(self, p):
        regx = '<p id="video" align="center"><script src=(.*?) type="text/javascript"></script></p>'
        result = tools.get_info(p._html, regx, fetch_one=True)
        if result:
            return True

