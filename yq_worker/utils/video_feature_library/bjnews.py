# *_*coding:utf-8 *_*
import re
import yq_worker.utils.tools as tools

def get_video_info(html):
    regx = '//p[@id="video"]//a/@href'
    result = tools.xpath_parser(html, regx, fetch_one=True)
    image_url = "http://img.tbnimg.com/icon/bjnews_114.png"
    if result:
        return True
if __name__ == '__main__':
    import requests
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36"
    }
    url = 'http://www.bjnews.com.cn/video/2018/07/24/496575.html'
    content = requests.get(url, headers=headers).text
    result = get_video_info(content)
    if result:
        print("我是视频哦")
