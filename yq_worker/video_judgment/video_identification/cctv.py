# *_*coding:utf-8 *_*
import yq_worker.utils.tools as tools
from yq_worker.video_judgment.base import Base
class CCTV(Base):
    def is_video(self, p):
        regx1 = r'fo.addVariable\(\"url\", \"(.*?)\"\);'
        video_url = tools.get_info(p._html, regx1,  fetch_one=True)
        if video_url:
            return True
