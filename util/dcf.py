def dcf(now_profit, grow_rate_list, discount_rate, forever_rate=0):
    market_value = 0

    last_profit = now_profit
    last_year = 1
    for grow_rate in grow_rate_list:
        last_profit *= 1 + float(grow_rate) / 100.0
        discount_profit = last_profit / ((1 + float(discount_rate) / 100.0) ** last_year)
        last_year += 1
        print('Year: %d -> last: %f, dis: %f, rate: %f%%' % (last_year - 1, last_profit, discount_profit, grow_rate))
        market_value += discount_profit

    for_ever_value = last_profit * (1 + float(forever_rate) / 100.0) / (
        float(discount_rate) / 100.0 - float(forever_rate) / 100.0)
    discount_for_ever_value = for_ever_value / ((1 + float(discount_rate) / 100.0) ** (last_year - 1))
    print('for ever: -> last: %f, dis: %f' % (for_ever_value, discount_for_ever_value))

    market_value += discount_for_ever_value
    print('=====Finally: -> %f' % market_value)
    return market_value


if __name__ == '__main__':
    # 宇通客车保守
    value_now = 439
    value_estimate = dcf(40.44, [-12, 3, 3, 10, 5], 10, 0)
    print('===宇通客车 Discount: %f \n' % (value_now / value_estimate))

    # 兴业银行保守
    value_now = 3307
    value_estimate = dcf(538, [2, 2, 2, 2, 2], 10, 0)
    print('===兴业银行 Discount: %f \n' % (value_now / value_estimate))

    # 中国平安保守
    value_now = 7861
    value_estimate = dcf(623, [15, 12, 10, 8, 5], 10, 0)
    print('===中国平安 Discount: %f \n' % (value_now / value_estimate))

    # 国投电力保守
    value_now = 518
    value_estimate = dcf(39, [-7, 8, 20, 12, 12], 10, 0)
    print('===国投电力 Discount: %f \n' % (value_now / value_estimate))

    # 川投能源保守
    value_now = 410
    value_estimate = dcf(35, [-5, 5, 15, 12, 12], 10, 0)
    print('===川投能源 Discount: %f \n' % (value_now / value_estimate))

    # 保利地产保守
    value_now = 1147
    value_estimate = dcf(124, [12, 15, 10, 3, 3], 10, 0)
    print('===保利地产 Discount: %f \n' % (value_now / value_estimate))

    # 中国建筑保守
    value_now = 2700
    value_estimate = dcf(300, [10, 10, 8, 5, 5], 10, 0)
    print('===中国建筑 Discount: %f \n' % (value_now / value_estimate))

    # 长安汽车保守
    value_now = 618
    value_estimate = dcf(102, [-15, 0, 10, 10, 5], 10, 0)
    print('===长安汽车 Discount: %f \n' % (value_now / value_estimate))

    # 泰禾集团保守
    value_now = 200
    value_estimate = dcf(17, [20, 30, 60, 1, 1], 10, 0)
    print('===泰禾集团 Discount: %f \n' % (value_now / value_estimate))

    # 平安银行保守
    value_now = 1511
    value_estimate = dcf(225, [-2, -2, 1, 3, 3], 10, 0)
    print('===平安银行 Discount: %f \n' % (value_now / value_estimate))

    # # 格力电器保守
    # value_now = 1682
    # value_estimate = dcf(133, [3, 3, 3, 3, 3], 10, 0)
    # print('===格力电器 Discount: %f \n' % (value_now / value_estimate))
    #
    # # 美的集团保守
    # value_now = 2098
    # value_estimate = dcf(150, [5, 5, 5, 5, 5], 10, 0)
    # print('===美的集团 Discount: %f \n' % (value_now / value_estimate))
