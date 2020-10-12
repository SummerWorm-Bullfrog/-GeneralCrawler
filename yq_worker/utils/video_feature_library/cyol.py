# *_*coding:utf-8 *_*
import re
import yq_worker.utils.tools as tools
def get_video_info(html):
    regx1 = '//div[@name="video_bravo_vms"]/span/@name'
    regx2 = 'window=(.*?)&'
    result = tools.xpath_parser(html, regx1, fetch_one=True)
    image_url = tools.get_info(html, regx2, fetch_one=True)
    if result:
        print(result)
        return True
if __name__ == '__main__':
    import requests
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36"
    }
    url = 'http://news.cyol.com/yuanchuang/2019-08/01/content_18094097.htm'
    content = requests.get(url, headers=headers).text
    result = get_video_info(content)
    if result:
        print("我是视频哦")
