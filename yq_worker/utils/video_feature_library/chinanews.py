# *_*coding:utf-8 *_*
import re
import yq_worker.utils.tools as tools
def get_video_info(html):
    regx = 'so.addVariable\("vInfo", "(.*?)"\);'
    result = tools.get_info(html, regx, fetch_one=True)
    image_url = 'http://i8.chinanews.com/2016cns/video/2_03.jpg'
    if result:
        return True
if __name__ == '__main__':
    import requests
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36"
    }
    url = 'http://www.chinanews.com/mil/shipin/cns/2019/08-01/news825773.shtml'
    content = requests.get(url, headers=headers).text
    result = get_video_info(content)
    if result:
        print("我是视频哦")
