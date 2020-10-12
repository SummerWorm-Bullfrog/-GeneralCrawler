# *_*coding:utf-8 *_*
import urllib.parse as urlparse
g_bin_postfix = set(
                [
                    'exe', 'doc', 'docx', 'xls',
                    'ppt', 'pptx', 'pdf', 'xlsx',
                    'jpg', 'png', 'bmp', 'jpeg',
                    'zip', 'rar', 'tar', 'bz2',
                    '7z', 'gz', 'gif', 'mkv',
                    'flv', 'mp4', 'avi', 'wmv',
                    'apk', 'void(0)', '@', 'app',
                    'download', 'javascript', 'login', 'css',
                    'js', 'rar', 'exe', 'photo', 'search.php',
                    '404'
                ]
)

ignore_website = set(
    [
    'auto', 'esf', 'astro', 'house',
    'mail', 'baobao', 'caipiao', 'photo',
    'weather', 'ka.sina', 'book', 'pic,',
    'homelife', 'mail', 'v.qq', 'hongcai.163',
    'open.163', 'game', 'qzone.qq', 'mobile',
    'app','you.163', 'login', 'k.sina',
     'class.qq'




    ]
)
g_news_postfix = [
    '.html?', '.htm?', '.shtml?',
    '.shtm?',
]
def clean_url(url):
    # 是否为合法的http url
    if not url.startswith('http'):
        return ''
    #去除#后面的参数
    index = url.find('#')
    if index != -1:
        url = url[:index]
    # 去掉静态化url后面的参数
    for np in g_news_postfix:
        p = url.find(np)
        if p > -1:
            p = url.find('?')
            url = url[:p]
            return url
    # 3. 不下载二进制类内容的链接
    up = urlparse.urlparse(url)
    # print(up)
    path = up.path
    if not path:
        path = '/'
    # 以网站后缀判断网站的性质
    postfix1 = path.split('.')[-1].lower()
    if postfix1 in g_bin_postfix:
        return ''
    #以链接中path路径判断过滤
    postfix2 = path
    for  g_bin in g_bin_postfix:
        if g_bin in postfix2:
            return ''
    #过滤不关心的网站：
    netloc = up.netloc
    for ignore in ignore_website:
        if ignore in netloc:
            return ''
    good_queries = []
    for query in up.query.split('&'):
        qv = query.split('=')
        if qv[0].startswith('spm') or qv[0].startswith('utm_'):
            continue
        if len(qv) == 1:
            continue
        good_queries.append(query)
    query = '&'.join(good_queries)
    url = urlparse.urlunparse((
        up.scheme,
        up.netloc,
        path,
        up.params,
        query,
        ''  #  crawler do not care fragment
    ))
    return url
if __name__ == '__main__':
    url = clean_url('https://class.qq.com/class/30290.html')
    print(url)