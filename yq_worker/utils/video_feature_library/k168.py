# *_*coding:utf-8 *_*
import re
import yq_worker.utils.tools as tools
def get_video_info(html):
    regx1 = '//iframe/@src'
    regx2 = '//embed/@src'
    result1 = tools.xpath_parser(html, regx1, fetch_one=True)
    if result1:
        return True
    result2 = tools.xpath_parser(html, regx2, fetch_one=True)
    if result2:
        return True


if __name__ == '__main__':
    import requests
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36"
    }
    url = 'http://v.k618.cn/vlist/201907/t20190702_17489908.html'
    content = requests.get(url, headers=headers).text
    result = get_video_info(content)
    if result:
        print("我是视频哦")
