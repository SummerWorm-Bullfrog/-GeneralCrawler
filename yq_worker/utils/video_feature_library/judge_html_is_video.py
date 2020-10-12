import re
from urllib import parse
import time
import execjs
import requests
import time
import xmltodict
from yq_worker.utils.video_feature_library import *
from lxml import etree

def contain_video(root_url, html):
    try:
        #央广网（中国广播网）
        if judge_url_contained('cnr',root_url):
            regx1 = 'vurl="(.*?)";'
            result = re.search(regx1, html).group(1)
            if result:
                regx2 = 'cnrlogo="(.*?)";'
                image_url = re.search(regx2, html).group(1)
                return result,image_url
            else:
                return False
        #中国网络电视台（CNTV）
        elif judge_url_contained('cctv',root_url):
            video_id_regx = 'guid="(.*?)";'
            video_id = re.search(video_id_regx, html).group(1)
            if video_id:
                video_url = 'http://cntv.hls.cdn.myqcloud.com/asp/hls/2000/0303000a/3/default/{}/2000.m3u8'.format(video_id)
                regx2 = 'var videoImgUrl="(.*?)";'
                image_url = re.search(regx2, html).group(1)
                return video_url,image_url
            else:
                return False
        #国际在线
        elif judge_url_contained('cri',root_url):
            e = etree.HTML(html)
            try:
                result = "".join(e.xpath('//div[@id="abody"]/p/video/@src'))
                if result:
                    result = 'http:' + result
            except Exception as e:
                result = ""
            try:
                image_url = "".join(e.xpath('//div[@id="abody"]/p/video/@poster'))

            except Exception as e:
                image_url = ""
            if result:
                return result,image_url
            else:
                return False
        #人民网
        elif judge_url_contained('people',root_url):
            regx = 'showPlayer(.*?);'
            result = re.search(regx, html)
            image_url = 'http://v.people.cn/img/MAIN/2015/06/115595/images/ptv_all.png'
            if result:
                return root_url,image_url
            else:
                return False
        #新华网
        elif judge_url_contained('xinhuanet',root_url):
            print(root_url)
            try:
                regx1 = '<video src=" (.*?)" .*>'
                result = re.search(regx1, html).group(1)
            except Exception as e:
                regx2 = '//iframe[@class="pageVideo"]/@src'
                result = xpath_parser(html, regx2)
                result = result if len(result)>1 else result

            image_url = 'http://www.newsimg.cn/common/share/logo4share.jpg'
            if result:
                return result,image_url
            else:
                return False
        #求是网
        elif judge_url_contained('qstheory',root_url):
            regx = '//div[@id="videoArea"]/span/text()'
            result = xpath_parser(html, regx, fetch_one=True)
            image_url = 'http://www.qstheory.cn/n7/images/v7_logo_shipin_20190111.png'
            if result:
                result = result.strip("\r\n")
                return result,image_url
            else:
                return False
        #中国军网
        elif judge_url_contained('81',root_url):
            try:
                node = execjs.get()
                jqury = '"jQuery" + ("1.11.3" + Math.random()).replace(/\D/g, "")'
                para = node.eval(jqury)
                ts = int(time.time() * 1000)
                regx = '//div[@id="cmplayer"]/@data-media'
                url1 = xpath_parser(html, regx, fetch_one=True)
                id = re.search(r'id=(.*?)&', url1).group(1)
                o_url = 'http://yspmvms.81.cn/?id={}&callbackparam={}_{}&ctype=sd&ttype=pc&_={}'.format(id, para, ts, ts)
                video_info = requests.get(o_url).text
                regx2 = '"(.*)"'
                video_url = re.search(regx2, video_info).group(1)
            except Exception as e:
                video_url = ""
            image_url = 'http://tv.81.cn/jlwyx/37301.files/favicon.png'
            if video_url:
                return video_url,image_url
            else:
                return False
        #光明网
        elif judge_url_contained('gmw',root_url):
            regx1 = '//div[@id="MultiAttachPh"]/text()'
            regx2 = '//div[@id="PicUrlPh"]/img/@src'
            result = xpath_parser(html, regx1, fetch_one=True).replace("\r\n" , '').strip()
            image_url = xpath_parser(html, regx2, fetch_one=True)
            if not image_url:
                image_url = 'http://img.gmw.cn/pic/gmwLogo_share.jpg'
            if result:
                return result,image_url
            else:
                return False
        #中国经济网
        elif judge_url_contained('ce',root_url):
            regx1 = '//div[@class="mdysp"]/video/@src'
            regx2 = '//div[@class="mdysp"]/video/@poster'
            result = xpath_parser(html, regx1, fetch_one=True)
            image_url = xpath_parser(html, regx2, fetch_one=True)
            if not image_url:
                image_url = "http://www.ce.cn/img4/cealllogo.jpg"
            if result:
                return result,image_url
            else:
                return False
        #中国日报网
        elif judge_url_contained('chinadaily',root_url):
            regx1 = '//iframe[@id="playerFrame"]/@src'
            info = xpath_parser(html, regx1 , fetch_one=True)
            regx2 = 'src=(.*?)&'
            result = "http:" + re.search(regx2, info).group(1)
            image_url = xpath_parser(html, '//meta[@name="shareImg"]/@content', fetch_one=True)
            if result:
                return result,image_url
            else:
                return False
        #人民政协网
        elif judge_url_contained('rmzxb',root_url):
            regx1 = "file:'(.*?)'"
            regx2 = "image:'(.*?)',"
            result = re.search(regx1, html).group(1)
            result = "http://www.rmzxb.com.cn" + result
            image_url = re.search(regx2, html).group(1)
            image_url = "http://www.rmzxb.com.cn" + image_url
            if result:
                return result,image_url
            else:
                return False
        #环球网
        elif judge_url_contained('huanqiu',root_url):
            regx1 = '//div[@id="vt-video"]/video/@src'
            regx2 = '//div[@id="vt-video"]/video/@poster'
            result = xpath_parser(html, regx1, fetch_one=True)
            image_url = xpath_parser(html, regx2, fetch_one=True)

            if result:
                return result,image_url
            else:
                return False
        #中国青年网（暂未发现相关视频板块）
        elif judge_url_contained('youth',root_url):
            regx = 'application/x-shockwave-flash'
            result = re.search(regx, html)
            if result:
                return True
            else:
                return False
        #中青在线
        elif judge_url_contained('cyol',root_url):
            regx1 = '//div[@name="video_bravo_vms"]/span/@name'
            regx2 = 'window=(.*?)&'
            result = xpath_parser(html, regx1, fetch_one=True)
            image_url = re.search(regx2, html).group(1)
            if result:
                return result,image_url
            else:
                return False
        #法制网
        elif judge_url_contained('legaldaily',root_url):
            regx1 = '//video[@id="my_video_1"]/source/@src'
            result = xpath_parser(html, regx1, fetch_one=True)
            image_url = 'http://www.legaldaily.com.cn/templateRes/201611/10/33946/33946/images/2016-zy-002.gif'
            if result:
                return result,image_url
            else:
                return False
        #中华女性网(暂未发现)
        elif judge_url_contained('cnwomen',root_url):
            regx = 'application/x-shockwave-flash'
            result = re.search(regx, html)
            if result:
                return True
            else:
                return False
        #中国农业新闻网
        elif judge_url_contained('farmer',root_url):
            regx = '//div[@id="sp"]/script/@src'
            result = xpath_parser(html, regx)
            image_url = 'http://www.farmer.com.cn/images/%E4%B8%AD%E5%9B%BD%E5%86%9C%E4%B8%9A%E6%96%B0%E9%97%BB%E7%BD%91%E7%BA%A2%E8%89%B2LOGO.png'
            if result:
                return root_url,image_url
            else:
                return False
        #中国科技网
        elif judge_url_contained('stdaily',root_url):
            regx = '<p id="video" align="center"><script src=(.*?) type="text/javascript"></script></p>'
            result = re.search(regx, html, re.M|re.I).group(1)
            image_url = 'http://www.stdaily.com/index/xhtml/images/kjwsy_04.png'
            if result != '""':
                return root_url,image_url
            else:
                return False
        #海外网
        elif judge_url_contained('haiwainet',root_url):
            regx = r'showPlayer\(\{id:\"(.*?)\"'
            xml_info = re.search(regx, html).group(1)
            xml_url = 'http://pvmsxml.haiwainet.cn'+xml_info
            xml_content = requests.get(xml_url).text
            content = xmltodict.parse(xml_content)
            video = content["root"]["video"]["item"]
            img = content["root"]["image"]
            node = execjs.get()
            ctx = node.compile(js_info)
            result = ctx.call('getDecoderVideoForMP4', video, 3, True)
            image_url = ctx.call("getDecoderVideo", img, "true")
            if result:
                return result,image_url
            else:
                return False
        #中工网(网站迁移http://www.workercn.cn/)
        #视频少
        elif judge_url_contained('workercn',root_url):
            regx = 'IFRAME'
            result = re.search(regx, html)
            if result:
                return True
            else:
                return False
        #党建网
        elif judge_url_contained('dangjian',root_url):
            regx = 'new CloudVodPlayer()'
            result = re.search(regx, html)
            image_url = 'http://images.wenming.cn/web_djw/images/mylogo15072401.jpg'
            if result:
                return root_url,image_url
            else:
                return False
        #中国网
        elif judge_url_contained('china',root_url):
            regx = '//span[@id="videofile"]/@src'
            result = xpath_parser(html, regx, fetch_one=True)
            image_url = "http://images.china.cn/images1/ch/2017video/2017video/logo.jpg"
            if result:
                return result,image_url
            else:
                return False
        #中新网（中国新闻网）
        elif judge_url_contained('chinanews',root_url):
            regx = 'so.addVariable\("vInfo", "(.*?)"\);'
            result = re.search(regx, html).group(1)
            image_url = 'http://i8.chinanews.com/2016cns/video/2_03.jpg'
            if result:
                if "http://videoclips.chinanews" not in result:
                    result = "http://pb-fms.chinanews.com.cn/wsj/"+result
                return result,image_url
            else:
                return False
        #虎嗅网(视频暂未发现)
        elif judge_url_contained('huxiu',root_url):
            regx = 'article-content-video-box'
            result = re.search(regx, html)
            if result:
                return True
            else:
                return False
        # #Techweb（外链优酷视频）
        # elif judge_url_contained('techweb',root_url):
        #     regx = 'video_box'
        #     result = re.search(regx, html)
        #     if result:
        #         return True
        #     else:
        #         return False
        #中公教育(pass)
        elif judge_url_contained('offcn',root_url):
            regx = 'video-box'
            result = re.search(regx, html)
            if result:
                return True
            else:
                return False
        #未来网
        elif judge_url_contained('k618',root_url):
            regx1 = '//iframe/@src'
            regx2 = '//embed/@src'
            result = xpath_parser(html, regx1, fetch_one=True)
            if not result:
                result = xpath_parser(html, regx2, fetch_one=True)
            image_url = 'http://cdn.k618img.cn/vk618cn/images/ranlogo2.png'
            if result:
                return result,image_url
            else:
                return False
        #北京时间(新闻数据和视频都不在源码中)
        elif judge_url_contained('brtn',root_url):
            regx = 'video-box'
            result = re.search(regx, html)
            image_url = "http://p0.ssl.cdn.btime.com/t017e6fc57421faf298.png"
            if result:
                return root_url,image_url
            else:
                return False
        #驱动中国
        elif judge_url_contained('qudong',root_url):
            regx1 = '\[CoverURL\] \=\> (.*?).jpg'
            regx2 = '\[PlayURL\] \=\>(.*?).mp4'
            result = re.search(regx1, html, re.M).group(1)
            image_url = re.search(regx2, html, re.M).group(1)
            if result:
                result = result + ".jpg"
                image_url = image_url + ".mp4"
                return result,image_url
            else:
                return False
        #观察者
        elif judge_url_contained('guancha',root_url):
            regx = '//iframe[@name="videoiframe"]/@src'
            result = xpath_parser(html, regx, fetch_one=True)
            image_url = "https://www.guancha.cn/images/mian-logo.png"
            if result:
                return result,image_url
            else:
                return False
        #东海网
        elif judge_url_contained('dhtv',root_url):
            regx1 = 'vid:(.*?)//'
            regx2 = r"'img_url': '(.*?)',"
            vid = re.search(regx1, html, re.M).group(1)
            url = "http://v.dhtv.cn/api/?mod=video&vid={}".format(vid)
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36"
            }
            json_content = requests.get(url, headers=headers).json()
            result = json_content["video"]["source"]
            image_url = re.search(regx2, html).group(1)
            if result:
                return result,image_url
            else:
                return False
        #比特网(暂未找到视频)
        elif judge_url_contained('chinabyte',root_url):
            regx = 'allowfullscreen'
            result = re.search(regx, html)
            if result:
                return True
            else:
                return False
        #每经网(暂未找到视频)
        elif judge_url_contained('nbd',root_url):
            regx = 'vedioItem aliyunVideo'
            result = re.search(regx, html)
            if result:
                return True
            else:
                return False
        #中国文明网
        elif judge_url_contained('wenming',root_url):
            regx1 = '//video[@id="example_video_1"]/@poster'
            regx2 = '//video[@id="example_video_1"]/source/@src'
            image_url = xpath_parser(html, regx1, fetch_one=True)
            result = xpath_parser(html, regx2, fetch_one=True)
            if result:
                return result,image_url
            else:
                return False
        #凤凰网
        elif judge_url_contained('ifeng',root_url):
            regx1 = '"videoPlayUrl": "(.*?)"'
            regx2 = '"videoLargePoster": "(.*?)",'
            result = re.search(regx1, html).group(1)
            image_url= re.search(regx2, html).group(1)
            if result:
                return root_url,image_url
            else:
                return False
        #新浪
        elif judge_url_contained('sina',root_url):
            regx1 = "swfOutsideUrl:'(.*?)',"
            regx2 = "pic: '(.*?)',"
            result = re.search(regx1, html).group(1)
            image_url = re.search(regx2, html).group(1)
            if result:
                return root_url,image_url
            else:
                return False
        #搜狐
        elif judge_url_contained('sohu',root_url):
            regx1 = "showVrsPlayer(.*?)"
            result = re.search(regx1, html)
            image_url = "http://css.tv.itc.cn/global/images/nav1/logo.gif"

            if result:
                return root_url,image_url
            else:
                return False
        ###############分割线
        #网易网
        elif judge_url_contained('163',root_url):
            regx = 'video/mp4'
            result = re.search(regx, html)
            image_url = ""
            if result:
                return root_url,image_url
            else:
                return False
        #百度新闻
        elif judge_url_contained('baidu',root_url):
            regx = 'J_Article_Player'
            result = re.search(regx, html)
            image_url = "https://box.bdimg.com/static/fisp_static/common/img/searchbox/logo_news_276_88_1f9876a.png"
            if result:
                return root_url,
            else:
                return False
        #猫扑
        elif judge_url_contained('mop',root_url):
            regx = 'video/mp4'
            result = re.search(regx, html)
            image_url = "http://www.mop.com/images/LOGO.jpg"
            if result:
                return root_url,image_url
            else:
                return False
        #搜狐博客
        elif judge_url_contained('souhu',root_url):
            regx1 = 'isAutoPlay'
            regx2 = 'sohuplayer'
            result1 = re.search(regx1, html)
            result2 = re.search(regx2, html)
            image_url = "http://js3.pp.sohu.com.cn/cn2012/blog/images_v20120217/bloglogo.gif"
            if result1 or result2:
                return root_url,image_url
            else:
                return False
        #澎湃网
        elif judge_url_contained('thepaper',root_url):
            id = re.search('\d+',root_url).group()
            regx = '//video[@id="video{}"]/source/@src'.format(id)
            regx2 = '"poster": "(.*?)"'
            result = xpath_parser(html, regx , fetch_one=True)
            image_url = get_info(html, regx2, fetch_one=True)
            if result:
                image_url = "http:"+image_url
                return result,image_url
            else:
                return False
        #腾讯网
        elif judge_url_contained('qq',root_url):
            regx = 'videoPlayerWrap'
            result = re.search(regx, html)
            image_url = "http://mat1.gtimg.com/pingjs/ext2020/newom/build/static/images/logo.png"
            if result:
                return root_url,image_url
            else:
                return False
        #中国新闻出版广电网
        elif judge_url_contained("chinaxwcb",root_url):
            regx = 'f:"(.*?)",'
            result = get_info(html,regx, fetch_one=True)
            image_url = "https://www.chinaxwcb.com/template/1/default/_files/images/logo.jpg"
            if result:
                result = 'https://www.chinaxwcb.com' + result
                return result,image_url
            else:
                return False
        #国家广播电视总局
        elif judge_url_contained("nrta",root_url):
            regx = "f:'(.*?)',"
            result = get_info(html,regx, fetch_one=True)
            image_url = "http://www.nrta.gov.cn/picture/0/a801e9065cbc43ab8521be65419ea8fd.png"
            if result:
                result = 'http://www.nrta.gov.cn' + result
                return result,image_url
            else:
                return False
        #东方网
        elif judge_url_contained("eastday", root_url):
            regx = '//iframe[@name="flashimedia"]/@src'
            result = xpath_parser(html, regx, fetch_one=True)
            image_url = "http://ej.eastday.com/images/2013newlogo/title_video.jpg"
            if result:
                return result, image_url
            else:
                return False

        elif judge_url_contained("cm3721", root_url):
            regx = '//div[@class="video-main"]/iframe/@src'
            regx2 = '//div[@class="share-view"]/a[@class="jm_sina"]/@url'
            result = xpath_parser(html, regx, fetch_one=True)
            image_url = xpath_parser(html, regx2, fetch_one=True)
            if result:
                return result,image_url
            else:
                return False
        #上观网
        elif judge_url_contained("shobserver", root_url):
            regx = 'livingVideo'
            result  = get_info(html, regx)
            image_url = "https://www.jfdaily.com/livingVideo/getDetail?id=1121"
            if result:
                return root_url,image_url
            else:
                return False
        #新京报网
        elif judge_url_contained("bjnews", root_url):
            regx = 'flowplayer'
            result  = get_info(html, regx)
            image_url = "http://img.tbnimg.com/icon/bjnews_114.png"
            if result:
                return root_url,image_url
            else:
                return False
        else:
            return False

    except Exception:
        return False
if __name__ == '__main__':
    url = "http://travel.sina.com.cn/video/baidang/2018-06-30/detail-ihespqrx3921747.shtml"
    import requests
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36"
    }
    content = requests.get(url, headers=headers).text
    s = contain_video(url, content)
    print(s)