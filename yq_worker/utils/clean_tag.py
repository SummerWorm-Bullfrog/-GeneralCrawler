# *_*coding:utf-8 *_*
from html.parser import HTMLParser
#https://www.cnblogs.com/myyan/p/4846391.html
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
if __name__ == '__main__':
    content = ''
    c = Clean_Tag()
    c.feed(content)
    html_list = c.html_list