#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os

import matplotlib.pyplot as plt

from guoren_api import GuorenApi
from xueqiu_data import XueqiuStockList

plt.style.use('ggplot')


def generate_data_by_code_using_guoren(code, name, reserved_count=1800):
    os.makedirs('gen/custom/', exist_ok=True)
    plt.figure(num=1, figsize=(8, 36))
    plt.clf()
    guoren_api = GuorenApi(code)

    plt.subplot(911)
    plt.title('历史PE')
    guoren_content = guoren_api.submit_req_pe()
    print(guoren_content)
    pe_series = GuorenApi.parse_json_to_series_filter_dirty(guoren_content, lambda x: (x[0], float(x[1])),
                                                            reserved_count=reserved_count)
    total_len = len(pe_series)
    pe = pe_series.get(total_len - 1)
    gt_now_pe_percent = len(pe_series[pe_series > pe]) / total_len * 100
    pe = round(pe, 2)
    pe_series.plot()

    plt.subplot(912)
    plt.title('历史PB')
    guoren_content = guoren_api.submit_req_pb()
    print(guoren_content)
    pb_series = GuorenApi.parse_json_to_series(guoren_content, reserved_count=reserved_count)
    total_len = len(pe_series)
    pb = pb_series.get(total_len - 1)
    gt_now_pb_percent = len(pb_series[pb_series > pb]) / total_len * 100
    pb = round(pb, 2)
    pb_series.plot()

    plt.subplot(913)
    plt.title('5日均成交量(单位:10万)')
    guoren_content = guoren_api.submit_req_volume()
    print(guoren_content)
    try:
        volume_series = GuorenApi.parse_json_to_series_filter_dirty(guoren_content,
                                                                    lambda x: (x[0], int(x[1] / 100000)),
                                                                    reserved_count=reserved_count)
        total_len = len(volume_series)
        gt_now_volume_percent = len(
                volume_series[volume_series > volume_series.get(len(volume_series) - 1)]) / total_len * 100
        volume_series.plot()
    except TypeError:
        volume_series = None
        gt_now_volume_percent = None
        print("error to print")

    plt.subplot(914)
    plt.title('ROE')
    guoren_content = guoren_api.submit_req_roe()
    print(guoren_content)
    GuorenApi.parse_json_to_series(guoren_content, lambda x: x * 100, reserved_count=reserved_count).plot()

    plt.subplot(915)
    plt.title('股息率')
    guoren_content = guoren_api.submit_req_dy()
    print(guoren_content)
    dy_series = GuorenApi.parse_json_to_series(guoren_content, lambda x: x * 100, reserved_count=reserved_count)
    dy = round(dy_series.get(len(dy_series) - 1), 2)
    dy_series.plot()

    plt.subplot(916)
    plt.title('收入增长率')
    guoren_content = guoren_api.submit_req_income_grow()
    print(guoren_content)
    GuorenApi.parse_json_to_series(guoren_content, lambda x: x * 100, reserved_count=reserved_count).plot()

    plt.subplot(917)
    plt.title('利润增长率')
    guoren_content = guoren_api.submit_req_profie_grow()
    print(guoren_content)
    GuorenApi.parse_json_to_series_filter_dirty(guoren_content, lambda x: (x[0], int(x[1] * 100)),
                                                reserved_count=reserved_count).plot()

    plt.subplot(918)
    plt.title('毛利率')
    guoren_content = guoren_api.submit_req_gross()
    print(guoren_content)
    GuorenApi.parse_json_to_series(guoren_content, lambda x: x * 100, reserved_count=reserved_count).plot()

    plt.subplot(919)
    plt.title('净利率')
    guoren_content = guoren_api.submit_req_interest()
    print(guoren_content)
    GuorenApi.parse_json_to_series(guoren_content, lambda x: x * 100, reserved_count=reserved_count).plot()

    title = '{} {}\n动态市盈率:{}, 市净率:{},股息率:{}\n'.format(
            name, code, pe, pb, dy)
    title += '\n{} 到 {} {}%时间大于当前市盈率\n'.format(pe_series.first_valid_index(), pe_series.last_valid_index(),
                                               round(gt_now_pe_percent, 2))
    title += '\n{} 到 {} {}%时间大于当前市净率\n'.format(pb_series.first_valid_index(), pb_series.last_valid_index(),
                                               round(gt_now_pb_percent, 2))
    if volume_series is not None and gt_now_volume_percent is not None:
        title += '\n{} 到 {} {}%时间大于当前成交量\n'.format(volume_series.first_valid_index(), volume_series.last_valid_index(),
                                                   round(gt_now_volume_percent, 2))
    plt.suptitle(title)
    plt.savefig('gen/custom/{}_{}.png'.format(name, code))


def generate_data_by_xueqiu_strategy(xueqiu):
    # step 1: req filter strategy from xueqiu
    content = xueqiu.submit_req()
    print(content)
    xueqiu_stock_list = XueqiuStockList.create(content)
    while xueqiu_stock_list.has_more():
        content = xueqiu.submit_req(xueqiu_stock_list.get_req_new_page())
        print(content)
        xueqiu_stock_new_page_list = XueqiuStockList.create(content)
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
        GuorenApi.parse_json_to_series(guoren_content).plot()

        plt.subplot(812)
        plt.title('历史PB')
        guoren_content = guoren_api.submit_req_pb()
        print(guoren_content)
        GuorenApi.parse_json_to_series(guoren_content).plot()

        plt.subplot(813)
        plt.title('5日均成交量(单位:10万)')
        guoren_content = guoren_api.submit_req_volume()
        print(guoren_content)
        try:
            GuorenApi.parse_json_to_series_filter_dirty(guoren_content, lambda x: (x[0], int(x[1] / 100000))).plot()
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


# generate_data_by_xueqiu_strategy(XueqiuStrategies.fastest())
# generate_data_by_code_using_guoren('600886', '国投电力')
# generate_data_by_code_using_guoren('601166', '兴业银行')
# generate_data_by_code_using_guoren('600066', '宇通客车')
# generate_data_by_code_using_guoren('601318', '中国平安', 1400)
generate_data_by_code_using_guoren('600048', '保利地产')
