from twisted.internet import defer
from  twisted.web.client import getPage
from twisted.internet import reactor
def response(content):
    print(type(content))


@defer.inlineCallbacks
def task():
    url = 'http://www.people.com.cn/'
    d = getPage(url.encode('utf-8'))
    d.addCallbacks(response)
    yield d
    # url = 'https://coding.imooc.com/learn/questiondetail/8933.html'
    # d = getPage(url.encode('utf-8'))
    # d.addCallbacks(response)
    # yield d

t= []
for i in range(5):
    d =task()
    t.append(d)
a = defer.DeferredList(t)
a.addBoth(lambda a:reactor.stop())
reactor.run()