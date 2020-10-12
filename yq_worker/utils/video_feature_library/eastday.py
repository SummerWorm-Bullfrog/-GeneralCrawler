# *_*coding:utf-8 *_*
import re
import yq_worker.utils.tools as tools

def get_video_info(html):
    regx = '//iframe[@name="flashimedia"]/@src'
    result = tools.xpath_parser(html, regx, fetch_one=True)
    image_url = "http://ej.eastday.com/images/2013newlogo/title_video.jpg"
    if result:
        return True
if __name__ == '__main__':
    import requests
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36"
    }
    url = 'http://imedia.eastday.com/node2/2015imedia/i/20190801/u8i781176.html'
    content = requests.get(url, headers=headers).text
    result = get_video_info(content)
    if result:
        print("我是视频哦")
