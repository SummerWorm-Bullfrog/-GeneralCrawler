# *_*coding:utf-8 *_*
import re
import yq_worker.utils.tools as tools

def get_video_info(html):
    regx1 = '//video[@id="my_video_1"]/source/@src'
    result = tools.xpath_parser(html, regx1, fetch_one=True)
    print(result)
    image_url = 'http://www.legaldaily.com.cn/templateRes/201611/10/33946/33946/images/2016-zy-002.gif'
    if result:
        return result
if __name__ == '__main__':
    import requests
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36"
    }
    url = 'http://www.legaldaily.com.cn/video/content/2019-07/17/content_7938020.htm'
    content = requests.get(url, headers=headers).text
    result = get_video_info(content)
    if result:
        print("我是视频哦")
