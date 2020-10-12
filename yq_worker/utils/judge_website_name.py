import re
from urllib import parse


def judge_url_contained(keyword,url):
    '''
    :param keyword: 域名
    :param url: 网站地址
    :return: 判断这个域名是否隶属于这个网站
    '''
    result = parse.urlparse(url)[1]
    try:
        domain=re.search(r"\.(.*)\.",result).group(1)
    except Exception as e:
        end=result.rfind(".")
        domain=result[:end]
    if "." in domain:
        str_list=domain.split(".")
        for domain in str_list:
            if keyword in domain:
                if len(keyword)==len(domain):
                    return True
                else:
                    return False
            else:
                continue
    else:
        if keyword in domain:
            if len(keyword)==len(domain):
                return True
            else:
                return False
        else:
            return False
def get_website_name(root_url):
    try:
        #央广网（中国广播网）
        if judge_url_contained('cnr',root_url):

            return '央广网'

        #中国网络电视台（CNTV）
        elif judge_url_contained('cctv',root_url):
            return '中国网络电视台'
        #国际在线
        elif judge_url_contained('cri',root_url):

            return '国际在线'
        #人民网
        elif judge_url_contained('people',root_url):

            return '人民网'
        #新华网
        elif judge_url_contained('xinhuanet',root_url):

            return '新华网'
        #求是网
        elif judge_url_contained('qstheory',root_url):
            return '求是网'
        #中国军网
        elif judge_url_contained('81',root_url):
            return '中国军网'
        #光明网
        elif judge_url_contained('gmw',root_url):
            return '光明网'
        #中国经济网
        elif judge_url_contained('ce',root_url):

            return '中国经济网'
        #中国日报网
        elif judge_url_contained('chinadaily',root_url):
            return '中国日报网'
        #人民政协网
        elif judge_url_contained('rmzxb',root_url):

            return '人民政协网'
        #环球网
        elif judge_url_contained('huanqiu',root_url):

            return '环球网'
        #中国青年网（暂未发现相关视频板块）
        elif judge_url_contained('youth',root_url):

            return '中国青年网'
        #中青在线
        elif judge_url_contained('cyol',root_url):

            return '中青在线'
        #法制网
        elif judge_url_contained('legaldaily',root_url):

            return '法制网'
        #中华女性网(暂未发现)
        elif judge_url_contained('cnwomen',root_url):

            return '中华女性网'
        #中国农业新闻网
        elif judge_url_contained('farmer',root_url):

            return '中国农业新闻网'
        #中国科技网
        elif judge_url_contained('stdaily',root_url):
            return '中国科技网'
        #海外网
        elif judge_url_contained('haiwainet',root_url):

            return '海外网'
        #中工网(网站迁移http://www.workercn.cn/)
        #视频少
        elif judge_url_contained('workercn',root_url):
            return '中工网'
        #党建网
        elif judge_url_contained('dangjian',root_url):
            return '党建网'
        #中华网
        elif judge_url_contained('china',root_url):

            return '中华网'
        #中新网（中国新闻网）
        elif judge_url_contained('chinanews',root_url):

            return '中国新闻网'
        #虎嗅网(视频暂未发现)
        elif judge_url_contained('huxiu',root_url):
            return '虎嗅网'
        # #Techweb（外链优酷视频）
        elif judge_url_contained('techweb',root_url):

            return 'Techweb'
        #中公教育(pass)
        elif judge_url_contained('offcn',root_url):
            return '中公教育'
        #未来网
        elif judge_url_contained('k618',root_url):

            return '未来网'
        #北京时间(新闻数据和视频都不在源码中)
        elif judge_url_contained('brtn',root_url):
            return '北京时间'
        #驱动中国
        elif judge_url_contained('qudong',root_url):
            return '驱动中国'
        #观察者
        elif judge_url_contained('guancha',root_url):
            return '观察者'
        #东海网
        elif judge_url_contained('dhtv',root_url):

            return '东海网'
        #比特网(暂未找到视频)
        elif judge_url_contained('chinabyte',root_url):
            return '比特网'
        #每经网(暂未找到视频)
        elif judge_url_contained('nbd',root_url):
            return '每经网'
        #中国文明网
        elif judge_url_contained('wenming',root_url):
            return '中国文明网'
        #凤凰网
        elif judge_url_contained('ifeng',root_url):

            return '凤凰网'
        #新浪
        elif judge_url_contained('sina',root_url):
                return '新浪网'
        #搜狐
        elif judge_url_contained('sohu',root_url):
            return '搜狐网'
        #网易网
        elif judge_url_contained('163',root_url):

            return '网易网'
        #百度新闻
        elif judge_url_contained('baidu',root_url):

            return '百度新闻'
        #猫扑
        elif judge_url_contained('mop',root_url):

            return '猫扑'
        #搜狐博客
        elif judge_url_contained('souhu',root_url):
            return '搜狐网'
        #澎湃网
        elif judge_url_contained('thepaper',root_url):

            return '澎湃网'
        #腾讯网
        elif judge_url_contained('qq',root_url):
            return '腾讯网'
        #中国新闻出版广电网
        elif judge_url_contained("chinaxwcb",root_url):

            return '中国新闻出版广电网'
        #国家广播电视总局
        elif judge_url_contained("nrta",root_url):

            return '国家广播电视总局'
        #东方网
        elif judge_url_contained("eastday", root_url):

            return '国家广播电视总局'

        elif judge_url_contained("cm3721", root_url):

            return ''
        #上观网
        elif judge_url_contained("jfdaily", root_url):

            return '上观网'
        #新京报网
        elif judge_url_contained("bjnews", root_url):

            return '新京报网'
        #天涯网
        elif judge_url_contained('tianya', root_url):
            return '天涯网'
        #电子商务研究中心
        elif judge_url_contained('100ec',root_url):
            return '电子商务研究中心'
        else:
            return ''
    except Exception:
        return ''
if __name__ == '__main__':
    url = 'http://www.100ec.cn/detail--6258283.html%20'
    name = get_website_name(url)
    print(name)