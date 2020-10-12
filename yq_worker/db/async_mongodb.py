# *_*coding:utf-8 *_*
from motor.motor_asyncio import AsyncIOMotorClient
from yq_worker.utils import tools
IP = tools.get_conf_value('config.conf', 'mongodb', 'ip')
PORT = int(tools.get_conf_value('config.conf', 'mongodb', 'port'))
DB = tools.get_conf_value('config.conf', 'mongodb', 'db')
'''https://motor.readthedocs.io/en/latest/tutorial-asyncio.html'''

class AsyncMongoDB():
    def __init__(self, ip = IP, port = PORT, db = DB):
        client = AsyncIOMotorClient(ip, port)
        self._db = client[db]['table']

    async def do_insert(self, document):
        '''
        插入单个文档
        :param document: key-value的字典
        :return:
        '''
        result = await self._db.insert_one(document)
        return result


    async def do_insert_many(self, documents):
        '''
        大量插入文档
        :param document: 列表里面包含key-value的字典
        :return: 
       '''
        result = await self._db.test_collection.insert_many(documents)

    async def do_find_one(self, condition):
        '''
        查询单个个文档
        :param condition: 得到匹配查询的第一个文档,插入的条件{'i': {'$lt': 1}}
        :return:{'_id': ObjectId('...'), 'i': 0}
        '''
        data = await self._db.test_collection.find_one(condition)

    async def do_find(self, condition):
        '''
        查询多个文档
        :param condition:
        :return:
        '''
        datas = []
        cursor = self._db.test_collection.find({'i': {'$lt': 5}}).sort('i')

        for data in await cursor.to_list(length=100):
            datas.append(data)

    # async def do_find():
    #循环中一次处理一个文档
    #     c = db.test_collection
    #     async for document in c.find({'i': {'$lt': 2}}):
    #     pprint.pprint(document)

    # async def do_find():
    #     cursor = db.test_collection.find({'i': {'$lt': 4}})
    #     # Modify the query before iterating
    #     cursor.sort('i', -1).skip(1).limit(2)
    #     async for document in cursor:
    #         ...
    #         pprint.pprint(document)
    async def do_replace(self, old_condition, new_condition):
        '''
        更改文档
        :param old_condition:
        :param new_condition:
        :return:
        '''
        old_document = await self._db.find_one(old_condition)
        _id = old_document['_id']
        result = await self._db.replace_one({'_id': _id}, new_condition)
        new_document = await self._db.find_one({'_id': _id})

    async def do_update(self, condition):
        '''
        update_one()只影响它找到的第一个文档
        :param condition:
        :return:
        '''
        result1 = await self._db.update_one({'i': 51}, {'$set': {'key': 'value'}})
        result2 = await self._db.update_many({'i': {'$gt': 100}},
                               {'$set': {'key': 'value'}})

    async def do_delete_many(self, condition):
        '''
        删除所有匹配的文档
        :param condition:
        :return:
        '''
        n = await self._db.count_documents({})
        result = await self._db.test_collection.delete_many({'i': {'$gte': 1000}})
        await self._db.count_documents({})
if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(do_count())