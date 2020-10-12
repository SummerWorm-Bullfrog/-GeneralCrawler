# *_*coding:utf-8 *_*
import yq_worker.utils.tools as tools
from yq_worker.video_judgment.base import Base
class CRI(Base):
    def is_video(self, p):
        regx = '<video.*?src="(.*?)" title'
        result = tools.get_info(p._html, regx, fetch_one=True)
        if result:
            return True

