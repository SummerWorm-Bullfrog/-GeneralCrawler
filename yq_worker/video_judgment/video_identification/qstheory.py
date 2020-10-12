# *_*coding:utf-8 *_*
import yq_worker.utils.tools as tools
from yq_worker.video_judgment.base import Base
class Qsthrory(Base):
    def is_video(self, p):
        regx = r'<iframe class="pageVideo".*?src="(.*?)"'
        result = tools.get_info(p._html, regx, fetch_one=True)
        if result:
            video_url = result.replace("amp;","")
            return True
if __name__ == '__main__':
    import requests
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36"
    }
    url = 'http://tv.81.cn/jlwyx/2019-07/30/content_9572205.htm'
    content = requests.get(url, headers=headers).text
    result = get_video_info(content)
    if result:
        print("我是视频哦")
