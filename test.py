import requests as request
import urllib.parse as url
from pyquery import PyQuery as jq

cookies = {}

html = request.get("https://www.baidu.com/").text
dom = jq(html)
print(dom('#lg'))


def do_login():
    res = request.post('http://tgkb168.com/muserChkLoginc.asp?hx66=login',
                       allow_redirects=False,
                       data='username=%C1%F5%BA%E3&password=qwer7226361',
                       headers={'Content-Type': 'application/x-www-form-urlencoded'})
    for i in res.cookies.items():
        cookies[i[0]] = i[1]
    for k, v in cookies.items():
        print(k, v)


# do_login()


def do_comm_request(url):
    return request.get(url, allow_redirects=False, cookies=cookies)


def get_index_page():
    if not cookies:
        do_login()

    url = 'http://tgkb168.com/index_cctv.asp'

    res = do_comm_request(url)

    # 可能是登入超时或者登入失效
    if int(res.headers['Content-Length']) < 250:
        do_login()
        res = do_comm_request(url)

    return str(res.content, 'GB2312')

# get_index_page()
