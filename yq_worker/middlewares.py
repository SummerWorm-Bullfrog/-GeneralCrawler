# -*- coding: utf-8 -*-
# Define here the models for your spider middleware
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html
import random
from collections import defaultdict
from urllib.parse import urlparse
from faker import Faker
# from fake_useragent import UserAgent
import logging
from scrapy.exceptions import NotConfigured
from scrapy.downloadermiddlewares.httpproxy import HttpProxyMiddleware
from scrapy.exceptions import IgnoreRequest
from scrapy.http import HtmlResponse
from twisted.internet import defer
from twisted.internet.error import *
from twisted.web.client import ResponseFailed
from scrapy.core.downloader.handlers.http11 import TunnelError
from requests_html import HTMLSession
import scrapy
from scrapy import signals
from yq_worker.utils.code_detection import UnicodeDetection
from yq_worker.utils.url_filter import clean_url
import websockets
import asyncio
import pyppeteer
from concurrent.futures._base import TimeoutError
from selenium import webdriver

logger = logging.getLogger(__name__)
'''
DOWNLOADER_MIDDLEWARES
下载中间件
下载中间件是scrapy提供用于用于在爬虫过程中可修改Request和Response，用于扩展scrapy的功能；比如：
    1.可以在请求被Download之前，请求头部加上某些信息；
    2.完成请求之后，回包需要解压等处理；
scrapy中间件中，处理request请求的函数，它的返回值有哪几种情况，分别有什么作用？

Retuen None: 将请求交给后续的中间件进行处理；

Return Request: 将请求交给调度器重新调度，并终止后续中间件的执行；

Return Response: 终止后续中间件及下载器的执行，直接将Response交给引擎。

Return Except: 抛出异常
________________________________________________________________________

scrapy中间件中，处理response响应的函数，它的返回值有哪几种情况，分别有什么作用？

Return Request: 终止后续中间件的执行，将请求重新交给调度器进行调度。

Return Response: 继续执行后续的中间件。

Return Except: 抛出异常。
'''
class RandomUserAgentMiddleware(object):
    @classmethod
    # @classmethod表示该方法输入该类，可以直接由类名调用，不必通过对象调用
    # 即Spider.from_crawler(crawler)即可调用该函数。在Crawler类中，Crawler通过
    # 传入一个Spider类作为参数初始化该Crawler，这个Spider类直接调用该from_crawler()
    # 函数从而实现Spider的初始化
    def from_crawler(cls, crawler):
        return cls(crawler)
    def __init__(self, crawler):
        # self.user_agent1 = UserAgent().random
        self.user_agent2 = crawler.settings.get('USER_AGENTS', False)
        self.proxy = {}
    def process_request(self, request, spider):
        user_agent = random.choice(self.user_agent2)
        request.headers['User-Agent'] = user_agent
    # def process_response(self, request, response, spider):

    def process_exception(self, request, exception, spider):
        # 处理错误
        pass

class ProcessAllExceptionMiddleware(object):
    ALL_EXCEPTIONS = (defer.TimeoutError, TimeoutError, DNSLookupError,
                      ConnectionRefusedError, ConnectionDone, ConnectError,
                      ConnectionLost, TCPTimedOutError, ResponseFailed, InvalidAddressError,
                      IOError, TunnelError)

    def process_response(self, request, response, spider):
        # 捕获状态码为40x/50x的response
        if str(response.status).startswith('4') or str(response.status).startswith('5'):
            # 随意封装，直接返回response，spider代码中根据url==''来处理response
            # response = HtmlResponse(url='')
            raise HttpError('Ignoring Error')
        # 其他状态码不处理
        return response

    def process_exception(self, request, exception, spider):
        # 捕获几乎所有的异常
        if isinstance(exception, self.ALL_EXCEPTIONS):
            # 在日志中打印异常类型
            logger.info('Got exception: %s' % (exception))
            # 随意封装一个response，返回给spider
            # response = HtmlResponse(url='')
            raise HttpError('Ignoring Error')
        # 打印出未捕获到的异常
        logger.info('not contained exception: %s' % exception)


class HttpError(IgnoreRequest):
    """A non-200 response was filtered"""

    def __init__(self, response, *args, **kwargs):
        self.response = response
        super(HttpError, self).__init__(*args, **kwargs)


class HttpErrorMiddleware(object):

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings)

    def __init__(self, settings):
        self.handle_httpstatus_all = settings.getbool('HTTPERROR_ALLOW_ALL')
        self.handle_httpstatus_list = settings.getlist('HTTPERROR_ALLOWED_CODES')

    def process_spider_input(self, response, spider):
        if 200 <= response.status < 300:  # common case
            return
        meta = response.meta
        if 'handle_httpstatus_all' in meta:
            return
        if 'handle_httpstatus_list' in meta:
            allowed_statuses = meta['handle_httpstatus_list']
        elif self.handle_httpstatus_all:
            return
        else:
            allowed_statuses = getattr(spider, 'handle_httpstatus_list', self.handle_httpstatus_list)
        if response.status in allowed_statuses:
            raise HttpError(response, 'Ignoring non-200 response')
        raise HttpError(response, 'Ignoring non-200 response')

    def process_spider_exception(self, response, exception, spider):
        if isinstance(exception, HttpError):
            spider.crawler.stats.inc_value('httperror/response_ignored_count')
            spider.crawler.stats.inc_value(
                'httperror/response_ignored_status_count/%s' % response.status
            )
            logger.info(
                "Ignoring response %(response)r: HTTP status code is not handled or not allowed",
                {'response': response}, extra={'spider': spider},
            )
            return []

# class RenderMiddleware(object):
#     def __init__(self):
#         self.session = HTMLSession()
#
#     def process_request(self, request, spider):
#         if spider.name == 'worker':
#             s = self.session.get(request.url)
#             body = s.html.html
#             url = s.url
#             return HtmlResponse(url,
#                                 body=body,
#                                 encoding='utf-8',
#                                 request=request)
class DealIrregularLink(object):
    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings)
    def __init__(self, settings):
        self._url = ''
        self.IGONRE_URL = settings.getlist("IGONRE_URL")
    def process_request(self, request, spider):
            if spider.name == 'worker':
                self._url = request.url
                for ignore_url in self.IGONRE_URL:
                    if self._url.endswith(ignore_url):
                        self._url = ''
                    else:
                        self._url = clean_url(self._url)
                if self._url:
                    s = UnicodeDetection(self._url)
                    body, encode = s.get_unicode_from_response()
                    if encode:
                        return HtmlResponse(self._url,
                                            body=body,
                                            encoding=encode,
                                            request=request)
                    else:
                        return
                else:
                    raise IgnoreRequest

class RandomHttpProxyMiddleware(HttpProxyMiddleware):

    def __init__(self, auth_encoding='latin-1', proxy_list = None):
        if not proxy_list:
            raise NotConfigured
        self.proxies = defaultdict(list)
        for proxy in proxy_list:
            parse = urlparse(proxy)
            self.proxies[parse.scheme].append(proxy)        #生成dict，键为协议，值为代理ip列表

    @classmethod
    def from_crawler(cls, crawler):
        if not crawler.settings.get('HTTP_PROXY_LIST'):
            raise NotConfigured

        http_proxy_list = crawler.settings.get('HTTP_PROXY_LIST')   #从配置文件中读取
        auth_encoding = crawler.settings.get('HTTPPROXY_AUTH_ENCODING', 'latin-1')

        return cls(auth_encoding, http_proxy_list)

    def _set_proxy(self, request, scheme):
        proxy = random.choice(self.proxies[scheme])     #随机抽取选中协议的IP
        request.meta['proxy'] = proxy

class RandomUserAgentMiddleware(object):

    def __init__(self):
        self.faker = Faker(local='zh_CN')
        self.user_agent = ''

    @classmethod
    def from_crawler(cls, crawler):
        o = cls()
        crawler.signals.connect(o.spider_opened, signal=signals.spider_opened)
        return o

    def spider_opened(self, spider):
        self.user_agent = getattr(spider, 'user_agent',self.user_agent)

    def process_request(self, request, spider):
        self.user_agent = self.faker.user_agent()    #获得随机user_agent
        request.headers.setdefault(b'User-Agent', self.user_agent)

class PyppeteerMiddleware(object):
    def __init__(self, **args):
        """
        init logger, loop, browser
        :param args:
        """
        self.loop = asyncio.get_event_loop()
        self.browser = self.loop.run_until_complete(
            pyppeteer.launch(headless=True))
        self.args = args

    def __del__(self):
        """
        close loop
        :return:
        """
        self.loop.close()

    def render(self, url, retries=1, script=None, wait=0.3, scrolldown=False, sleep=0,
               timeout=8.0, keep_page=False):
        """
        render page with pyppeteer
        :param url: page url
        :param retries: max retry times
        :param script: js script to evaluate
        :param wait: number of seconds to wait before loading the page, preventing timeouts
        :param scrolldown: how many times to page down
        :param sleep: how many long to sleep after initial render
        :param timeout: the longest wait time, otherwise raise timeout error
        :param keep_page: keep page not to be closed, browser object needed
        :param browser: pyppetter browser object
        :param with_result: return with js evaluation result
        :return: content, [result]
        """

        # define async render
        async def async_render(url, script, scrolldown, sleep, wait, timeout, keep_page):
            try:
                # basic render
                page = await self.browser.newPage()
                await asyncio.sleep(wait)
                response = await page.goto(url, options={'timeout': int(timeout * 1000)})
                if response.status != 200:
                    return None, None, response.status
                result = None
                # evaluate with script
                if script:
                    result = await page.evaluate(script)

                # scroll down for {scrolldown} times
                if scrolldown:
                    for _ in range(scrolldown):
                        await page._keyboard.down('PageDown')
                        await asyncio.sleep(sleep)
                else:
                    await asyncio.sleep(sleep)
                if scrolldown:
                    await page._keyboard.up('PageDown')

                # get html of page
                content = await page.content()

                return content, result, response.status
            except TimeoutError:
                return None, None, 500
            finally:
                # if keep page, do not close it
                if not keep_page:
                    await page.close()

        content, result, status = [None] * 3

        # retry for {retries} times
        for i in range(retries):
            if not content:
                content, result, status = self.loop.run_until_complete(
                    async_render(url=url, script=script, sleep=sleep, wait=wait,
                                 scrolldown=scrolldown, timeout=timeout, keep_page=keep_page))
            else:
                break

        # if need to return js evaluation result
        return content, result, status

    def process_request(self, request, spider):
        """
        :param request: request object
        :param spider: spider object
        :return: HtmlResponse
        """
        if request.meta.get('render'):
            try:
                logger.debug('rendering %s', request.url)
                html, result, status = self.render(request.url)
                s = UnicodeDetection(request.url)
                body, encode = s.get_unicode_from_response()
                if encode:
                    return HtmlResponse(url=request.url, body=html, request=request, encoding=encode,
                                        status=status)
                else:
                    raise IgnoreRequest
            except websockets.exceptions.ConnectionClosed:
                pass

    @classmethod
    def from_crawler(cls, crawler):
        return cls(**crawler.settings.get('PYPPETEER_ARGS', {}))


class SeleniumChromeMiddleware(object):
    def __init__(self):
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        self.browser = webdriver.Chrome(options=options)

    def process_request(self, request, spider):
        """
        :param request: request object
        :param spider: spider object
        :return: HtmlResponse
        """
        url = request.url
        self.browser.get(url)
        html = self.browser.page_source
        s = UnicodeDetection(request.url)
        body, encode = s.get_unicode_from_response()
        if encode:
            return HtmlResponse(url=request.url, body=html.encode("utf-8"), request=request, encoding=encode)
        else:
            raise IgnoreRequest

    def __del__(self):
        """
        close loop
        :return:
        """
        self.browser.quit()
