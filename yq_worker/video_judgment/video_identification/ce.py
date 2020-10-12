# *_*coding:utf-8 *_*
import yq_worker.utils.tools as tools
from yq_worker.video_judgment.base import Base
class Ce(Base):
    def is_video(self, p):
        regx1 = '//video/@src'
        regx2 = '//video/@poster'
        result = tools.xpath_parser(p._html, regx1, fetch_one=True)
        image_url = tools.xpath_parser(p._html, regx2, fetch_one=True)
        if result:
            return True
