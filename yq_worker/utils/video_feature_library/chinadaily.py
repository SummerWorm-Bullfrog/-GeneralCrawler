# *_*coding:utf-8 *_*
import re

import yq_worker.utils.tools as tools

def get_video_info(html):
    regx1 = '//iframe[@id="playerFrame"]/@src'
    info = tools.xpath_parser(html, regx1, fetch_one=True)
    regx2 = 'src=(.*?)&'
    result = "http:" + tools.get_info(info, regx2, fetch_one=True)
    image_url = tools.xpath_parser(html, '//meta[@name="shareImg"]/@content', fetch_one=True)
    if result:
        return True
if __name__ == '__main__':
    import requests
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36"
    }
    url = 'http://cen.ce.cn/cevideo/jj/'
    content = requests.get(url, headers=headers).text
    result = get_video_info(content)
    if result:
        print("我是视频哦")
