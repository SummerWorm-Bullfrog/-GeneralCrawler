# *_*coding:utf-8 *_*
import re
import execjs
import time
import requests
import yq_worker.utils.tools as tools
from yq_worker.utils.tools import xpath_parser
from yq_worker.video_judgment.base import Base
class Military(Base):
    def is_video(self, p):
        node = execjs.get()
        jqury = '"jQuery" + ("1.11.3" + Math.random()).replace(/\D/g, "")'
        para = node.eval(jqury)
        ts = int(time.time() * 1000)
        regx = '//div[@id="cmplayer"]/@data-media'
        url1 = xpath_parser(p._html, regx, fetch_one=True)
        id = re.search(r'id=(.*?)&', url1).group(1)
        o_url = 'http://yspmvms.81.cn/?id={}&callbackparam={}_{}&ctype=sd&ttype=pc&_={}'.format(id, para, ts, ts)
        video_info = requests.get(o_url).text
        regx2 = '"(.*)"'
        video_url = tools.get_info(video_info, regx2, fetch_one=True)
        if video_url:
            # print(video_url)
            return True
