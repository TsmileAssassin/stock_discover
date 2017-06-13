import json
import os
import urllib.request


def download_financial_year_statements(code, year, is_mid_year=False):
    # 从巨潮资讯网下载文档
    req_data = 'stock={}'.format(code)
    req_data += '&pageNum=1&pageSize=30'
    req_data += '&searchkey=&tabName=fulltext&sortName=&sortType=&limit=&seDate=Name'
    if is_mid_year:
        req_data += '&category=category_bndbg_szsh%3B&column=szse_main'
    else:
        req_data += '&category=category_ndbg_szsh%3B&column=sse'
    print(req_data)
    req_data_bytes = req_data.encode('utf8')
    headers = {
        'X-Requested-With': 'XMLHttpRequest',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.98 Safari/537.36',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6',
        'Origin': 'http://www.cninfo.com.cn',
        'Connection': 'keep-alive',
        'Referer': 'http://www.cninfo.com.cn/cninfo-new/disclosure/szse/showFulltext/{}'.format(code),
    }
    content_len = len(req_data_bytes)
    headers['Content-Length'] = str(content_len)
    req = urllib.request.Request('http://www.cninfo.com.cn/cninfo-new/announcement/query',
                                 data=req_data_bytes, headers=headers, method='POST')
    print(headers)
    content = urllib.request.urlopen(req).read().decode("utf8")
    print(content)
    statements_data = json.loads(content)
    found_statement = None
    for statement in statements_data['announcements']:
        statement_title = statement['announcementTitle']
        if statement_title.find(year) >= 0 and statement_title.find('摘要') < 0:
            found_statement = statement
            break
    if found_statement is not None:
        os.makedirs('../gen/statement/', exist_ok=True)
        statement_file_url = 'http://www.cninfo.com.cn/' + found_statement['adjunctUrl']
        print(statement_file_url)
        if is_mid_year:
            local_file = '../gen/statement/{}_{}M.pdf'.format(found_statement['secName'], year)
        else:
            local_file = '../gen/statement/{}_{}.pdf'.format(found_statement['secName'], year)
        urllib.request.urlretrieve(statement_file_url, local_file)


if __name__ == '__main__':
    download_financial_year_statements('000671', '2016')
    # download_financial_year_statements('600048', '2015')
    # download_financial_year_statements('600048', '2014')
    # download_financial_year_statements('600048', '2013')
