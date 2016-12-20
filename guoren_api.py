import json
import urllib.request

from pandas import Series

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

    def get_req_data_gross(self):
        return '{"ticker":[["%s","0.M.股票每日指标_销售毛利率.0"]],"index":[],"sector":[],"pool":[],"strategy":[]}' % self.symbol

    def get_req_data_interest(self):
        return '{"ticker":[["%s","0.M.股票每日指标_销售净利率.0"]],"index":[],"sector":[],"pool":[],"strategy":[]}' % self.symbol

    def get_req_data_dy(self):
        return '{"ticker":[["%s","0.M.股票每日指标_股息率.0"]],"index":[],"sector":[],"pool":[],"strategy":[]}' % self.symbol

    def get_req_data_roe(self):
        return '{"ticker":[["%s","0.M.股票每日指标_资权益回报率.0"]],"index":[],"sector":[],"pool":[],"strategy":[]}' % self.symbol

    def get_req_data_income_grow(self):
        return '{"ticker":[["%s","0.M.股票每日指标_营业收入同比增长.0"]],"index":[],"sector":[],"pool":[],"strategy":[]}' % self.symbol

    def get_req_data_profie_grow(self):
        return '{"ticker":[["%s","0.M.股票每日指标_净利润增长率.0"]],"index":[],"sector":[],"pool":[],"strategy":[]}' % self.symbol

    def get_req_data_gross_profie_grow(self):
        return '{"ticker":[["%s","0.M.股票每日指标_毛利润增长率.0"]],"index":[],"sector":[],"pool":[],"strategy":[]}' % self.symbol

    def submit_req_pe(self):
        return self.__submit_req(self.get_req_data_pe())

    def submit_req_pb(self):
        return self.__submit_req(self.get_req_data_pb())

    def submit_req_volume(self):
        return self.__submit_req(self.get_req_data_volume())

    def submit_req_gross(self):
        return self.__submit_req(self.get_req_data_gross())

    def submit_req_interest(self):
        return self.__submit_req(self.get_req_data_interest())

    def submit_req_dy(self):
        return self.__submit_req(self.get_req_data_dy())

    def submit_req_roe(self):
        return self.__submit_req(self.get_req_data_roe())

    def submit_req_income_grow(self):
        return self.__submit_req(self.get_req_data_income_grow())

    def submit_req_profie_grow(self):
        return self.__submit_req(self.get_req_data_profie_grow())

    def submit_req_gross_profie_grow(self):
        return self.__submit_req(self.get_req_data_gross_profie_grow())

    def __submit_req(self, req_data):
        guoren_data = req_data.encode("utf8")
        guoren_data_len = len(guoren_data)
        guoren_headers = self.get_req_headers()
        guoren_headers['Content-Length'] = str(guoren_data_len)
        guoren_req = urllib.request.Request(self.get_req_url(),
                                            data=guoren_data,
                                            headers=guoren_headers, method='POST')
        guoren_content = urllib.request.urlopen(guoren_req).read().decode("utf8")
        return guoren_content

    @staticmethod
    def parse_json_to_series(guoren_content, item_value_change_func=None, reserved_count=1800):
        guoren_data = json.loads(guoren_content)
        axis_data = guoren_data['data']['sheet_data']['meas_data'][0]
        axis_index = guoren_data['data']['sheet_data']['row'][0]['data'][1]
        axis_index = list(map(lambda x: x[2:], axis_index))
        if reserved_count < len(axis_data) == len(axis_index):
            end_index = len(axis_data)
            axis_data = axis_data[end_index - reserved_count:end_index:1]
            axis_index = axis_index[end_index - reserved_count:end_index:1]
        if item_value_change_func is not None:
            axis_data = list(map(item_value_change_func, axis_data))
        return Series(data=axis_data, index=axis_index)

    @staticmethod
    def parse_json_to_series_filter_dirty(guoren_content, item_change_func, reserved_count=1800):
        guoren_data = json.loads(guoren_content)
        axis_data = guoren_data['data']['sheet_data']['meas_data'][0]
        axis_index = guoren_data['data']['sheet_data']['row'][0]['data'][1]
        axis_index = list(map(lambda x: x[2:], axis_index))
        axis_tuple_list = list(zip(axis_index, axis_data))
        if reserved_count < len(axis_tuple_list):
            end_index = len(axis_tuple_list)
            axis_tuple_list = axis_tuple_list[end_index - reserved_count:end_index:1]
        axis_tuple_list = list(filter(lambda x: x[1] != '', axis_tuple_list))
        axis_tuple_list = list(map(item_change_func, axis_tuple_list))
        axis_unzip_tuple_list = list(zip(*axis_tuple_list))
        return Series(data=list(axis_unzip_tuple_list[1]), index=list(axis_unzip_tuple_list[0]))


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
