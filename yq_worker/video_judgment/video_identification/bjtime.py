# *_*coding:utf-8 *_*
import re
import yq_worker.utils.tools as tools
from yq_worker.video_judgment.base import Base
def get_video_info(html):
    regx = 'video-box'
    result = tools.get_info(html, regx, fetch_one=True)
    if result:
        return True


if __name__ == '__main__':
    import requests
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36"
    }
    url = 'https://item.btime.com/46g9kgjndlr9k0pgqn2f3l7vdpg'
    content = requests.get(url, headers=headers).text
    result = get_video_info(content)
    if result:
        print("我是视频哦")
