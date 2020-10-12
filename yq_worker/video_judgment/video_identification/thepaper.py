# *_*coding:utf-8 *_*
import re
import yq_worker.utils.tools as tools
from yq_worker.video_judgment.base import Base
class Thepaper(Base):
    def is_video(self, p):
        id = re.search('\d+', p._url).group()
        regx = '//video[@id="video{}"]/source/@src'.format(id)
        regx2 = '"poster": "(.*?)"'
        result = tools.xpath_parser(p._html, regx, fetch_one=True)
        image_url = tools.get_info(p._html, regx2, fetch_one=True)
        if result:
            return True

