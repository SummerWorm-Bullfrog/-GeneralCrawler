# *_*coding:utf-8 *_*
import re
import yq_worker.utils.tools as tools
from yq_worker.video_judgment.base import Base
class QQ(Base):
    def is_video(self, p):
        regx = 'VIDEO_INFO = {(.*?)}'
        result = tools.get_info(p._html, regx, fetch_one=True)
        image_url = "http://mat1.gtimg.com/pingjs/ext2020/newom/build/static/images/logo.png"
        if result:
            return True
