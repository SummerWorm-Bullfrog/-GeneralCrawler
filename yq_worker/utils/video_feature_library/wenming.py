# *_*coding:utf-8 *_*
import re
import yq_worker.utils.tools as tools

def get_video_info(html):
    regx1 = '//video[@id="example_video_1"]/@poster'
    regx2 = '//video[@id="example_video_1"]/source/@src'
    image_url = tools.xpath_parser(html, regx1, fetch_one=True)
    result = tools.xpath_parser(html, regx2, fetch_one=True)
    if result:
        return result
if __name__ == '__main__':
    import requests
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36"
    }
    url = 'http://www.wenming.cn/zgwmw_ysp/ysp_ws/201903/t20190305_5026930.shtml'
    content = requests.get(url, headers=headers).text
    result = get_video_info(content)
    if result:
        print("我是视频哦")
