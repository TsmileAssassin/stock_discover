#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import os
import urllib.request
from json.decoder import WHITESPACE

import matplotlib.pyplot as plt
from pandas import Series

from guoren_api import GuorenApi
from xueqiu_api import XueqiuApi
from xueqiu_data import XueqiuStock
from xueqiu_data import XueqiuStockList
from xueqiu_strategy import XueqiuStategys

plt.style.use('ggplot')


class StockDecoder(json.JSONDecoder):
    def decode(self, s, _w=WHITESPACE.match):
        dict_data = super().decode(s)
        if dict_data['count'] > 0:
            local_stock_data = XueqiuStockList(total_count=dict_data['count'])
            for item in dict_data['list']:
                stock = XueqiuStock.create(item)
                local_stock_data.append(stock)
            return local_stock_data
        return XueqiuStockList()


xueqiu = XueqiuStategys.stable()
headers = XueqiuApi.get_req_headers()
url = xueqiu.get_req_url()
print('---req:\n' + url)
req = urllib.request.Request(url, headers=headers)
content = urllib.request.urlopen(req).read().decode("utf8")
print(content)
xueqiu_stock_list = json.loads(content, cls=StockDecoder)
while xueqiu_stock_list.has_more():
    new_url = url + '&page=%d' % xueqiu_stock_list.get_req_new_page()
    print('---req:%d\n' % xueqiu_stock_list.get_req_new_page() + new_url)
    req = urllib.request.Request(new_url, headers=headers)
    content = urllib.request.urlopen(req).read().decode("utf8")
    print(content)
    xueqiu_stock_new_page_list = json.loads(content, cls=StockDecoder)
    xueqiu_stock_list.append_list(xueqiu_stock_new_page_list.stock_list)
print("\ncount:{}".format(len(xueqiu_stock_list.stock_list)))

os.makedirs('gen/{}/'.format(xueqiu.name), exist_ok=True)
file = open('gen/{}.txt'.format(xueqiu.name), 'w', encoding='utf-8')
file.write('{}'.format(xueqiu_stock_list.stock_list))
file.close()
for idx, stock_item in enumerate(xueqiu_stock_list.stock_list):
    plt.figure(num=1, figsize=(8, 26))
    plt.clf()
    plt.suptitle('{} {}\n动态市盈率:{}, 市净率:{},股息率:{}'.format(
            stock_item.name, stock_item.symbol, stock_item.pettm, stock_item.pb, stock_item.dy))
    print('symbol:' + stock_item.symbol[2:])
    guoren_api = GuorenApi(stock_item.symbol[2:])

    plt.subplot(711)
    plt.title('历史PE')
    guoren_data = guoren_api.get_req_data_pe().encode("utf8")
    print('pe_guoren_data:' + guoren_api.get_req_data_pe())
    guoren_data_len = len(guoren_data)
    guoren_headers = guoren_api.get_req_headers()
    guoren_headers['Content-Length'] = str(guoren_data_len)
    guoren_req = urllib.request.Request(guoren_api.get_req_url(),
                                        data=guoren_data,
                                        headers=guoren_headers, method='POST')
    guoren_content = urllib.request.urlopen(guoren_req).read().decode("utf8")
    print(guoren_content)
    guoren_pe_data = json.loads(guoren_content)
    axis_data = guoren_pe_data['data']['sheet_data']['meas_data'][0]
    axis_index = guoren_pe_data['data']['sheet_data']['row'][0]['data'][1]
    axis_index = list(map(lambda x: x[2:], axis_index))
    if 1500 < len(axis_data) == len(axis_index):
        end_index = len(axis_data)
        axis_data = axis_data[end_index - 1500:end_index:1]
        axis_index = axis_index[end_index - 1500:end_index:1]
    Series(data=axis_data, index=axis_index).plot()

    plt.subplot(712)
    plt.title('历史PB')
    guoren_data = guoren_api.get_req_data_pb().encode("utf8")
    print('pb_guoren_data:' + guoren_api.get_req_data_pb())
    guoren_data_len = len(guoren_data)
    guoren_headers = guoren_api.get_req_headers()
    guoren_headers['Content-Length'] = str(guoren_data_len)
    guoren_req = urllib.request.Request(guoren_api.get_req_url(),
                                        data=guoren_data,
                                        headers=guoren_headers, method='POST')
    guoren_content = urllib.request.urlopen(guoren_req).read().decode("utf8")
    print(guoren_content)
    guoren_pb_data = json.loads(guoren_content)
    axis_data = guoren_pb_data['data']['sheet_data']['meas_data'][0]
    axis_index = guoren_pb_data['data']['sheet_data']['row'][0]['data'][1]
    axis_index = list(map(lambda x: x[2:], axis_index))
    if 1500 < len(axis_data) == len(axis_index):
        end_index = len(axis_data)
        axis_data = axis_data[end_index - 1500:end_index:1]
        axis_index = axis_index[end_index - 1500:end_index:1]
    Series(data=axis_data, index=axis_index).plot()

    plt.subplot(713)
    plt.title(stock_item.roediluted.name)
    stock_item.roediluted.sort_index(ascending=True).plot()
    plt.subplot(714)
    plt.title(stock_item.income_grow.name)
    stock_item.income_grow.sort_index(ascending=True).plot()
    plt.subplot(715)
    plt.title(stock_item.profit_grow.name)
    stock_item.profit_grow.sort_index(ascending=True).plot()
    plt.subplot(716)
    plt.title(stock_item.gross.name)
    stock_item.gross.sort_index(ascending=True).plot()
    plt.subplot(717)
    plt.title(stock_item.interest.name)
    stock_item.interest.sort_index(ascending=True).plot()
    # plt.show()
    plt.savefig('gen/{}/{}_{}.png'.format(xueqiu.name, stock_item.name, stock_item.symbol))
