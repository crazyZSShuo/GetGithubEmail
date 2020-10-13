import logging
import re
import random

import requests
import scrapy

from github.settings import USERNAME,PASSWORD,COOKIE_POOL


headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
}

# 使用requests完成登录
def login_get_cookies_requests():
    if not USERNAME or not PASSWORD:
        raise ValueError('用户名或密码必须填，请检查！')
    res1 = requests.get('https://github.com/login', headers=headers)
    logging.warning("开始登录...")
    authenticity_token = re.findall(r'authenticity_token.*?value="(.*?)"', res1.text)[0]
    logging.warning(f"获取authenticity_token：{authenticity_token}")
    _device_id_cookie = {"_device_id":"86704863fabc61a602b7e77a5cfe040b"}
    cookie = res1.cookies.get_dict()
    cookie.update(_device_id_cookie)
    try:
        res2 = requests.post(
            'https://github.com/session',
            data={
                'commit': 'Sign in',
                'utf8': '✓',
                'authenticity_token': authenticity_token,
                'login': USERNAME,
                'password': PASSWORD,
            },
            cookies=cookie,
            headers=headers,
        )

        if res2.status_code not in [301,302,400,404,403]:
            print(res2.status_code)
            logging.warning("登录成功！")
            print("登录成功！")
            return res2.cookies.get_dict()
        else:
            #logging.warning("新环境登录，需要邮箱验证码")
            #logging.warning("开始尝试使用Cookie池")
            #return random.choice(COOKIE_POOL)
            if "verified-device" in res2.url:
                print(res2.url)
                raise ValueError("新环境登录，需要邮箱验证码")
    except Exception as e:
        logging.warning(f'登陆失败！{e}')
        raise e


def test_url():
    url = 'https://github.com/ichtrojan'
    cookies = login_get_cookies_requests()
    resp = requests.get(url, cookies=cookies)
    from lxml import etree
    html = etree.HTML(resp.text)
    email = html.xpath("//li[@itemprop='email']/a/text()")
    print(email)


if __name__ == '__main__':
    test_url()
