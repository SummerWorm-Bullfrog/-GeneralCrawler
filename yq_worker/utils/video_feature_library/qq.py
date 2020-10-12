# *_*coding:utf-8 *_*
import re
import yq_worker.utils.tools as tools

def get_video_info(html):
    regx = 'VIDEO_INFO = {(.*?)}'
    result = tools.get_info(html, regx, fetch_one=True)
    image_url = "http://mat1.gtimg.com/pingjs/ext2020/newom/build/static/images/logo.png"
    if result:
        return True
if __name__ == '__main__':
    import requests
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36"
    }
    url = 'https://v.qq.com/x/cover/69jv4h59idcimc7/s09077lvdvk.html'
    content = requests.get(url, headers=headers).text
    result = get_video_info(content)
    if result:
        print("我是视频哦")
