# *_*coding:utf-8 *_*
from yq_worker.extractor.fun_tools import *
from langid.langid import LanguageIdentifier, model
from html.parser import HTMLParser
#https://blog.csdn.net/weixin_35955795/article/details/52823203
'''tag是的html标签，attrs是 (属性，值)元组(tuple)的列表(list)'''
class Clean_Tag(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.html_list = []
        self.p_text = False
    def handle_starttag(self, tag, attr):
        if tag == 'p':
            self.p_text = True
    def handle_endtag(self, tag):
        if tag == 'p':
            self.p_text = False

    def handle_data(self, data):
        if self.p_text:
            self.html_list.append(data)

def is_chinese2(content):
    if content:
        identifier = LanguageIdentifier.from_modelstring(model, norm_probs=True)
        result = identifier.classify(content)
        language, score = result
        if language =='zh' and score > 0.7:
            return True
        else:
            return False
def is_chinese(content):
    c = Clean_Tag()
    c.feed(content)
    c.close()
    html_list = c.html_list
    score = 0
    if html_list:
        for str in html_list:
            result = is_have_chinese(str)
            if result:
                score = score + 1/len(html_list)
        if score > 0.6:
            return True
        else:
            return
    else:
        return
