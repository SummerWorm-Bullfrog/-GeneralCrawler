# -*- coding: utf-8 -*-
from yq_worker.scrapy_redis.spiders import RedisSpider
from yq_worker.items import YqWorkerItem
from yq_worker.extractor_article.article_extractor import ArticleExtractor
from yq_worker.utils import tools
from yq_worker.video_judgment.content_judege import ContentJudege

class WorkerSpider(RedisSpider):
    name = 'worker'
    alllow_domain = ['*']
    def parse(self, response):
        root_url = response.url
        meta = response.meta
        encode = response.encoding
        website_name = meta["website_name"]
        # print(meta)
        site_id = meta["site_id"]
        website_domain = tools.get_domain(root_url)
        html = response.text
        item = YqWorkerItem()
        item.setdefault('uuid', "")
        item.setdefault('title', "")
        item.setdefault('author', "")
        item.setdefault('release_time', "")
        item.setdefault('url', "")
        item.setdefault('uuid', "")
        item.setdefault('content', "")
        website_position = 1
        content = title = release_time = author = ''
        article_extractor = ArticleExtractor(root_url, html, encode)
        content = article_extractor.get_content()
        c = ContentJudege(root_url, content)
        video_url = c.is_video()
        if content or video_url:
            title = article_extractor.get_title()
            release_time = article_extractor.get_release_time()
            author = article_extractor.get_author()
            # uuid = tools.get_uuid2(title, root_url, website_name) if title != website_name else tools.get_uuid2("",root_url,website_name)
            uuid = tools.get_uuid2(root_url)
            if video_url:
                content_type = "video"

            else:
                content_type = "text"
            item["site_id"] = site_id
            item["uuid"] = uuid
            item["title"] = title
            item["author"] = author
            item["release_time"] = release_time
            item["website"] = website_name
            item["domain"] = website_domain
            item["position"] = website_position
            item["url"] = root_url
            item["content"] = content
            item["content_type"] = content_type
            item["record_time"] =  tools.get_current_date()

        yield item


