import re
from  yq_worker.extractor.fun_tools import debug
import cchardet
import requests
from requests import utils
from bs4 import UnicodeDammit
from yq_worker.utils.url_filter import clean_url
from yq_worker.settings import USER_AGENTS
import random

headers = {
    "user-agent": random.choice(USER_AGENTS)
}
class UnicodeDetection(object):
    '''检测网页编码'''
    def __init__(self, url):

        self.__find_charset1 = re.compile(
            br'<meta.*?charset=["\']*(.+?)["\'>]', flags=re.I
        ).findall
        self.__find_charset = re.compile(
            br'<meta.*?charset=["\']*(.+?)["\'>]', flags=re.I
        ).findall
        self.__find_pragma = re.compile(
            br'<meta.*?content=["\']*;?charset=(.+?)["\'>]', flags=re.I
        ).findall

        self.__find_xml = re.compile(
            br'^<\?xml.*?encoding=["\']*(.+?)["\'>]'
        ).findall
        self._response = requests.get(url, timeout=3, headers=headers)
        self._encoding = ''
    @debug
    def __get_encodings_from_content(self, content):
        encodings = (self.__find_charset(content) + self.__find_pragma(content)
                     + self.__find_xml(content))
        encodings = [encoding.decode('utf8') for encoding in encodings]
        _encoding = encodings[0].lower()
        self._encoding = _encoding

    def __response_parser(self, encoding):
        try:
            return self._response.content, encoding

        except UnicodeError:
            pass

    @debug
    def __get_unicode_method1(self):
        dammit = UnicodeDammit(self._response.content, override_encodings=["utf-8", "gbk2312", "gbk"], is_html=True)
        self._encoding = dammit.original_encoding

    @debug
    def __get_unicode_method2(self):
        self._encoding = cchardet.detect(self._response.content)['encoding']

    @debug
    def __get_unicode_method3(self):
        self._encoding = utils.get_encoding_from_headers(self._response.headers)
    @debug
    def get_unicode_from_response(self):
        url = self._response.url
        result = clean_url(url)
        if not result:
            return '', ''

        self.__get_encodings_from_content(self._response.content)
        if not self._encoding:
            self.__get_unicode_method1()
        if not self._encoding:
            self.__get_unicode_method2()
        if not self._encoding:
            self.__get_unicode_method3()
        if self._encoding:
            return self.__response_parser(self._encoding)
        try:
            return str(self._response.content, encoding='ISO-8859-1', errors='replace'), 'ISO-8859-1'
        except TypeError:
            pass
if __name__ == '__main__':
    url = 'http://politics.people.com.cn/n1/2019/0808/c1001-31282188.html'
    u = UnicodeDetection(url)
    a,b = u.get_unicode_from_response()
    print(a,b)