# *_*coding:utf-8 *_*
import yq_worker.utils.tools as tools

from yq_worker.video_judgment.base import Base
class Gmw(Base):
    def is_video(self, p):
        regx1 = '//div[@id="MultiAttachPh"]/text()'
        regx2 = '//div[@id="PicUrlPh"]/img/@src'
        result = tools.xpath_parser(p._html, regx1, fetch_one=True)
        if result:
            video_url = result.replace("\r\n", '').strip()
            return True
