from .utils import pre_parse, remove_noise_node
from yq_worker.extractor.gne_extractor.extractor import ContentExtractor
import json

class GeneralNewsExtractor:
    '''
    Ti:节点 i 的字符串字数
    LTi：节点 i 的带链接的字符串字数
    TGi：节点 i 的标签数
    LTGi：节点 i 的带连接的标签数
    node：表示当前的节点元素
    density：相关密度
    sbdi： 文本中对应的符号的密度
    score：模型评估之后的分数
    '''
    def __init__(self):
        self.content_extractor = ContentExtractor()
        # self.title_extractor = TitleExtractor()
        # self.author_extractor = AuthorExtractor()
        # self.time_extractor = TimeExtractor()
        #噪音词汇库
        self.noise_keywords = ['服务电话', 'E-mail', '邮政编码', '官方电话']
    def assess_result(self, result):
        '''

        :param result:
        :return:
        '''
        try:
            node = result["node"]
            a_num = result["ltgi"]
            p_num = len(node.xpath('.//p'))
            tag_a_density = a_num / p_num
            # print(tag_a_density)
            if tag_a_density > 1:
                return ''
            else:
                content = result["text"]
                if len(content) < 200:
                    content = ""
                else:
                    for noise_kw in self.noise_keywords:
                        if noise_kw in content:
                            return
                    return content
        except Exception as e:
            # print(e)
            pass
    def extract(self, html, noise_node_list=None):
        element = pre_parse(html)
        remove_noise_node(element, noise_node_list)
        content = self.content_extractor.extract(element)
        content = content[0][1]
        # print(content)
        content = self.assess_result(content)
        content_wite_tag = "<p>" + content + "</p>"
        # title = self.title_extractor.extract(element)
        # publish_time = self.time_extractor.extractor(element)
        # author = self.author_extractor.extractor(element)
        return content_wite_tag
