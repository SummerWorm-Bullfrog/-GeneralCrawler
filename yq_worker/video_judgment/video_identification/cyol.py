# *_*coding:utf-8 *_*
import re
import yq_worker.utils.tools as tools
from yq_worker.video_judgment.base import Base
class Cyol(Base):
    def is_video(self, p):
        regx1 = '//div[@name="video_bravo_vms"]/span/@name'
        regx2 = 'window=(.*?)&'
        result = tools.xpath_parser(p._html, regx1, fetch_one=True)
        image_url = tools.get_info(p._html, regx2, fetch_one=True)
        if result:
            return True
