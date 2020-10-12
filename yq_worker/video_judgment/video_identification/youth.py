# *_*coding:utf-8 *_*
import yq_worker.utils.tools as tools
from yq_worker.video_judgment.base import Base
class Youth(Base):
    def is_video(self, p):
        regx1 = ' //div[@class="video_content"]//embed/@flashvars'
        result = tools.xpath_parser(p._html, regx1, fetch_one=True)
        if result:
            return True
        regx2 = '//source[@id="youth_video_src_1"]/@src'
        video_url = tools.xpath_parser(p._html, regx2, fetch_one=True)
        if video_url:
            return True
        regx3 = '//video/@src'
        video_url2 = tools.xpath_parser(p._html, regx3, fetch_one=True)
        if video_url2:
            return True
