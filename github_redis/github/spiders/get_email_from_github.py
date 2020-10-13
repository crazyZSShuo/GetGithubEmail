# -*- coding: utf-8 -*-
import logging
from urllib.parse import urljoin

import scrapy
import re
from github.utils.login import login_get_cookies_requests
import math
from scrapy.loader import ItemLoader
from github.items import EmailItem
from scrapy_redis.spiders import RedisSpider
import six

def bytes_to_str(s, encoding='utf-8'):
    """Returns a str if a bytes object is given."""
    if six.PY3 and isinstance(s, bytes):
        return s.decode(encoding)
    return s




class GithubSpider(RedisSpider):
    name = 'github'
    redis_key = 'github:start_urls'
    allowed_domains = ['github.com']
    cookies = {}
    total_star = None

    def next_requests(self):
        use_set = self.settings.getbool('REDIS_START_URLS_AS_SET', "False")
        fetch_one = self.server.spop if use_set else self.server.lpop
        # XXX: Do we need to use a timeout here?
        found = 0
        # TODO: Use redis pipeline execution.
        while found < self.redis_batch_size:
            data = fetch_one(self.redis_key)
            if not data:
                # Queue empty.
                break
            req = self.make_request_from_data(data)
            if req:
                yield req
                found += 1
            else:
                self.logger.debug("Request not made from data: %r", data)

        if found:
            self.logger.debug("Read %s requests from '%s'", found, self.redis_key)
    def make_request_from_data(self, data):
        url = bytes_to_str(data, self.redis_encoding)
        return self.make_requests_from_url(url)


    def make_requests_from_url(self, url):
        return scrapy.Request(url, dont_filter=True)


    def parse(self, response):
        # 使用requests完成登录
        self.cookies = login_get_cookies_requests()
        logging.info(f"获取Cookie：{self.cookies}")
        if not self.cookies:
            logging.error("获取Cookie失败，登录失败!!")
            raise RuntimeError("获取Cookie失败，登录失败!!")

        userprofile_urls = response.xpath("//div[@class='f6 text-gray mt-2']/a[1]/@href").getall()
        userprofile_urls = list(map(lambda x : urljoin(response.url,x),userprofile_urls))
        for path in userprofile_urls:
            yield scrapy.Request(path, callback=self.user_detail, cookies=self.cookies)

    # 获取用户详情
    def user_detail(self, response):
        count = response.xpath('//*[@id="repos"]/div[1]/nav/a[1]/span/text()').get()
        logging.info(f"用户收藏数:{count}")
        self.total_star = count
        get_follows_funs_urls = response.xpath("//ol[@class='follow-list clearfix']/li/div[2]/h3/span/a/@href")
        get_follows_funs_urls = list(map(lambda x: urljoin(response.url, x), get_follows_funs_urls.getall()))
        for user in get_follows_funs_urls:
            logging.warning(f"开始请求项目粉丝Url:{user}")
            yield scrapy.Request(user, callback=self.get_email, cookies=self.cookies)

        # 爬取下一页
        if response.xpath("//div[@class='paginate-container']/div[@class='BtnGroup']/a"):
            next_page = response.xpath("//div[@class='paginate-container']/div[@class='BtnGroup']/a/@href").getall()
            if len(next_page) == 1:
                next_page = next_page[0]
            else:
                next_page = [page for page in next_page if 'after' in page][0]
            logging.warning(f"获取下一页:{next_page}")
            yield scrapy.Request(next_page, callback=self.user_detail, cookies=self.cookies)


    # 获取用户邮箱
    def get_email(self, response):
        logging.warning("开始请求粉丝详情页，获取邮箱")
        loader = ItemLoader(item=EmailItem(), response=response)
        follower = following = star = location = twitter = mechanism = email = ''

        # 获取用户所有显示信息
        follows_and_star_data = response.xpath("//div[@class='flex-order-1 flex-md-order-none mt-2 mt-md-0']/div[@class='mb-3']")
        for data_info in follows_and_star_data:
            follower = data_info.xpath("./a[1]/span/text()")
            if follower:
                follower = follower.get()
            else:
                follower = '0'
            following = data_info.xpath("./a[2]/span/text()")
            if following:
                following = following.get()
            else:
                following = '0'
            star = data_info.xpath("./a[3]/span/text()")
            if star:
                star = star.get()
            else:
                star = '0'

        extra_info_datas = response.xpath("//ul[@class='vcard-details']")
        for extra_info in extra_info_datas:
            location = extra_info.xpath("./li[@itemprop='homeLocation']/span/text()")
            if location:
                location = location.get()
            else:
                location = ''

            twitter = extra_info.xpath("./li[@itemprop='twitter']/a/@href")
            if twitter:
                twitter = twitter.get()
            else:
                twitter = ''

            mechanism = extra_info.xpath("./li[@data-test-selector='profile-website-url']/a/@href")
            if mechanism:
                mechanism = mechanism.get()
            else:
                mechanism = ''

            # 获取用户邮箱
            email = response.xpath("//li[@itemprop='email']/a/text()")
            if email:
                email = email.get()
                logging.info(f"发现用户邮箱>>>{email}")
            else:
                email = ''
                logging.info(f"用户未公开邮箱>>>{email}")

        user = response.url.split('/')[-1]
        summery = response.xpath("//div[@class='p-note user-profile-bio mb-3 js-user-profile-bio f4']/div/text()")
        if summery:
            summery = summery.get()
        else:
            summery = ''

        highlights = response.xpath("//div[@class='border-top pt-3 mt-3 d-none d-md-block']/ul/li/a/@href")
        if not highlights:
            highlights = response.xpath("//div[@class='border-top pt-3 mt-3 d-none d-md-block']/ul/li/span/text()")
        if highlights:
            highlights = highlights.get()
        else:
            highlights = ''

        organizations = response.xpath("//div[@class='border-top pt-3 mt-3 clearfix hide-sm hide-md']/a/@href")
        if organizations:
            organizations = list(map(lambda x : urljoin(response.url, x), organizations.getall()))
            organizations = ','.join(organizations)
        else:
            organizations = ''

        programmingLanguage = response.xpath("//span[@class='d-inline-block mr-3']/span[@itemprop='programmingLanguage']/text()")
        if programmingLanguage:
            programmingLanguage = list(set(programmingLanguage.getall()))
            programmingLanguage = ','.join(programmingLanguage)
        else:
            programmingLanguage = ''

        # 判断个人页面是否有项目跟随者，如有，继续递归深度爬取
        try:
            is_star_project = response.xpath("//p[@class='mb-0 f6 text-gray']/a/@href")
            if is_star_project:
                logging.warning("个人详情页面又发现新的项目和粉丝")
                is_star_project = is_star_project.getall()
                for is_star_url in is_star_project:
                    if 'stargazers' in is_star_url:
                        next_star_project_link = urljoin(response.url, is_star_url)
                        logging.warning("开始新一轮递归深度爬取..")
                        yield scrapy.Request(next_star_project_link, dont_filter=False, callback=self.user_detail)
        except:
            pass

        loader.add_value('email', email)
        loader.add_value('url', response.url)
        loader.add_value('follower', follower)
        loader.add_value('following', following)
        loader.add_value('star', star)
        loader.add_value('location', location)
        loader.add_value('twitter', twitter)
        loader.add_value('mechanism', mechanism)
        loader.add_value('total_star', self.total_star)
        loader.add_value('user', user)
        loader.add_value('summery', summery)
        loader.add_value('highlights', highlights)
        loader.add_value('organizations', organizations)
        loader.add_value('programmingLanguage', programmingLanguage)

        logging.info(f"最终结果:{response.url}-{email}")
        yield loader.load_item()
