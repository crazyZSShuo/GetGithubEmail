from requests import Session
import re

session = Session()

headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
}

res1 = session.get('https://github.com/login', headers=headers)
authenticity_token = re.findall(r'authenticity_token.*?value="(.*?)"', res1.text)[0]
_device_id_cookie = {"_device_id": "86704863fabc61a602b7e77a5cfe040b"}
cookie = res1.cookies.get_dict()
cookie.update(_device_id_cookie)
print(cookie)
res2 = session.post(
            'https://github.com/session',
            data={
                'commit': 'Sign in',
                'utf8': '✓',
                'authenticity_token': authenticity_token,
                'login': "XXXXXXXX",
                'password': "XXXXXXXXX",
            },
            cookies=cookie,
            headers=headers,
            # allow_redirects = False
        )
cookies = res2.cookies.get_dict()
print(cookies)
#url = 'https://github.com/philographer'
url = 'https://github.com/mahdisalehian'
resp = session.get(url, cookies=cookies)
from lxml import etree

html = etree.HTML(resp.text)
email = html.xpath("//li[@itemprop='email']/a/text()")
print(email)



