import pandas as pd
from selenium import webdriver
import requests
import json
import datetime
import time

def get_headers(headers):
    url = 'https://www.thingiverse.com/'
    options = webdriver.ChromeOptions()
    # 设置中文
    for (key,value) in headers.items():
        options.add_argument('%s="%s"' % (key, value))
    options.add_argument('headless')
    driver = webdriver.Chrome(chrome_options=options)
    driver.get(url)
    cookies=driver.get_cookies()
    driver.quit()
    ck = dict()
    for i in cookies:
        ck[i['name']] = i['value']
    headers.update({"Cookie":' ;'.join([k+'='+v for (k,v) in ck.items()])})
    return(headers)

class web_d():

    def __init__(self) -> None:
        pass

    def get_headers(headers):
        url = 'https://www.thingiverse.com/'
        options = webdriver.ChromeOptions()
        # 设置中文
        for (key,value) in headers.items():
            options.add_argument('%s="%s"' % (key, value))
        options.add_argument('headless')
        driver = webdriver.Chrome(chrome_options=options)
        driver.get(url)
        cookies=driver.get_cookies()
        driver.quit()
        ck = dict()
        for i in cookies:
            ck[i['name']] = i['value']
        headers.update({"Cookie":' ;'.join([k+'='+v for (k,v) in ck.items()])})
        return(headers)

def get_category(web_d, url):
    pass

def read_list(web_d, url):
    pass

def read_itempage(web_d, url):
    pass

def read_userpage(web_d, url):
    pass

def download_files(web_d, url):
    pass

def read_data_from_xueqiu(url, headers, proxy=None):

    url = url.format(timestamp = int(time.mktime(datetime.datetime.now().timetuple())*1000))
    if proxy is not None:
        proxies = {
            "http": "http://" + proxy[0],
        }
        response = requests.get(url,headers=headers, proxies=proxies)
    else:
        response = requests.get(url,headers=headers)
    res_dict = json.loads(response.text)

    if res_dict['data'] is not None:
        try:
            data = pd.DataFrame(res_dict['data']['item'],columns=res_dict['data']['column']).assign(code = res_dict['data']['symbol'])
        except:
            data = None
    else:
        print('fail')
        data = None
    return(data)


def read_financial_report(code, exchange, report_type):
    stockfi_url = 'https://stock.xueqiu.com/v5/stock/finance/{exchange}/{report_type}.json?symbol={code}&type=all&is_detail=true&count=1000&timestamp={timestamp}'.format(code=code,exchange=exchange, report_type=report_type, timestamp= int(time.mktime(datetime.datetime.now().timetuple())*1000))
    data = read_data_from_xueqiu(stockfi_url)
    columns_list = []
    for i in data['data']['list']:
        columns_list = columns_list +list(data['data']['list'][0].keys())
    columns_list = list(set(columns_list))
    if report_type != 'income':
        columns_list.remove('ctime')
        columns_list.remove('sd')
        columns_list.remove('ed')
    res = pd.DataFrame()
    for j in data['data']['list']:
        a = dict()
        for i in columns_list:
            if isinstance(j[i],list):
                a[i] = j[i][0]
            else:
                a[i] = j[i]
        res = res.append(pd.DataFrame(a,index=[0]))
    res = res.assign(report_date = res.report_date.apply(lambda x:x/1000))
    res = res.assign(report_date = res.report_date.apply(lambda x:str(datetime.datetime.fromtimestamp(x))[0:10]))
    return(res)