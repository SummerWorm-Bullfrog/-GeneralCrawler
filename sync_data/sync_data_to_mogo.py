# *_*coding:utf-8 *_*
import motor.motor_asyncio
import redis
import asyncio
from yq_worker.db.redisdb import RedisDB
from yq_worker.utils import tools
IP = '127.0.0.1'
PORT = 27017
DB = 'test'
TABLE = 'test_data'
'''
ObjectId =时间戳（4字节） + 机器标识码（3字节） + 进程ID（2字节） + 计数器（3字节）
'''
class SyncData():
    def __init__(self):
        self._redis = RedisDB()
        self._r = redis.Redis(host='192.168.80.43', port=6379, db=0)
        self._client = motor.motor_asyncio.AsyncIOMotorClient(IP, PORT)
        self._db = self._client[DB][TABLE]
        self._sync_count = 0
        self.loop = asyncio.get_event_loop()
    async def sync_data(self):
        is_show_tip = False
        while True:
            try:
                datas =  self.get_data_from_redis()
                if not datas:
                    if not is_show_tip:
                        print('\n{time} 无数据 休眠...    '.format(time=tools.get_current_date()))
                        is_show_tip = True

                else:
                    result = await self.do_insert_many(datas)
                    if result:
                        is_show_tip = False
                        self._sync_count += len(datas)
                        tools.print_one_line('已同步 %d 条数据' % self._sync_count)
                await asyncio.sleep(1)
            except Exception as e:
                print(e)
    async def add_one_to_mongo(self, document):
        '''
        插入单个文档
        :param document: key-value的字典
        :return:
        '''
        result = await self._db.insert_one(document)
        return result
    def get_data_from_redis(self, count=5):
        datas = self._redis.sget('news:news_article', count = count)
        return_datas = []
        for data in datas:
            data = eval(data)
            release_time = data.get('release_time')
            if release_time and len(release_time) == 19:
                return_datas.append(data)
        return return_datas
    async def do_insert_many(self, documents):
        '''
        大量插入文档
        :param document: 列表里面包含key-value的字典
        :return:
       '''
        result = await self._db.test_collection.insert_many(documents)
        return result
    def main(self):
        self.loop.run_until_complete(self.sync_data())

if __name__ == '__main__':
    sd = SyncData()
    sd.main()

