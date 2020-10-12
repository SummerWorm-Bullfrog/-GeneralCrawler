import pymongo
from  yq_worker.utils.log import log
from yq_worker.utils import tools
IP = '192.168.80.70,192.168.80.71,192.168.80.72'
PORT = 2000
DB = 'news_info'


class Singleton(object):
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls,'_inst'):
            cls._inst=super(Singleton,cls).__new__(cls, *args, **kwargs)

        return cls._inst

class MongoDB(Singleton):
    def __init__(self, ip = IP, port = PORT, db = DB):
        super(MongoDB, self).__init__()

        if not hasattr(self,'_db'):
            try:
                with pymongo.MongoClient(ip, port) as client:
                    self._db = client[db]
            except Exception as e:
                raise
            else:
                log.debug('连接到数据库 %s'%db)


    def get_db(self):
        return self._db

    def find(self, table, condition = {}, limit = 0, sort = []):
        '''
        @summary: 查询
        ---------
        @param table: 表名
        @param condition: 条件 默认查询全部
        @param limit: 个数限制 默认查询全部
        @param sort: 排序 默认不排序
        ---------
        @result:
        '''

        result = []
        if sort:
            result = self._db[table].find(condition).limit(limit).sort(sort).batch_size(100)
        else:
            result = self._db[table].find(condition).limit(limit).batch_size(100)

        return list(result)


    def add(self, table, key_value):
        '''
        @summary: 添加 表不存在自动创建表
        ---------
        @param table: 表名
        @param key_value: 要添加的值 字典格式
        ---------
        @result: True / False
        '''

        try:
            self._db[table].save(key_value)
        except Exception as e:
            log.error(e)
            return False
        else:
            return True

    def update(self, table, old_value, new_value, multi = True):
        '''
        @summary: 更新
        ---------
        @param table: 表名
        @param old_value: 旧值
        @param new_value: 新值
        @param multi: 是否删除多个 默认是
        ---------
        @result:
        '''

        try:
            self._db[table].update(old_value, {'$set':new_value}, multi = multi)
        except Exception as e:
            log.error(e)
            return False
        else:
            return True

    def delete(self, table, condition={}):
        '''
        @summary: 删除数据
        ---------
        @param table: 表名
        @param condition: 删除条件 {}删除所有
        ---------
        @result:
        '''
        try:
            self._db[table].remove(condition)
        except Exception as e:
            log.error(e)
            return False
        else:
            return True
    def bulk_add(self, table, dict_list):
        try:
            self._db[table].insert_many(dict_list)
        except Exception as e:
            # log.error(e)
            return False
        else:
            return True
    def set_unique_key(self, table, key):
        try:
            self._db[table].ensure_index(key, unique=True)
        except:
            log.error("%s表中%s有重复的数据, 请先去重"%(table, key))

    def set_ensure_index(self, table, key):
        try:
            self._db[table].ensure_index(key, unique=False)
        except Exception as e:
            log.error(e)
if __name__ == '__main__':
    md = MongoDB()
    r = md.add('a',{"url":'231'})
    print(r)
