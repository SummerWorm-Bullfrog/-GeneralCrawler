# *_*coding:utf-8 *_*
import re
import yq_worker.utils.tools as tools
from yq_worker.video_judgment.base import Base
class HuanQiu(Base):
    def is_video(self, p):
        char = r'addltype:"video"'
        regx1 = '//div[@id="vt-video"]/video/@src'
        regx2 = '//div[@id="vt-video"]/video/@poster'
        result = tools.xpath_parser(p._html, regx1, fetch_one=True)
        image_url = tools.xpath_parser(p._html, regx2, fetch_one=True)
        if result:
            return True
        regx = 'name="mvFlash" pluginspage=".*?" src="(.*?)"'
        flash_url = tools.get_info(p._html, regx, fetch_one=True)
        if flash_url:
            return True
        if char in p._html:
            return True

