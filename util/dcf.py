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
    value_now = 445
    value_estimate = dcf(39.88, [3, 3, 10, 10, 5], 10, 0)
    print('===宇通客车 Discount: %f \n' % (value_now / value_estimate))

    # 兴业银行保守
    value_now = 3277
    value_estimate = dcf(502.5, [2, 2, 2, 2, 2], 10, 0)
    print('===兴业银行 Discount: %f \n' % (value_now / value_estimate))

    # 中国平安保守
    value_now = 6796
    value_estimate = dcf(695, [10, 10, 10, 5, 5], 10, 0)
    print('===中国平安 Discount: %f \n' % (value_now / value_estimate))

    # 国投电力保守
    value_now = 459
    value_estimate = dcf(39, [3, 3, 10, 10, 10], 10, 0)
    print('===国投电力 Discount: %f \n' % (value_now / value_estimate))

    # 保利地产保守
    value_now = 1134
    value_estimate = dcf(130, [5, 5, 5, 5, 5], 10, 0)
    print('===保利地产 Discount: %f \n' % (value_now / value_estimate))
