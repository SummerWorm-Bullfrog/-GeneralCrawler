# *_*coding:utf-8 *_*
import re
import yq_worker.utils.tools as tools
from yq_worker.video_judgment.base import Base
class DangJian(Base):
    def is_video(self, p):
        regx = r'flashvars="(.*?)"'
        result = tools.get_info(p._html, regx, fetch_one=True)
        image_url = 'http://images.wenming.cn/web_djw/images/mylogo15072401.jpg'
        if result:
            return True
