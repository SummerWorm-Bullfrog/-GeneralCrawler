# *_*coding:utf-8 *_*
import re
import yq_worker.utils.tools as tools

def get_video_info(root_url, html):
    id = re.search('\d+', root_url).group()
    regx = '//video[@id="video{}"]/source/@src'.format(id)
    regx2 = '"poster": "(.*?)"'
    result = tools.xpath_parser(html, regx, fetch_one=True)
    image_url = tools.get_info(html, regx2, fetch_one=True)
    if result:
        return True
if __name__ == '__main__':
    import requests
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36"
    }
    url = 'https://www.thepaper.cn/newsDetail_forward_4058886'
    content = requests.get(url, headers=headers).text
    result = get_video_info(url, content)
    if result:
        print("我是视频哦")
