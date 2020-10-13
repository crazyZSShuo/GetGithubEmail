# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html
import logging
import random

from scrapy import signals
from scrapy.core.downloader.handlers.http11 import TunnelError
from twisted.internet.error import TCPTimedOutError
from twisted.web._newclient import ResponseNeverReceived

from github.settings import COOKIE_POOL
from github.utils.login import login_get_cookies_requests

class GithubSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class GithubDownloaderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class GithubLoginMiddlerware(object):

    def __init__(self):
        self.cookie = {'logged_in': 'yes', '__Host-user_session_same_site': 'VgGdxNtJWVEt7Lp0Pb5DDITpQ4GqkrSBJF2NnDxRLbRUgKey', '_gh_sess': 'wR1YqgNB%2FEDzoJy%2F4DAouPmOIfox3YS6RKqSZ%2FH9thqtowLlI5j2eXy5SWbsU%2BTgt%2Fl6u2k4iBeL3A6BvPA%2FLDq6CotAZMNxom71pCX0zRe9uYkCV274G5KfS57ydBYeAzK8WDpx5tr0eNpz7gO2zZrFln83pwxIMMCMU5gf%2FQy%2FSdOzW7RBZH8W%2FbGtIMtrqilmVuxTuhJPv9aNbAJ5afQmzAMSYbt9S61Bi%2Fx4JWIVqL%2FNgaJoAXBo%2BnKTKJsMxxN1IuHMpu7u8u7N0TNJl1VWYXoC0W9yM%2BrqwgQmN89Gx5e2--h9nRnRwd3xuzt%2Fcx--Su1nIW%2FziGSsNwfSybWiCg%3D%3D', 'has_recent_activity': '1', 'user_session': 'VgGdxNtJWVEt7Lp0Pb5DDITpQ4GqkrSBJF2NnDxRLbRUgKey'}


    def process_request(self, request, spider):
        request.cookies = self.cookie

    def process_response(self, request, response, spider):
        if 'Sign in to view email' in response.text:
            self.cookie = login_get_cookies_requests()
            return request
        return response
      

    def process_exception(self, request, exception, spider):
        try:
            if isinstance(exception, TCPTimedOutError):
                return request
            if isinstance(exception, TimeoutError):
                return request
            if isinstance(exception, TunnelError):
                return request
            if isinstance(exception, ConnectionRefusedError):
                return request
        except Exception as e:
            logging.warning(f"未知错误.....{e}")
            pass



