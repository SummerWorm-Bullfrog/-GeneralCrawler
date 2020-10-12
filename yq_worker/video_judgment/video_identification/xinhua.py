# *_*coding:utf-8 *_*
import yq_worker.utils.tools as tools
from yq_worker.video_judgment.base import Base
class XinHua(Base):
    def is_video(self, p):
        regx = r'<iframe class="pageVideo".*?src="(.*?)"'
        result = tools.get_info(p._html, regx, fetch_one=True)
        if result:
            video_url = result.replace("amp;","")
            return True
