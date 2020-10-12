# *_*coding:utf-8 *_*
import re
import yq_worker.utils.tools as tools
def get_video_info(html):
    regx = '//iframe/@src'
    result = tools.xpath_parser(html, regx, fetch_one=True)
    image_url = 'http://www.farmer.com.cn/images/%E4%B8%AD%E5%9B%BD%E5%86%9C%E4%B8%9A%E6%96%B0%E9%97%BB%E7%BD%91%E7%BA%A2%E8%89%B2LOGO.png'
    if result:
        return True
if __name__ == '__main__':
    import requests
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36"
    }
    url = 'http://www.farmer.com.cn/2019/03/13/99818500.html'
    content = requests.get(url, headers=headers).text
    result = get_video_info(content)
    if result:
        print("我是视频哦")
