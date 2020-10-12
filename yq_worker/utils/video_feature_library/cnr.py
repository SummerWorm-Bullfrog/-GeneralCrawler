# *_*coding:utf-8 *_*
import yq_worker.utils.tools as tools
#暂时未发现视频
def get_video_info(html):
    regx = 'vurl="(.*?)";'
    result = tools.get_info(html, regx, fetch_one=True)
    if result:
        return True
if __name__ == '__main__':
    import requests
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36"
    }
    url = 'http://tv.cctv.com/2019/07/30/VIDE4iNnXZbVBU8qbEzxZScW190730.shtml?spm=C28340.P9dhkRStLqPh.E8KuwdzHZQNM.1'
    content = requests.get(url, headers=headers).text
    result, image_url = get_video_info(content)
