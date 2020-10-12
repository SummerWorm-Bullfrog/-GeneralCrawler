# *_*coding:utf-8 *_*
import re
from lxml.html.clean import Cleaner
bad_attrs = ['width', 'height', 'style', '[-a-z]*color', 'background[-a-z]*', 'on*']
single_quoted = "'[^']+'"
double_quoted = '"[^"]+"'
non_space = '[^ "\'>]+'
def normalize_spaces(s):
    """去除多余的空格"""
    if not s:
        return ''
    return ' '.join(s.split())
def replace_str(source_str, regex, replace_str = ''):
    '''
    @summary: 替换字符串
    ---------
    @param source_str: 原字符串
    @param regex: 正则
    @param replace_str: 用什么来替换 默认为''
    ---------
    @result: 返回替换后的字符串
    '''
    str_info = re.compile(regex, re.M|re.S)
    return str_info.sub(replace_str, source_str)
def normalize_entities(cur_title):
    '''
    规范化一些符号显示
    :param cur_title:
    :return:
    '''
    entities = {
        u'\u2014':'-',
        u'\u2013':'-',
        u'&mdash;': '-',
        u'&ndash;': '-',
        u'\u00A0': ' ',
        u'\u00AB': '"',
        u'\u00BB': '"',
        u'&quot;': '"',
    }
    for c, r in entities.items():
        if c in cur_title:
            cur_title = cur_title.replace(c, r)
    return cur_title
def norm_title(title):
    return normalize_entities(normalize_spaces(title))
html_cleaner1 = Cleaner(scripts=True, javascript=True, comments=True,
                  style=True, links=True, meta=False, add_nofollow=False,
                  page_structure=False, processing_instructions=True, embedded=True,
                  frames=True, forms=True, annoying_tags=True, remove_tags=None,
                  remove_unknown_tags=None, safe_attrs_only=False,kill_tags=['a','td','tr','table'])
html_cleaner2 = Cleaner(scripts=True, javascript=True, comments=True,
                  style=True, links=True, meta=True, add_nofollow=False,
                  page_structure=False, processing_instructions=True, embedded=True,
                  frames=True, forms=True, annoying_tags=True, remove_tags=None,
                  remove_unknown_tags=None, safe_attrs_only=False,kill_tags=['a','td','tr','table','head','h1','h2','h3','h4','h5','ul','li'])