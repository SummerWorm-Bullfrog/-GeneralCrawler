# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
# '''    article = {
#         'uuid' : uuid,
#         'title' : title,
#         'author' : author,
#         'release_time' : release_time,
#         'website' : website_name,
#         'domain' : website_domain,
#         'position' : website_position,
#         'url' : url,
#         'content' : content,
#         'record_time' : tools.get_current_date(),
#         'content_type': content_type,
#         'image_url': image_url
#     }
# '''
class YqWorkerItem(scrapy.Item):
    # define the fields for your item here like:
    site_id = scrapy.Field() #网站的唯一id
    uuid = scrapy.Field() #生成的唯一键title+url+domain
    title = scrapy.Field() #文章的标题
    author = scrapy.Field() #文章的作者
    release_time = scrapy.Field() #文章的发布时间
    website = scrapy.Field() #网站的名称
    domain = scrapy.Field() #网站的域名
    position = scrapy.Field() #网站的位置
    url = scrapy.Field() #网站的url
    content = scrapy.Field() #网页的内容
    record_time = scrapy.Field() #爬取改网站的记录时间
    content_type = scrapy.Field() #网站的类型，纯文章，包含视频俩类
    image_url = scrapy.Field() #内容中视频的封面链接
# YqWorkerItem.setdefault('uuid', "")
# YqWorkerItem.setdefault('title', "")
# YqWorkerItem.setdefault('author', "")
# YqWorkerItem.setdefault('release_time', "")
# YqWorkerItem.setdefault('url', "")
# YqWorkerItem.setdefault('uuid', "")
# YqWorkerItem.setdefault('content', "")