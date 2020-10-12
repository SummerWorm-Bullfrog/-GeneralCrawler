# *_*coding:utf-8 *_*
import re
import execjs
import time
import requests
import yq_worker.utils.tools as tools
from yq_worker.utils.tools import xpath_parser

def get_video_info(html):
    node = execjs.get()
    jqury = '"jQuery" + ("1.11.3" + Math.random()).replace(/\D/g, "")'
    para = node.eval(jqury)
    ts = int(time.time() * 1000)
    regx = '//div[@id="cmplayer"]/@data-media'
    url1 = xpath_parser(html, regx, fetch_one=True)
    id = re.search(r'id=(.*?)&', url1).group(1)
    o_url = 'http://yspmvms.81.cn/?id={}&callbackparam={}_{}&ctype=sd&ttype=pc&_={}'.format(id, para, ts, ts)
    video_info = requests.get(o_url).text
    regx2 = '"(.*)"'
    video_url = tools.get_info(video_info, regx2, fetch_one=True)
    if video_url:
        print(video_url)
if __name__ == '__main__':
    import requests
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36"
    }
    url = 'http://tv.81.cn/jbmtd/2019-07/29/content_9571947.htm'
    content = requests.get(url, headers=headers).text
    result = get_video_info(content)
    if result:
        print("我是视频哦")