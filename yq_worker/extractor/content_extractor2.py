# *_*coding:utf-8 *_*
# *_*coding:utf-8 *_*
import datetime
import re
from yq_worker.extractor.fun_tools import debug, debug_traceback
import lxml
import lxml.html
from lxml import etree
from lxml.html import HtmlComment
from yq_worker.extractor.config import DAY_TIME_REGEXS
from yq_worker.extractor.fun_tools import get_info, format_date
import logging
logger = logging.getLogger(__name__)
REGEXES = {
    'positiveRe': re.compile(
        ('article|arti|body|content|entry|hentry|main|page|'
         'artical|zoom|arti|context|message|editor|'
         'pagination|post|txt|text|blog|story'), re.I|re.M),
    'negativeRe': re.compile(
        ('copyright|combx|comment|com-|contact|foot|footer|footnote|decl|copy|'
         'notice|'
         'masthead|media|meta|outbrain|promo|related|scroll|link|pagebottom|bottom|'
         'other|shoutbox|sidebar|sponsor|shopping|tags|tool|widget'), re.I|re.M),
}

class ContentExtractorTwo():
    def __init__(self, html, with_tag=True, min_len=650, encode='utf-8'):
        self.non_content_tag = set([
            'head',
            'meta',
            'script',
            'style',
            'object', 'embed',
            'iframe',
            'marquee',
            'select',
        ])
        self.p_space = re.compile(r'\s')
        self.encoding = encode
        self.p_content_stop = re.compile(r'正文.*结束|正文下|相关阅读|声明')
        self.p_clean_tree = re.compile(r'author|post-add|copyright')
        self._release_time_box = []
        self._html = html
        self._with_tag = with_tag
        self._min_len = min_len
        self._max_weight = 5
        self._mix_weight = 1

    def calc_node_weight(self, node):
        weight = 1
        attr = '%s %s %s' % (
            node.get('class', ''),
            node.get('id', ''),
            node.get('style', '')
        )
        if attr:
            mm = REGEXES['negativeRe'].findall(attr)
            weight -= 2 * len(mm)
            mm = REGEXES['positiveRe'].findall(attr)
            weight += 4 * len(mm)
        if node.tag in ['div', 'p', 'table']:
            weight += 2
        return weight
    def verfy_datetime(self, release_time_str):
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
                return n_time
            else:
                return ""
        else:
            return ""
    @debug_traceback
    def get_main_block(self, html):
        ''' return (release_time, etree_of_main_content_block)
        '''
        # doc = lxml.html.fromstring(html)
        doc = etree.HTML(html)
        self.remove_noise_node(doc, noise_xpath_list=['//div[@class="comment-list"]', '//div[@id="footer"]'])
        body = doc.xpath('//body')
        if not body:
            return None
        candidates = []
        nodes = body[0].getchildren()

        while nodes:
            node = nodes.pop(0)
            children = node.getchildren()
            tlen = 0
            for child in children:
                if isinstance(child, HtmlComment):
                    continue
                if child.tag in self.non_content_tag:
                    continue
                if child.tag == 'a':
                    continue
                if child.tag == 'textarea':
                    # FIXME: this tag is only part of content?
                    continue
                text = child.text
                tail = child.tail
                # print(text)
                # print("\n")
                attr = '%s%s%s' % (child.get('class', ''),
                                   child.get('id', ''),
                                   child.get('style'))
                if 'display' in attr and 'none' in attr:
                    continue
                nodes.append(child)
                if child.tag == 'p':
                    weight = self._max_weight
                else:
                    weight = self._mix_weight
                text = '' if not child.text else child.text.strip()
                tail = '' if not child.tail else child.tail.strip()
                tlen += (len(text) + len(tail)) * weight
            if tlen < self._min_len:
                continue
            weight = self.calc_node_weight(node)
            candidates.append((node, tlen*weight))
        if not candidates:
            return None
        candidates.sort(key=lambda a: a[1], reverse=True)
        good = candidates[0][0]
        if good.tag in ['p', 'pre', 'code', 'blockquote']:
            for i in range(5):
                good = good.getparent()
                if good.tag == 'div':
                    break

        good = self.clean_node(good)
        return good
    def get_release_time(self):
        if self._release_time_box:
            # print(self._release_time_box)
            # self._release_time_box.sort(reverse=True)
            release_time = self._release_time_box[0]
        else:
            release_time =''
        return release_time
    def clean_node(self, tree):
        to_drop = []
        drop_left = False
        for node in tree.iterdescendants():
            if drop_left:
                to_drop.append(node)
                continue
            if isinstance(node, HtmlComment):
                to_drop.append(node)
                if self.p_content_stop.search(node.text):
                    drop_left = True
                continue
            if node.tag in self.non_content_tag:
                to_drop.append(node)
                continue
            attr = '%s %s' % (
                node.get('class', ''),
                node.get('id', '')
            )
            if self.p_clean_tree.search(attr):
                to_drop.append(node)
                continue
            aa = node.xpath('.//a')
            if aa:
                text_node = len(self.p_space.sub('', node.text_content()))
                text_aa = 0
                for a in aa:
                    alen = len(self.p_space.sub('', a.text_content()))
                    if alen > 5:
                        text_aa += alen
                if text_aa > text_node * 0.4:
                    to_drop.append(node)
        for node in to_drop:
            try:
                node.drop_tree()
            except:
                pass
        return tree

    def remove_noise_node(self, element, noise_xpath_list):
        if not noise_xpath_list:
            return
        for noise_xpath in noise_xpath_list:
            nodes = element.xpath(noise_xpath)
            for node in nodes:
                node.getparent().remove(node)
        return element
    def get_text(self, doc):
        lxml.etree.strip_elements(doc, 'script')
        lxml.etree.strip_elements(doc, 'style')
        for ch in doc.iterdescendants():
            if not isinstance(ch.tag, str):
                continue
            if ch.tag in ['div', 'h1', 'h2', 'h3', 'p', 'br', 'table', 'tr', 'dl']:
                if not ch.tail:
                    ch.tail = '\n'
                else:
                    ch.tail = '\n' + ch.tail.strip() + '\n'
            if ch.tag in ['th', 'td']:
                if not ch.text:
                    ch.text = '  '
                else:
                    ch.text += '  '
            # if ch.tail:
            #     ch.tail = ch.tail.strip()
        lines = doc.text_content().split('\n')
        content = []
        for l in lines:
            l = l.strip()
            if not l:
                continue
            content.append(l)
        return '\n'.join(content)
    def assess_result(self, node):
        '''
        噪音词汇库
        :param result:
        :return:
        '''
        try:
            a_num = len(node.xpath('.//a'))
            p_num = len(node.xpath('.//p'))
            tag_a_density = a_num / p_num
            # print(tag_a_density)
            if tag_a_density > 1:
                return
            else:
                return node
        except Exception as e:
            # print(e)
            pass
    def get_content(self):
        node = self.get_main_block(self._html)
        node = self.assess_result(node)
        if node is None:
            return ''
        if self._with_tag:
            # content = lxml.html.tostring(node, encoding=self.encoding).decode(self.encoding)
            content = lxml.html.tostring(node, encoding=self.encoding).decode(self.encoding)
        else:
            content = self.get_text(node)

        return content


