import re
import requests
from lxml import etree
from urllib.parse import urljoin
import logging

from concurrent.futures import ThreadPoolExecutor

'''
Function:
	GitHub模拟登录
'''

session = requests.Session()



class github():
    def __init__(self, **kwargs):
        self.info = 'github'
        # self.session = session

    '''登录函数'''

    def login(self, username, password, **kwargs):
        # 设置代理
        logging.info("开始登陆....")
        print("开始登陆....")
        session.proxies.update(kwargs.get('proxies', {}))
        logging.info("初始化操作...")
        print("初始化操作...")
        self.__initializePC()
        token = self.__getToken()
        logging.info("获取登录认证Token...")
        print("获取登录认证Token...")
        logging.info(f"获取登录认证Token成功:{token}")
        print(f"获取登录认证Token成功:{token}")
        data = {
            'commit': 'Sign in',
            'utf8': '✓',
            'authenticity_token': token,
            'login': username,
            'password': password
        }
        res = session.post(self.post_url, headers=self.login_headers, data=data)
        if res.status_code == 200 and 'Sign in to GitHub · GitHub' not in res.text:
            print('[INFO]: 登录成功 -> %s, login successfully...' % username)
            # logging.info('[INFO]: 登录成功 -> %s, login successfully...' % username)
            userprofile_urls = self.get_somebody_links()[13:14]
            for user in userprofile_urls:
                print(f"Get:{user}")
                get_follows_funs_urls = self.get_userprofile_follows_funs(user)
                for follows_funs_urls in get_follows_funs_urls:
                    with ThreadPoolExecutor(max_workers=20) as pool:
                        data = pool.map(self.get_userprofile_follows_funs_email, follows_funs_urls)
                        for i in data:
                            print(i)

                # for follows_funs_urls in [funs_urls for follows_funs_urls in get_follows_funs_urls
                #                           for funs_urls in follows_funs_urls]:
                #     print("follows_funs_urls:",follows_funs_urls)
                #     data = self.get_userprofile_follows_funs_email(follows_funs_urls)
                #     logging.info(f"开发者信息：{data}")
                #     print(data)
            # infos_return = {'username': username}
            # return infos_return, self.session
        else:
            raise RuntimeError('登录失败 -> %s, fail to login, username or password error...' % username)


    '''获取authenticity_token参数'''

    def __getToken(self):
        res = session.get(self.login_url)
        token = re.findall(r'authenticity_token.*?value="(.*?)"', res.text)[0]
        return token

    '''初始化PC端'''

    def __initializePC(self):

        self.login_headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            'Content-Length': '196',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Host': 'github.com',
            'Origin': 'https://github.com',
            'Pragma': 'no-cache',
            'Referer': 'https://github.com/login',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36'
        }
        self.somebody_headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36'
        }
        self.get_email_headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Cookie':'_octo=GH1.1.1925059196.1592892678; _ga=GA1.2.488305389.1592892684; tz=Asia%2FShanghai; _device_id=e8b98f21406a32631c03ad0b5f43c995; _gat=1; has_recent_activity=1; user_session=pJ2n_FcEdU6kFJ_v54nFPGZKeH4nLWhE9le4KRKZTe_OEURX; __Host-user_session_same_site=pJ2n_FcEdU6kFJ_v54nFPGZKeH4nLWhE9le4KRKZTe_OEURX; logged_in=yes; dotcom_user=hellozs1024; _gh_sess=onHuxPu2Lk5S0LDqcToUAmK8TfePdW%2BxFzo01NFljh27ToOUd3n4MG4O70g0ircHjwBe8s0cQWGgUeOl05kFmIpZVopJV8DXy2vPZ%2BImUL4L9MpnnJq00wBUqfPFVM11NjssME%2FV2ladYbj%2BzFz3tLmtZTeryUCkE5xVIXvZ0MbpLD4uhfcPXtdx8JWFGI6ozFmEm%2BOnnbmZ8yNAgj%2FBi1orpIk75aqHvcxkOGUjV7bZoqTJ920W0csTsFBtttvXxvdhEjPcUTBV%2Fec40gQBr%2Fk3OhPLovw5P191pssYybUWJAwXC3qF35lYTWO99qzqcuiTpAsv%2Ff4xCSwhoT%2B%2FxTzu5T73fjiIlnKyiLVz45MU2fwm7dJSee9%2FyGp2czKH2UL1SoL8kaGWi%2BPIseeEw%2FEVae3GjrPogMQmuKta1LLoRhk1IvPuYG8HBFv%2B7D%2FJHFxwoRoXr9DgrcR5%2BHlQw3PWULcKTEWItANIn0GeGK81duqPflUFaX37ZBc3aDS2ia8KgfTJAn2vtEeiS3Jt8ktjKKcpDOi1hYzrPXlKTaqhNYQGhQr5nCmv54c7qs%2BQcbe6x1cs9pJj%2BWxU%2FiGlseZNUKAZ3X3IbwOWcyBn0OT4MSFR1%2FrmbCJm76B0Ru35oLddGtAmWZz6arrm2xnWHKjdtD8uUNxNor7YFJUvK6m3T7j5pKXi1GhuZVU14mKNva9Bth24jMmc0MbJXWupg2CRIUfv8%2BHKaQd437w84dzsZMymoPObW5jTsagJ%2FNBKB64ILB%2B5h0RXqm0Adn%2BxBjKRh0fcvqa12Xu9UfrWA10UJg1F1K%2BsTa%2B1%2F%2BcwCghCk1nN6h0cVQqFd5JqyHzBy24YNsvg%2BeB5huDXYzJ%2BocMi%2FO9G9ynU%2FizgeJTfn%2FpOvK0mpjp0D85Ln61w%2BR5EdRJwuwSYS4NewculLZIlj6Y2%2BRIBJkLUS7lHJ93sHh%2BggiQ2IPTDJsKDvGVbIAoV%2FPau1nvTOFHbc%2FhJ964jY8k%3D--%2FZYySvmIUSlFtu7f--D15%2FukDh7is8IKpiY21GZQ%3D%3D',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36'
        }
        self.login_url = 'https://github.com/login'
        self.post_url = 'https://github.com/session'
        # self.somebody_url = "https://github.com/trending?since=monthly"
        self.somebody_url = "https://github.com/trending?since=daily"


    # 获取近一个月内开发项目热度最高的拥有粉丝者链接
    def get_somebody_links(self):
        logging.info("获取近一个月内开发项目热度最高的拥有粉丝者链接")
        resp = session.get(self.somebody_url, headers=self.somebody_headers)
        html = etree.HTML(resp.text)
        userprofile_urls = html.xpath("//div[@class='f6 text-gray mt-2']/a[1]/@href")
        userprofile_urls = list(map(lambda x : urljoin(resp.url,x),userprofile_urls))
        return userprofile_urls

    # 获取首页各位开发者大神的追随者们
    def get_userprofile_follows_funs(self, userprofile):
        logging.info("获取首页各位开发者大神的追随者们")
        print(f"获取首页各位开发者大神的追随者们:{userprofile}")
        resp = session.get(userprofile)
        html = etree.HTML(resp.text)
        if html.xpath("//div[@class='paginate-container']/div[@class='BtnGroup']/a"):
            logging.info("获取下一页....")
            next_page = html.xpath("//div[@class='paginate-container']/div[@class='BtnGroup']/a/@href")
            if len(next_page) == 1:
                next_page = next_page[0]
            else:
                next_page = [page for page in next_page if 'after' in page][0]
            get_follows_funs_urls = html.xpath("//ol[@class='follow-list clearfix']/li/div[2]/h3/span/a/@href")
            get_follows_funs_urls = list(map(lambda x: urljoin(resp.url, x), get_follows_funs_urls))
            yield get_follows_funs_urls
            self.get_userprofile_follows_funs(next_page)
        else:
            logging.info("没有下一页了，到底了...")
            get_follows_funs_urls = html.xpath("//ol[@class='follow-list clearfix']/li/div[2]/h3/span/a/@href")
            get_follows_funs_urls = list(map(lambda x: urljoin(resp.url, x), get_follows_funs_urls))
            yield get_follows_funs_urls

    def get_userprofile_follows_funs_email(self, follows_funs_urls):
        logging.info("开始获取开发者邮箱...")
        print(f"开始获取开发者邮箱:{follows_funs_urls}...")
        resp = session.get(follows_funs_urls, headers=self.get_email_headers)
        html = etree.HTML(resp.text)
        url = follows_funs_urls
        email = html.xpath("//li[@itemprop='email']/a/text()")
        if email:
            email = email[0]
        else:
            email = ''
        return {
            'url':url,
            'email':email,
        }




if __name__ == '__main__':
    github().login('xxxxx','xxxxxx')

