# *_*coding:utf-8 *_*
import yq_worker.utils.tools as tools
#暂时未发现视频
def get_video_info(html):
    regx = r'<iframe class="pageVideo".*?src="(.*?)"'
    result = tools.get_info(html, regx, fetch_one=True)
    if result:
        video_url = result.replace("amp;","")
        return True
if __name__ == '__main__':
    import requests
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36"
    }
    url = 'http://www.gd.xinhuanet.com/newscenter/2019-07/29/c_1124812504.htm'
    content = requests.get(url, headers=headers).text
    result = get_video_info(content)
    if result:
        print("我是视频哦")
