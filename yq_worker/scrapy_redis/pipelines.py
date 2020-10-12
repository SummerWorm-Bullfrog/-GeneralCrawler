import datetime

from scrapy.utils.misc import load_object
from scrapy.utils.serialize import ScrapyJSONEncoder
from twisted.internet.threads import deferToThread
from yq_worker.db.mongodb import MongoDB
from scrapy.exceptions import DropItem

from yq_worker.utils import tools
from . import connection, defaults


default_serialize = ScrapyJSONEncoder().encode


class RedisPipeline(object):
    """Pushes serialized item into a redis list/queue

    Settings
    --------
    REDIS_ITEMS_KEY : str
        Redis key where to store items.
    REDIS_ITEMS_SERIALIZER : str
        Object path to serializer function.

    """

    def __init__(self, server,
                 key=defaults.PIPELINE_KEY,
                 serialize_func=default_serialize):
        """Initialize pipeline.

        Parameters
        ----------
        server : StrictRedis
            Redis client instance.
        key : str
            Redis key where to store items.
        serialize_func : callable
            Items serializer function.

        """
        self.server = server
        self.key = key
        self.serialize = serialize_func
        self._mongo = MongoDB()

    @classmethod
    def from_settings(cls, settings):
        params = {
            'server': connection.from_settings(settings),
        }
        if settings.get('REDIS_ITEMS_KEY'):
            params['key'] = settings['REDIS_ITEMS_KEY']
        if settings.get('REDIS_ITEMS_SERIALIZER'):
            params['serialize_func'] = load_object(
                settings['REDIS_ITEMS_SERIALIZER']
            )

        return cls(**params)

    @classmethod
    def from_crawler(cls, crawler):
        return cls.from_settings(crawler.settings)
    def add_data_to_mongo(self, item):
        if item["content_type"] == "video":
            video_url = 1
        else:
            video_url = 0
        article = {
            'site_id': item["site_id"],
            'title': item["title"],
            'author': item["author"],
            'release_time': item["release_time"],
            # 'website' : website_name,
            # 'domain' : website_domain,
            # 'position' : website_position,
            'url': item["url"],
            'content': item["content"],
            'record_time': tools.get_current_date(),
            'video_url': video_url,
            # 'image_url': item["image_url"]
        }
        result = self._mongo.add('news_info', article)
        if result:
            print('存入mongo')
    def process_item(self, item, spider):
        return deferToThread(self._process_item, item, spider)
    def _process_item(self, item, spider):
        try:
            if item["content_type"] == "video" and item["release_time"] and item["title"]:
                self.add_data_to_mongo(item)
                key = self.item_key(item, spider)
                data = self.serialize(item)
                self.server.rpush(key, data)
                return item
            elif all([item["release_time"],item["content"],item['title']]):
                self.add_data_to_mongo(item)
                key = self.item_key(item, spider)
                data = self.serialize(item)
                self.server.rpush(key, data)
                return item
            else:
                with open('urls.txt', "a+") as f:
                    f.write(item["url"])
                    f.write('\n')
                raise DropItem("data is none")
        except Exception as e:
            with open('urls.txt',"a+") as f:
                f.write(item["url"])
                f.write('\n')
            raise DropItem('item error!')


        

    def item_key(self, item, spider):
        """Returns redis key based on given spider.

        Override this function to use a different key depending on the item
        and/or spider.

        """
        return self.key % {'spider': spider.name}
