# *_*coding:utf-8 *_*

from yq_worker.extractor_article.article_extractor_base import BaseExtractor
from yq_worker.extractor.content_extractor1 import ContentExtractorOne
from yq_worker.extractor.content_extractor2 import ContentExtractorTwo
from yq_worker.utils.code_detection import UnicodeDetection
from yq_worker.utils.language_detection import is_chinese
from yq_worker.utils.tools import *
from yq_worker.extractor.fun_tools import *
from yq_worker.extractor.config import *
from yq_worker.extractor.gne_extractor import GeneralNewsExtractor
class ArticleExtractor(BaseExtractor):
    def __init__(self, url, html, encode):
        super(ArticleExtractor, self).__init__(url, html, encode)
        self._content = ''
        self._release_time = ''
        self.encoding = encode
        self._html = html
        self._url = url
        self.noise_node_list = ['//div[@class="comment-list"]', '//div[@id="footer"]']
        # self._c1 = ContentExtractorOne(self._html)
        self._c3 = GeneralNewsExtractor()
        self._c2 = ContentExtractorTwo(self._html, self.encoding)
    @debug
    def get_content(self):
        self._content = self._c2.get_content()
        if not self._content:
            self._content = self._c3.extract(self._html, noise_node_list=self.noise_node_list)
        if is_chinese(self._content):
            return self._content


    @debug
    def get_release_time(self):
        if not self._release_time:
            str= replace_str(self._html, '<!-- .* -->')
            release_time_str = get_info(str, DAY_TIME_REGEXS, fetch_one=True)
            self._release_time = verfy_datetime(release_time_str)
        if self._release_time == 'None':
            self._release_time = ''
        return self._release_time
if __name__ == '__main__':
    url = 'http://news.china.com.cn/txt/2019-07/25/content_75031282.htm'
    if url:
        s = UnicodeDetection(url)
        body, encode = s.get_unicode_from_response()
        html = body.decode('utf-8')
        ate = ArticleExtractor(url, html , encode)
        print(ate.get_title())
        print(ate.get_author())
        print(ate.get_release_time())
        print(ate.get_content())
