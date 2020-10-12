# *_*coding:utf-8 *_*
import re
from html.parser import HTMLParser

from yq_worker.extractor.config import USEFUL_TAG
from yq_worker.extractor.html_clearner import html_cleaner2

from yq_worker.utils import tools


class ContentExtractorThree():
    def __init__(self, html):
        self._html = html
        self.filter_useless_tag()
        self._html = self.__del_html_tag(self._html)
        blocks = self._html.split('\n')
        self._paragraphs = [block for block in blocks if block.strip()]
        # print(self._paragraphs)
    def isNullOrWhiteSpace(self, content):
        return content or len(content) == 0
    @tools.debug
    def __replace_str(self, source_str, regex, replace_str = ''):
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
    def __del_html_tag(self, html, save_useful_tag = True):
        '''
        @summary:
        ---------
        @param html:
        @param save_useful_tag:保留有用的标签，如img和p标签
        ---------
        @result:
        '''
        if save_useful_tag:
            html = self.__replace_str(html, r'(?!{useful_tag})<(.|\n)+?>'.format(useful_tag = '|'.join(USEFUL_TAG)))
        else:
            html = self.__replace_str(html, '<(.|\n)*?>')
        html = self.__replace_str(html, '[\f\r\t\v]') # 将空格和换行符外的其他空白符去掉
        html = html.strip()
        return html
    def filter_useless_tag(self):
        self._html = html_cleaner2.clean_html(self._html)
    def get_main_content(self, _limitCount=500, _depth=5, _appendMode=False):
        """
        能够从过滤html标签后的文本中找到正文文本的起止行号，行号之间的文本就是网页正文部分。
        特性：正文部分的文本密度要高出非正文部分很多。
        :param content_list: 去除html标签后的文本，按行拆分为list
        :param _limitCount: 候选文本长度达到该值时，认为进入正文部分
        :param _depth: 每次分析几行数据
        :return: 正文内容
        """
        preTextLen = 0 # 上一次统计的字符数量
        startPos = -1 # 记录文章起始位置
        _headEmptyLines = 2
        _endLimitCharCount = 20
        content = []
        line = []
        for i in range(len(self._paragraphs) - _depth):
            length = 0
            for j in range(_depth):
                length += len(self._paragraphs[i + j])

            if startPos == -1:
                # 还没找到正文位置
                if (preTextLen > _limitCount) and (length > 0):
                    # 查找文章起始位置，发现两行连续为空认为是头部
                    emptyCount = 0
                    for j in range(i - 1, 0, -1):
                        if self.isNullOrWhiteSpace(self._paragraphs[j]):
                            emptyCount += 1
                        else:
                            emptyCount = 0
                        if emptyCount == _headEmptyLines:
                            startPos = j + _headEmptyLines
                            break
                    # 如果没有定位到正文开始，以当前位置为起始
                    if startPos == -1:
                        startPos = i
                    for j in range(startPos, i + 1):
                        # 将发现的正文放入list
                        content.append(self._paragraphs[j])
                        line.append(j)
            else:
                # 如当前长度、上一次长度都小于阈值，认为已经结束，若开启追加模式，则继续往后找
                if length <= _endLimitCharCount and preTextLen < _endLimitCharCount:
                    if not _appendMode:
                        break
                    startPos = -1
                line.append(i)
                content.append(self._paragraphs[i])
            preTextLen = length
        # 返回发现的正文内容
        # return '\n'.join(content), [min(line), max(line)] if len(line) > 0 else [0, 0]
        return '\n'.join(content) if len(line) > 0 else [0, 0]
if __name__ == '__main__':
    url = 'http://world.huanqiu.com/photo/2019-04/2927230.html'
    html, r = tools.get_html_by_requests(url)
    c3 = ContentExtractorThree(html)
    content = c3.get_main_content()
    print(content)