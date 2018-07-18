import requests
from flask import Flask, request, make_response
from pyquery import PyQuery as jq

app = Flask(__name__, static_folder='images', static_url_path='')

cookies = {}


def do_login():
    res = requests.post('http://tgkb168.com/muserChkLoginc.asp?hx66=login',
                        allow_redirects=False,
                        data='username=%C1%F5%BA%E3&password=qwer7226361',
                        headers={'Content-Type': 'application/x-www-form-urlencoded'})
    for i in res.cookies.items():
        cookies[i[0]] = i[1]


def do_comm_request(url):
    return requests.get(url, allow_redirects=False, cookies=cookies)


def get_index_page():
    if not cookies:
        do_login()

    url = 'http://tgkb168.com/index_cctv.asp'

    res = do_comm_request(url)

    # 可能是登入超时或者登入失效
    if int(res.headers['Content-Length']) < 250:
        do_login()
        res = do_comm_request(url)

    return str(res.content,'gb2312')

    dom = jq(res.content, parser='html')
    dom('.phone-top').remove()
    dom('script').remove()
    dom('#divkjt_bg').remove()

    return dom.__str__()


@app.errorhandler(404)
def page_not_found(error):
    path = request.path
    if 'inc/js.js' in path:
        return ""

    # res = redirect('http://tgkb168.com{}'.format(path))
    # res.headers['Access-Control-Allow-Origin'] = '*'
    # for key, value in cookies.items():
    #     res.set_cookie(key, value)
    # return res

    proxyres = requests.get('http://tgkb168.com{}'.format(path))
    content = proxyres.content
    relres = make_response(content)
    relres.headers['Content-Type'] = proxyres.headers['Content-Type']

    with open('./images/{}'.format(request.path[1:]), 'wb') as file:
        file.write(content)

    return relres


@app.route('/stocklist.html')
def index():
    return get_index_page()


@app.route("/")
def hello_world():
    return 'Hello World! {}'


print(app.url_map)

if __name__ == '__main__':
    app.run()
