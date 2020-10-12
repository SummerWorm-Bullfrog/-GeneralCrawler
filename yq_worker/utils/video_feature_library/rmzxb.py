# *_*coding:utf-8 *_*
import re

import yq_worker.utils.tools as tools
def get_video_info(html):
    regx1 = "file:'(.*?)'"
    regx2 = "image:'(.*?)',"
    result = tools.get_info(html, regx1, fetch_one=True)
    result = "http://www.rmzxb.com.cn" + result
    image_url = tools.get_info(html, regx2, fetch_one=True)
    image_url = "http://www.rmzxb.com.cn" + image_url
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
