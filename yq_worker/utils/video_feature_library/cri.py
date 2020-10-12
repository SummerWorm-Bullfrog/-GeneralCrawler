# *_*coding:utf-8 *_*
import yq_worker.utils.tools as tools

def get_video_info(html):
    regx = '<video.*?src="(.*?)" title'
    result = tools.get_info(html, regx, fetch_one=True)
    if result:
        return True
if __name__ == '__main__':
    import requests
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36"
    }
    url = 'http://news.cri.cn/20190725/f6329b86-8747-1023-6cef-4606eddf164b.html'
    content = requests.get(url, headers=headers).text
    result = get_video_info(content)
    if result:
        print("我是视频哦")
