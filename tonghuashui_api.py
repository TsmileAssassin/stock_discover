import json
import urllib.request

from bs4 import BeautifulSoup
from pandas import Series


class TonghuashuiApi(object):
    def __init__(self, symbol=None):
        self.symbol = symbol
        self.__req_url = 'http://basic.10jqka.com.cn/{}/finance.html'.format(symbol)
        self.bank_data = None
        self.insurance_data = None

    def get_req_url(self):
        return self.__req_url

    @staticmethod
    def get_req_headers():
        return {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.98 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Cookie': 'searchGuide=sg; usersurvey=1; isTradeDay=yes; reviewJump=nojump',
        }

    def is_bank_req(self):
        return self.bank_data is not None

    # 银行拨备覆盖率
    def get_bank_provision_coverage_series(self, begin_year):
        return self.get_percentage_series(3, begin_year)

    # 银行拨备覆盖率最大值
    def get_bank_max_provision_coverage(self, begin_year):
        return self.get_max_data_tuple(3, begin_year)

    # 坏账率
    def get_bank_bad_debts_series(self, begin_year):
        return self.get_percentage_series(8, begin_year)

    # 坏账率最大值
    def get_bank_max_bad_debts(self, begin_year):
        return self.get_max_data_tuple(8, begin_year)

    # 净息差
    def get_bank_interest_series(self, begin_year):
        return self.get_percentage_series(17, begin_year)

    # 净息差最大值
    def get_bank_max_interest(self, begin_year):
        return self.get_max_data_tuple(17, begin_year)

    def get_max_data_tuple(self, data_index, begin_year):
        axis_data = self.bank_data['report'][data_index]
        axis_index = self.bank_data['report'][0]
        axis_index = list(map(lambda x: x[2:], axis_index))
        axis_tuple_list = list(zip(axis_index, axis_data))
        axis_tuple_list = list(
            filter(lambda x: x[1] != '' and x[1] is not False and begin_year <= int(x[0][0:2]) < 30, axis_tuple_list))
        return axis_tuple_list[0]

    def get_percentage_series(self, data_index, begin_year):
        axis_data = self.bank_data['report'][data_index]
        axis_index = self.bank_data['report'][0]
        axis_index = list(map(lambda x: x[2:], axis_index))
        axis_tuple_list = list(zip(axis_index, axis_data))
        axis_tuple_list = list(
            filter(lambda x: x[1] != '' and x[1] is not False and begin_year <= int(x[0][0:2]) < 30, axis_tuple_list))
        axis_tuple_list = list(
            map(lambda x: (x[0], float(x[1][:-1])), axis_tuple_list))
        axis_tuple_list.reverse()
        axis_unzip_tuple_list = list(zip(*axis_tuple_list))
        return Series(data=list(axis_unzip_tuple_list[1]), index=list(axis_unzip_tuple_list[0]))

    def submit_req(self):
        headers = TonghuashuiApi.get_req_headers()
        url = self.get_req_url()
        print('---req:\n' + url)
        req = urllib.request.Request(url, headers=headers)
        content = urllib.request.urlopen(req).read().decode('gbk')
        soup = BeautifulSoup(content, 'html.parser')
        benefit_text = soup.find('p', attrs={'id': 'benefit'}).get_text()
        print('利润表:\n {}'.format(benefit_text))
        debt_text = soup.find('p', attrs={'id': 'debt'}).get_text()
        print('资产负债表:\n {}'.format(debt_text))
        cash_text = soup.find('p', attrs={'id': 'cash'}).get_text()
        print('现金流量表:\n {}'.format(cash_text))
        main_text = soup.find('p', attrs={'id': 'main'}).get_text()
        print('主要指标:\n {}'.format(main_text))
        grow_text = soup.find('p', attrs={'id': 'grow'}).get_text()
        print('增长指标:\n {}'.format(grow_text))
        pay_text = soup.find('p', attrs={'id': 'pay'}).get_text()
        print('偿债指标:\n {}'.format(pay_text))
        operate_text = soup.find('p', attrs={'id': 'operate'}).get_text()
        print('营运指标:\n {}'.format(operate_text))

        bank_data = soup.find('p', attrs={'id': 'bank'})
        insurance_data = soup.find('p', attrs={'id': 'insurance'})
        if bank_data is not None:
            bank_text = soup.find('p', attrs={'id': 'bank'}).get_text()
            print('银行专项指标:\n {}'.format(bank_text))
            self.bank_data = json.loads(bank_text)
        elif insurance_data is not None:
            insurance_text = soup.find('p', attrs={'id': 'insurance'}).get_text()
            print('保险专项指标:\n {}'.format(insurance_text))
            self.insurance_data = json.loads(insurance_text)

    def is_bank_data(self):
        return self.bank_data is not None

    def get_bank_series_by_index(self, index=1):
        pass


if __name__ == '__main__':
    # api = TonghuashuiApi('601318')
    # api.submit_req()
    api = TonghuashuiApi('601166')
    api.submit_req()
    api.get_bank_provision_coverage_series()
