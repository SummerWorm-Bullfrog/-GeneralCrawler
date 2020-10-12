# *_*coding:utf-8 *_*
import datetime
import re
import time
import functools
import traceback
#程序错误追溯
import requests
from requests.adapters import HTTPAdapter
import logging
logger = logging.getLogger(__name__)
TIME_OUT = 30
def debug_traceback(func):
    def wrapper(*args, **kw):
        try:
            return func(*args, **kw)
        except Exception as err:
            traceback.print_exc()
    return wrapper
def debug(func):
    def wrapper(*args, **kw):
        try:
            return func(*args, **kw)
        except Exception as err:
            logger.info('ERROR：'+ str(err))
    return wrapper

# 装饰器：计算运行时间
def log_function_time(func):
    try:
        @functools.wraps(func)  # 将函数的原来属性付给新函数
        def calculate_time(*args, **kw):
            began_time = time.time()
            callfunc = func(*args, **kw)
            end_time = time.time()
            print(func.__name__ + " run time  = " + str(end_time - began_time))
            return callfunc

        return calculate_time
    except:
        print('求取时间无效 因为函数参数不符')
        return func


def run_safe_model(module_name):
    def inner_run_safe_model(func):
        try:
            @functools.wraps(func)  # 将函数的原来属性付给新函数
            def run_func(*args, **kw):
                callfunc = ''
                try:
                    callfunc = func(*args, **kw)
                except Exception as e:
                    print(module_name + ": " + func.__name__ + " - " + str(e))
                return callfunc

            return run_func
        except Exception as e:
            print(module_name + ": " + func.__name__ + " - " + str(e))
            return func

    return inner_run_safe_model
_regexs = {}
def get_info(html, regexs, allow_repeat=False, fetch_one=False, split=None):
    '''
    正则提取文本
    :param html: 待提取的字符串
    :param regexs: 提取规则
    :param allow_repeat: 是否允许重复
    :param fetch_one: 是否提取一个
    :param split:
    :return:
    '''
    if not html:
        return
    regexs = isinstance(regexs, str) and [regexs] or regexs
    infos = []
    for regex in regexs:
        if regex == '':
            continue

        if regex not in _regexs.keys():
            _regexs[regex] = re.compile(regex, re.S)

        if fetch_one:
            infos = _regexs[regex].search(html)
            if infos:
                infos = infos.groups()
            else:
                continue
        else:
            infos = _regexs[regex].findall(str(html))

        if len(infos) > 0:
            # print(regex)
            break

    if fetch_one:
        infos = infos if infos else ('',)
        return infos if len(infos) > 1 else infos[0]
    else:
        infos = allow_repeat and infos or sorted(set(infos), key=infos.index)
        infos = split.join(infos) if split else infos
        return infos
def format_date(date, old_format = '', new_format = '%Y-%m-%d %H:%M:%S'):
    '''
    @summary: 格式化日期格式
    ---------
    @param date: 日期 eg：2017年4月17日 3时27分12秒
    @param old_format: 原来的日期格式 如 '%Y年%m月%d日 %H时%M分%S秒'
        %y 两位数的年份表示（00-99）
        %Y 四位数的年份表示（000-9999）
        %m 月份（01-12）
        %d 月内中的一天（0-31）
        %H 24小时制小时数（0-23）
        %I 12小时制小时数（01-12）
        %M 分钟数（00-59）
        %S 秒（00-59）
    @param new_format: 输出的日期格式
    ---------
    @result: 格式化后的日期，类型为字符串 如2017-4-17 3:27:12
    '''

    if not old_format:
        regex = '(\d+)'
        numbers = get_info(date, regex, allow_repeat = True)
        formats = ['%Y', '%m', '%d', '%H', '%M', '%S']
        old_format = date
        for i, number in enumerate(numbers):
            if i == 0 and len(number) == 2: # 年份可能是两位 用小%y
                old_format = old_format.replace(number, formats[i].lower(), 1) # 替换一次 '2017年11月30日 11:49' 防止替换11月时，替换11小时
            else:
                old_format = old_format.replace(number, formats[i], 1)  # 替换一次

    try:
        date_obj = datetime.datetime.strptime(date, old_format)
        date_str = datetime.datetime.strftime(date_obj, new_format)
    except Exception as e:
        logger.debug('日期格式化出错，old_format = %s 不符合 %s 格式'%(old_format, date))
        date_str = date
    return date_str

def replace_str(source_str, regex, replace_str=''):
    '''
    @summary: 替换字符串
    ---------
    @param source_str: 原字符串
    @param regex: 正则
    @param replace_str: 用什么来替换 默认为''
    ---------
    @result: 返回替换后的字符串
    '''
    str_info = re.compile(regex)
    return str_info.sub(replace_str, source_str)
def del_html_tag(content, except_line_break=False, save_img=False):
    content = replace_str(content, '(?i)<script(.|\n)*?</script>')  # (?)忽略大小写
    content = replace_str(content, '(?i)<style(.|\n)*?</style>')
    content = replace_str(content, '<!--(.|\n)*?-->')
    content = replace_str(content, '(?!&[a-z]+=)&[a-z]+;?')  # 干掉&nbsp等无用的字符 但&xxx= 这种表示参数的除外
    if except_line_break:
        content = content.replace('</p>', '/p')
        content = replace_str(content, '<[^p].*?>')
        content = content.replace('/p', '</p>')
        content = replace_str(content, '[ \f\r\t\v]')

    elif save_img:
        content = replace_str(content, '(?!<img.+?>)<.+?>')  # 替换掉除图片外的其他标签
        content = replace_str(content, '(?! +)\s+', '\n')  # 保留空格
        content = content.strip()

    else:
        content = replace_str(content, '<(.|\n)*?>')
        content = replace_str(content, '\s')
        content = content.strip()

    return content


def del_html_js_css(content):
    content = replace_str(content, '(?i)<script(.|\n)*?</script>')  # (?)忽略大小写
    content = replace_str(content, '(?i)<style(.|\n)*?</style>')
    content = replace_str(content, '<!--(.|\n)*?-->')

    return content
@debug
def get_html_by_requests(url, headers='', code='utf-8', data=None, proxies={},max_retries=1):
    html = None
    if not url.endswith('.exe') and not url.endswith('.EXE'):
        r = None
        s = requests.Session()
        s.mount('http://', HTTPAdapter(max_retries=max_retries-1))
        s.mount('https://', HTTPAdapter(max_retries=max_retries-1))
        try:
            if data:
                r = s.post(url, headers=headers, timeout=TIME_OUT, data=data, proxies=proxies)
            else:
                r = s.get(url, headers=headers, timeout=TIME_OUT, proxies=proxies)

            if code:
                r.encoding = code
            html = r.text

        except Exception as e:
            logger.error(e)
        finally:
            r and r.close()

    return html and len(html) < 1024 * 1024 and html or None, r
def is_have_chinese(content):
    regex = '[\u4e00-\u9fa5]+'
    chinese_word = get_info(content, regex)
    return chinese_word and True or False

def get_chinese_word(content):
    regex = '[\u4e00-\u9fa5]+'
    chinese_word = get_info(content, regex)
    return chinese_word
@debug
def verfy_datetime(release_time_str):
    if release_time_str:
        release_time_str = format_date(release_time_str)
        #将字符串时间格式转换为datetime类型
        n_time = datetime.datetime.strptime(release_time_str, '%Y-%m-%d %H:%M:%S')
        # 范围时间
        d_time = datetime.datetime.strptime(str(datetime.datetime.now().date()) + ' 23:59:59', '%Y-%m-%d %H:%M:%S')
        # # 当前时间
        # d_time = datetime.datetime.now()
        # 判断当前时间是否在范围时间内
        if n_time < d_time:
            return str(n_time)

        else:
            return ""
    else:
        return ""
