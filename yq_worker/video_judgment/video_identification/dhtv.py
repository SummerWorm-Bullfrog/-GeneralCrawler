# *_*coding:utf-8 *_*
import re
import yq_worker.utils.tools as tools
from yq_worker.video_judgment.base import Base
class Dhtv(Base):
    def is_video(self, p):
        regx1 = 'vid:(.*?)//'
        regx2 = r"'img_url': '(.*?)',"
        vid = tools.get_info(p._html, regx1, fetch_one=True)
        url = "http://v.dhtv.cn/api/?mod=video&vid={}".format(vid)
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36"
        }
        json_content = requests.get(url, headers=headers).json()
        result = json_content["video"]["source"]
        image_url = tools.get_info(p._html, regx2, fetch_one=True)
        if result:
            return result
if __name__ == '__main__':
    import requests
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36"
    }
    url = 'http://tv.dhtv.cn/news/dswz/000033228.html'
    content = requests.get(url, headers=headers).text
    result = get_video_info(content)
    if result:
        print("我是视频哦")
