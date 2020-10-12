# *_*coding:utf-8 *_*
import yq_worker.utils.tools as tools
from yq_worker.video_judgment.base import Base
from yq_worker.video_judgment.video_identification.base_judge import BaseJudge

class ContentJudege(Base):
    def __init__(self, url, html):
        self._url = url
        self._html = html
        self.curr = BaseJudge()
    def set_website(self, p):
        self.curr = p
    def is_video(self):
        result = self.curr.is_video(self)
        return result
if __name__ == '__main__':
    import requests
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36"
    }
    url = 'http://www.xinhuanet.com/video/2019-06/02/c_1210149659.htm'
    content = requests.get(url, headers=headers).text
    c = ContentJudege(url, content)
    result = c.is_video()
    if result:
        print("我是视频哦")

