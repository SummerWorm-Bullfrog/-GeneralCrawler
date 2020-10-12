# *_*coding:utf-8 *_*
import re
import yq_worker.utils.tools as tools

def get_video_info(html):
    regx1 = "showVrsPlayer\((.*?)\)"
    result = tools.get_info(html, regx1, fetch_one=True)
    image_url = "http://css.tv.itc.cn/global/images/nav1/logo.gif"
    if result:
        return True
if __name__ == '__main__':
    import requests
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36"
    }
    url = 'https://www.sohu.com/a/330782057_356941?spm=smpc.home%2F72_2.yule-news11.2.1564646104829Tbd46uR&_f=index_yulenews_0_1_0'
    content = requests.get(url, headers=headers).text
    result = get_video_info(content)
    if result:
        print("我是视频哦")
