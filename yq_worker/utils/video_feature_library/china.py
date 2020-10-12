# *_*coding:utf-8 *_*
import re
import yq_worker.utils.tools as tools
def get_video_info(html):
    regx = '//span[@id="videofile"]/@src'
    result = tools.xpath_parser(html, regx, fetch_one=True)
    image_url = "http://images.china.cn/images1/ch/2017video/2017video/logo.jpg"
    if result:
        return True
if __name__ == '__main__':
    import requests
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36"
    }
    url = 'http://news.china.com.cn/2019-08/01/content_75054143.htm'
    content = requests.get(url, headers=headers).text
    result = get_video_info(content)
    if result:
        print("我是视频哦")
