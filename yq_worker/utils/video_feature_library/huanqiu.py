# *_*coding:utf-8 *_*
import re
import yq_worker.utils.tools as tools
def get_video_info(html):
    regx1 = '//div[@id="vt-video"]/video/@src'
    regx2 = '//div[@id="vt-video"]/video/@poster'
    result = tools.xpath_parser(html, regx1, fetch_one=True)
    image_url = tools.xpath_parser(html, regx2, fetch_one=True)
    if result:
        return True
    regx = 'name="mvFlash" pluginspage=".*?" src="(.*?)"'
    flash_url = tools.get_info(html, regx, fetch_one=True)
    if flash_url:
        return True
if __name__ == '__main__':
    import requests
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36"
    }
    url = 'http://v.huanqiu.com/jiong/2018-01/11528688.html?agt=15438'
    content = requests.get(url, headers=headers).text
    result = get_video_info(content)
    if result:
        print("我是视频哦")
