import json
import redis
from yq_worker.db.elastic_search import ES
import threading
from yq_worker.utils import tools
SYNC_STEP = 50  # 一次同步的数据量
from yq_worker.db.mongodb import MongoDB
class SyncArtice(threading.Thread):
    def __init__(self):
        super(SyncArtice, self).__init__()
        self.r = redis.Redis(host='127.0.0.1',port=6379, db=2)
        self._es = ES()
        self._sync_count = 0
        self._mg_table = 'news_info'
        self._mongo = MongoDB()
    def get_data_from_redis(self, count = 10):
        datas = []
        while count:
            source, data = self.r.blpop(["worker:items"], timeout=5 * 60)
            if not data:
                count -= 1
                continue
            data = json.loads(data)
            datas.append(data)
            count-=1
        return datas
    def run(self):
        is_show_tip = False
        while True:
            try:
                datas = self.get_data_from_redis(SYNC_STEP)
                if not datas:
                    if not is_show_tip:
                        print('\n{time} 无数据 休眠...    '.format(time = tools.get_current_date()))
                        is_show_tip = True
                elif self.add_data_to_es(datas):
                    is_show_tip = False
                    self._sync_count += len(datas)
                    tools.print_one_line('已同步 %d 条数据'%self._sync_count)
                tools.delay_time(1)
            except Exception as e:
                print(e)

    def add_data_to_es(self, datas):
        return self._es.add_batch(datas, primary_key = 'uuid', table = 'news_article')
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
        # result = self._mongo.bulk_add(self._mongo, dict_list)
        result = self._mongo.add('news_info', article)
        if result:
            print('存入mongo')
if __name__ == '__main__':

    sync_article = SyncArtice()
    sync_article.start()

    # data = sync_article.get_data_from_redis(1)
    # print(data)

