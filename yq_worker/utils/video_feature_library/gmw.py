# *_*coding:utf-8 *_*
import yq_worker.utils.tools as tools

def get_video_info(html):
    regx1 = '//div[@id="MultiAttachPh"]/text()'
    regx2 = '//div[@id="PicUrlPh"]/img/@src'
    result = tools.xpath_parser(html, regx1, fetch_one=True)
    if result:
        video_url = result.replace("\r\n", '').strip()
        return True
if __name__ == '__main__':
    import requests
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36"
    }
    url = 'http://reader.gmw.cn/2019-06/18/content_32929833.htm'
    content = requests.get(url, headers=headers).text
    result = get_video_info(content)
    if result:
        print("我是视频哦")
