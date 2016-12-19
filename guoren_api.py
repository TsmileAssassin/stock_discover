import urllib.request

from user_define_cookie import UserDefineCookie


class GuorenApi(object):
    def __init__(self, symbol=None):
        self.symbol = symbol
        self.__req_url = 'https://guorn.com/stock/query'

    def get_req_headers(self):
        return {
            'Connection': 'keep-alive',
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Origin': 'https://guorn.com',
            'X-Requested-With': 'XMLHttpRequest',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.98 Safari/537.36',
            'Referer': 'https://guorn.com/stock/history?his=1&ticker={},0.M.%E8%82%A1%E7%A5%A8%E6%AF%8F%E6%97%A5%E6%8C%87%E6%A0%87_%E5%B8%82%E7%9B%88%E7%8E%87.0,1'.format(
                    self.symbol),
            'Content-Type': 'application/json; charset=UTF-8',
            'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6',
            'Cookie': UserDefineCookie.get_guoren_cookie()
        }

    def get_req_url(self):
        return self.__req_url

    def get_req_data_pe(self):
        return '{"ticker":[["%s","0.M.股票每日指标_市盈率.0"]],"index":[],"sector":[],"pool":[],"strategy":[]}' % self.symbol

    def get_req_data_pb(self):
        return '{"ticker":[["%s","0.M.股票每日指标_市净率.0"]],"index":[],"sector":[],"pool":[],"strategy":[]}' % self.symbol

    def get_req_data_volume(self):
        return '{"ticker":[["%s","0.M.股票每日指标_5日均成交量.0"]],"index":[],"sector":[],"pool":[],"strategy":[]}' % self.symbol

if __name__ == '__main__':
    guoren_api = GuorenApi('601166')
    print('url:' + guoren_api.get_req_url())
    data = guoren_api.get_req_data_volume().encode("utf8")
    data_len = len(data)
    headers = guoren_api.get_req_headers()
    headers['Content-Length'] = str(data_len)
    print('header:' + headers.__repr__())
    guoren_req = urllib.request.Request(guoren_api.get_req_url(),
                                        data=data,
                                        headers=headers, method='POST')
    content = urllib.request.urlopen(guoren_req).read().decode("utf8")
    print(content)
