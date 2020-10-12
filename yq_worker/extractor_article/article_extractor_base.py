# *_*coding:utf-8 *_*
from yq_worker.extractor.get_article_author import AuthorExtractor
from yq_worker.extractor.get_article_title import TitleExtractor
from yq_worker.extractor.fun_tools import *
from yq_worker.utils.tools import is_have_chinese


class BaseExtractor(object):
    def __init__(self, url , raw_hml, encode):
        self._raw_hml = raw_hml
        self._title = ''
        self._author = ''
    @debug
    def get_title(self):
        t  = TitleExtractor(self._raw_hml)
        self._title = t.get_title()
        if is_have_chinese(self._title):
            return self._title
    def get_content(self):
        pass
    @debug
    def get_author(self):
        a = AuthorExtractor(self._raw_hml)
        self._author = a.get_author()
        return self._author
    def get_release_time(self):
        pass