# *_*coding:utf-8 *_*
import re
import lxml
from yq_worker.utils.code_detection import UnicodeDetection
import requests
from lxml.html.clean import Cleaner
from yq_worker.extractor.config import *
from readability import Document #pip install readability-lxml
from goose3 import Goose
from goose3.text import StopWordsChinese
from yq_worker.extractor.fun_tools import get_info

class TitleExtractor(object):
    def __init__(self, html):
        self._html = html
        self._title = ''
        self._doc = Document(html)
    def clean_title(self, title):
        spliters = [' - ', '–', '—', '-', '|', '::']
        for s in spliters:
            if s not in title:
                continue
            tts = title.split(s)
            if len(tts) < 2:
                continue
            title = tts[0]
            break
        return title
    def get_title_method1(self):
        self._title = self._doc.short_title()
    def get_title_method2(self):
        # 处理特殊的网站不规则的标题
        if not self._title:
            regex = TITLE_RE
            self._title = get_info(self._html, regex, fetch_one=True)
    def get_title_method3(self):
        g = Goose()
        article = g.extract(raw_html=self._html)
        self._title = article.title
    def get_title_method4(self):
        doc = lxml.html.fromstring(self._html)
        title = ''
        title_el = doc.xpath('//title')
        if title_el:
            title = title_el[0].text_content().strip()
        if len(title) < 7:
            tt = doc.xpath('//meta[@name="title"]')
            if tt:
                title = tt[0].get('content', '')
        if len(title) < 7:
            tt = doc.xpath('//*[contains(@id, "title") or contains(@class, "title")]')
            if not tt:
                tt = doc.xpath('//*[contains(@id, "font01") or contains(@class, "font01")]')
            for t in tt:
                ti = t.text_content().strip()
                if ti in title and len(ti) * 2 > len(title):
                    title = ti
                    break
                if len(ti) > 20: continue
                if len(ti) > len(title) or len(ti) > 7:
                    title = ti
        self._title = title
    def get_title(self):
        self.get_title_method1()
        if not self._title:
            self.get_title_method2()
        if not self._title:
            self.get_title_method3()
        self._title = self.clean_title(self._title)
        return self._title



