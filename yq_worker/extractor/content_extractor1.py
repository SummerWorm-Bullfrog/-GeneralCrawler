# *_*coding:utf-8 *_*
from yq_worker.utils.code_detection import UnicodeDetection
import re
import datetime
from yq_worker.extractor.config import *
import stopit
from yq_worker.extractor import fun_tools as tools
from yq_worker.extractor.html_clearner import html_cleaner1

class ContentExtractorOne():
    def __init__(self, html):
        self._html = html
        self._content_start_pos = ''
        self._content_end_pos = ''
        self._content_center_pos = ''
        self._paragraphs = ''
        self.filter_useless_tag()
        self._text = self.__del_html_tag(self._html, save_useful_tag = True)

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
    @tools.debug
    @stopit.threading_timeoutable()
    def __del_html_tag(self, html, save_useful_tag = False):
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
        self._html = html_cleaner1.clean_html(self._html)
    @tools.debug
    def __del_unnecessary_character(self, content):
        '''
        @summary: 去掉多余的换行和空格
        ---------
        @param content:
        ---------
        @result:
        '''
        content = content.strip()
        content = content[content.find('>') + 1 : ] if content.startswith('</') else content # 去掉开头的结束符
        content = self.__replace_str(content, ' {2,}', '') # 去掉超过一个的空格
        return self.__replace_str(content, '(?! )\s+', '\n') # 非空格的空白符转换为回车
    @tools.debug
    @stopit.threading_timeoutable()
    def get_content(self):
        '''
        @summary:
        基于文本密度查找正文
            1、将html去标签，将空格和换行符外的其他空白符去掉
            2、统计连续n段文字的长度，此处用于形容一定区域的文本密度
            3、将文本最密集处当成正文的开始和结束位置
            4、在正文开始处向上查找、找到文本密度小于等于正文文本密度阈值值，算为正文起始位置。该算法文本密度阈值值为文本密度值的最小值
            5、在正文开始处向下查找、找到文本密度小于等于正文文本密度阈值值，算为正文结束位置。该算法文本密度阈值值为文本密度值的最小值

        去除首页等干扰项：
            1、正文一般都包含p标签。此处统计p标签内的文字数占总正文文字数的比例。超过一定阈值，则算为正文
        待解决：
            翻页 如：http://mini.eastday.com/a/171205202028050-3.html
        ---------
        ---------
        @result:
        '''

        paragraphs = self._text.split('\n')
        # 统计连续n段的文本密度
        paragraph_lengths = [len(self.__del_html_tag(paragraph)) for paragraph in paragraphs]
        # paragraph_lengths = [len(paragraph.strip()) for paragraph in paragraphs]
        paragraph_block_lengths = [sum(paragraph_lengths[i : i + MAX_PARAGRAPH_DISTANCE]) for i in range(len(paragraph_lengths))]  # 连续n段段落长度的总和（段落块），如段落长度为[0,1,2,3,4] 则连续三段段落长度为[3,6,9,3,4]

        self._content_center_pos = content_start_pos = content_end_pos = paragraph_block_lengths.index(max(paragraph_block_lengths)) #文章的开始和结束位置默认在段落块文字最密集处
        min_paragraph_block_length = MIN_PARAGRAPH_LENGHT * MAX_PARAGRAPH_DISTANCE
        # 段落块长度大于最小段落块长度且数组没有越界，则看成在正文内。开始下标继续向上查找
        while content_start_pos > 0 and paragraph_block_lengths[content_start_pos] > min_paragraph_block_length:
            content_start_pos -= 1

        # 段落块长度大于最小段落块长度且数组没有越界，则看成在正文内。结束下标继续向下查找
        while content_end_pos < len(paragraph_block_lengths) and paragraph_block_lengths[content_end_pos] > min_paragraph_block_length:
            content_end_pos += 1
        # 处理多余的换行和空白符
        content = paragraphs[content_start_pos : content_end_pos]
        content = '\n'.join(content)
        content = self.__del_unnecessary_character(content)
        # 此处统计p标签内的文字数占总正文文字数的比例。超过一定阈值，则算为正文
        if content:
            paragraphs_text_len = len(self.__del_html_tag(''.join(tools.get_info(content, '<p.*?>(.*?)</p>'))))
            content_text_len = len(self.__del_html_tag(content))
            if content_text_len and content_text_len > MIN_COUNTENT_WORDS and ((paragraphs_text_len / content_text_len) > MIN_PARAGRAPH_AND_CONTENT_PROPORTION):
                self._content_start_pos = content_start_pos
                self._content_end_pos = content_end_pos
                self._paragraphs = paragraphs
                # print(content_start_pos, content_end_pos, self._content_center_pos)
                return content
            else:

                return ''

    # @tools.debug
    # def get_release_time(self):
    #     def get_release_time_in_paragraph(paragraph_pos):
    #         if self._paragraphs:
    #             while paragraph_pos >= 0:
    #                 content = self.__replace_str(self._paragraphs[paragraph_pos], '<(.|\n)*?>', '<>')
    #                 release_time = tools.get_info(content, DAY_TIME_REGEXS, fetch_one = True)
    #                 if release_time:
    #                     return tools.format_date(release_time)
    #                 paragraph_pos -= 1
    #
    #         return None
    #
    #     release_time = get_release_time_in_paragraph(self._content_start_pos)
    #     if not release_time:
    #         release_time = get_release_time_in_paragraph(self._content_center_pos)
    #     release_time = self.verfy_datetime(release_time)
    #     if not release_time:
    #         paragraphs = self._text.split('\n')
    #         paragraph_texts = [self.__del_html_tag(paragraph) for paragraph in paragraphs if paragraph]
    #         for text in paragraph_texts:
    #             if text:
    #                 release_str = tools.get_info(text, DAY_TIME_REGEXS, fetch_one = True)
    #                 release_time = self.verfy_datetime(release_str)
    #                 if release_time:
    #                     return release_time
    #     if not release_time:
    #         release_str = tools.get_info(self._html, DAY_TIME_REGEXS, fetch_one = True)
    #         release_time = self.verfy_datetime(release_str)
    #         if release_time:
    #             return release_time
    #     return release_time
    @tools.debug
    def verfy_datetime(self,release_time_str):
        if release_time_str:
            release_time_str = tools.format_date(release_time_str)
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
