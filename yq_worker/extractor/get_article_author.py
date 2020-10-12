# *_*coding:utf-8 *_*
from goose3 import Goose
from yq_worker.utils.code_detection import UnicodeDetection
from yq_worker.extractor.config import *
from yq_worker.extractor.fun_tools import get_info
from yq_worker.extractor.html_clearner import replace_str

class AuthorExtractor(object):
    def __init__(self, html):
        self._html = html
        self._auhtor = ''
        self._g  = Goose()
    def get_auhtor_method1(self):
        self._article = self._g.extract(raw_html=self._html)
        auhtors = self._article.authors
        if auhtors:
            self._auhtor = auhtors[0]
    def get_auhtor_method2(self):
        self._auhtor = get_info(self._html, AUTHOR_REGEXS_TEXT, fetch_one = True)
        if not self._auhtor: # 没有匹配到，去掉标签后进一步匹配，有的作者和名字中间有标签
            self._auhtor = get_info(replace_str(self._html, '<(.|\n)*?>', ' '), AUTHOR_REGEXS_TEXT, fetch_one = True)

        if not self._auhtor: # 仍没匹配到，则在html的author中匹配
            self._auhtor = get_info(self._html, AUTHOR_REGEX_TAG, fetch_one = True)

    def get_author(self):
        self.get_auhtor_method1()
        if not self._auhtor:
            self.get_auhtor_method2()
        return self._auhtor
if __name__ == '__main__':
    url = 'http://news.hsw.cn/system/2019/0708/1097939.shtml'
    text = UnicodeDetection(url).get_unicode_from_response()
    t = AuthorExtractor(text)
    print(t.get_author())
