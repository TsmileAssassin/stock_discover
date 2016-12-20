import urllib.request

from user_define_cookie import UserDefineCookie


class XueqiuApi(object):
    def __init__(self, name=None):
        self.name = name
        self.__req_url = 'https://xueqiu.com/stock/screener/screen.json?category=SH&exchange=&areacode=&indcode=&_=1425870008963'

    # 动态市盈率
    def append_pettm(self, start='0', end='20'):
        self.__req_url = self.__req_url + '&pettm=' + start + '_' + end

    # 市净率
    def append_pb(self, start='0', end='30'):
        self.__req_url = self.__req_url + '&pb=' + start + '_' + end

    # 股息率
    def append_dy(self, start='0', end='100'):
        self.__req_url = self.__req_url + '&dy=' + start + '_' + end

    # 净资产收益率
    def append_roediluted(self, time, start='5', end='100', is_order_by_this=False):
        key_name = 'roediluted.' + time
        self.__req_url = self.__req_url + '&' + key_name + '=' + start + '_' + end
        if is_order_by_this:
            self.__req_url = self.__req_url + '&orderby=' + key_name + '&order=desc'

    # 毛利率
    def append_gross(self, time, start='0', end='100'):
        key_name = 'sgpr.' + time
        self.__req_url = self.__req_url + '&' + key_name + '=' + start + '_' + end

    # 净利率
    def append_interest(self, time, start='0', end='100'):
        key_name = 'snpr.' + time
        self.__req_url = self.__req_url + '&' + key_name + '=' + start + '_' + end

    # 收入增长
    def append_income_grow(self, time, start='-30', end='500'):
        key_name = 'mbig.' + time
        self.__req_url = self.__req_url + '&' + key_name + '=' + start + '_' + end

    # 利润增长
    def append_profie_grow(self, time, start='-30', end='500'):
        key_name = 'nig.' + time
        self.__req_url = self.__req_url + '&' + key_name + '=' + start + '_' + end

    # 资产负债率
    def append_debt_assert_rate(self, time, start='0', end='100'):
        key_name = 'dar.' + time
        self.__req_url = self.__req_url + '&' + key_name + '=' + start + '_' + end

    def get_req_url(self):
        return self.__req_url

    def submit_req(self, page=1):
        headers = XueqiuApi.get_req_headers()
        url = self.get_req_url()
        print('---req:\n' + url)
        if page > 1:
            url += '&page=%d' % page
        req = urllib.request.Request(url, headers=headers)
        content = urllib.request.urlopen(req).read().decode("utf8")
        return content

    @staticmethod
    def get_req_headers():
        return {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.98 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Cookie': UserDefineCookie.get_xueqiu_cookie(),
        }
