#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import os
from json.decoder import WHITESPACE

import matplotlib.pyplot as plt
from pandas import Series

from guoren_api import GuorenApi
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


# step 1: req filter strategy from xueqiu
xueqiu = XueqiuStategys.fastest()
content = xueqiu.submit_req()
print(content)
xueqiu_stock_list = json.loads(content, cls=StockDecoder)
while xueqiu_stock_list.has_more():
    content = xueqiu.submit_req(xueqiu_stock_list.get_req_new_page())
    print(content)
    xueqiu_stock_new_page_list = json.loads(content, cls=StockDecoder)
    xueqiu_stock_list.append_list(xueqiu_stock_new_page_list.stock_list)
print("\ncount:{}".format(len(xueqiu_stock_list.stock_list)))

os.makedirs('gen/{}/'.format(xueqiu.name), exist_ok=True)
file = open('gen/{}.txt'.format(xueqiu.name), 'w', encoding='utf-8')
file.write('{}'.format(xueqiu_stock_list.stock_list))
file.close()

# step 2: draw pic and req detail from guoren
for idx, stock_item in enumerate(xueqiu_stock_list.stock_list):
    plt.figure(num=1, figsize=(8, 30))
    plt.clf()
    plt.suptitle('{} {}\n动态市盈率:{}, 市净率:{},股息率:{}'.format(
            stock_item.name, stock_item.symbol, stock_item.pettm, stock_item.pb, stock_item.dy))
    print('symbol:' + stock_item.symbol[2:])
    guoren_api = GuorenApi(stock_item.symbol[2:])

    plt.subplot(811)
    plt.title('历史PE')
    guoren_content = guoren_api.submit_req_pe()
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

    plt.subplot(812)
    plt.title('历史PB')
    guoren_content = guoren_api.submit_req_pb()
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

    plt.subplot(813)
    plt.title('5日均成交量(单位:10万)')
    guoren_content = guoren_api.submit_req_volume()
    print(guoren_content)
    guoren_volume_data = json.loads(guoren_content)
    axis_data = guoren_volume_data['data']['sheet_data']['meas_data'][0]
    axis_index = guoren_volume_data['data']['sheet_data']['row'][0]['data'][1]
    axis_index = list(map(lambda x: x[2:], axis_index))
    axis_tuple_list = list(zip(axis_index, axis_data))
    try:
        if 1500 < len(axis_tuple_list):
            end_index = len(axis_tuple_list)
            axis_tuple_list = axis_tuple_list[end_index - 1500:end_index:1]
            axis_tuple_list = list(filter(lambda x: x[1] != '', axis_tuple_list))
            axis_tuple_list = list(map(lambda x: (x[0], int(x[1] / 100000)), axis_tuple_list))
        axis_unzip_tuple_list = list(zip(*axis_tuple_list))
        Series(data=list(axis_unzip_tuple_list[1]), index=list(axis_unzip_tuple_list[0])).plot()
    except TypeError:
        print("error to print")

    plt.subplot(814)
    plt.title(stock_item.roediluted.name)
    stock_item.roediluted.sort_index(ascending=True).plot()
    plt.subplot(815)
    plt.title(stock_item.income_grow.name)
    stock_item.income_grow.sort_index(ascending=True).plot()
    plt.subplot(816)
    plt.title(stock_item.profit_grow.name)
    stock_item.profit_grow.sort_index(ascending=True).plot()
    plt.subplot(817)
    plt.title(stock_item.gross.name)
    stock_item.gross.sort_index(ascending=True).plot()
    plt.subplot(818)
    plt.title(stock_item.interest.name)
    stock_item.interest.sort_index(ascending=True).plot()
    # plt.show()
    plt.savefig('gen/{}/{}_{}.png'.format(xueqiu.name, stock_item.name, stock_item.symbol))
