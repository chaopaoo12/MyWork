# -*- encoding: utf-8 -*-
'''
@File    :   task.py
@Time    :   2024/08/03 17:41:09
@Author  :   chaopaoo12 
@Version :   1.0
@Contact :   chaopaoo12@hotmail.com
'''

# here put the import lib
from process import read_fromListPage,read_fromItemPage,download_action
from core import web_d
from read_format import get_nextPage
from store import insert_database
from fake_useragent import UserAgent

channel = {'3D':'https://www.thingiverse.com/?page=1&sort=newest&category_id=73',
           'ART':'https://www.thingiverse.com/?page=1&sort=newest&category_id=63',
           'FASHION':'https://www.thingiverse.com/?page=1&sort=newest&category_id=64',
           'GADGETS':'https://www.thingiverse.com/?page=1&sort=newest&category_id=65',
           'HOBBY':'https://www.thingiverse.com/?page=1&sort=newest&category_id=66',
           'HOUSEHOLD':'https://www.thingiverse.com/?page=1&sort=newest&category_id=67',
           'LEARNING':'https://www.thingiverse.com/?page=1&sort=newest&category_id=69',
           'MODELS':'https://www.thingiverse.com/?page=1&sort=newest&category_id=70',
           'TOOLS':'https://www.thingiverse.com/?page=1&sort=newest&category_id=71',
           'TOYS':'https://www.thingiverse.com/?page=1&sort=newest&category_id=72',
           'OTHER':'https://www.thingiverse.com/?page=1&sort=newest&category_id=0', 
}

def read_channel(url):
    headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Cache-Control': 'max-age=0',
            'User-Agent': UserAgent(),
            'Connection': 'close'
            }
    web_att = web_d(headers=headers)
    web_att.init_driver()
    web_att.read_data_from(url)
    list_data = read_fromListPage(web_att.driver)
    insert_database('item_info', list_data)
    print("','".join(list(list_data['itemLink'])))
    while get_nextPage(web_att.driver) is False:
        list_data = read_fromListPage(web_att.driver)
        insert_database('item_info', list_data)
    web_att.close()
    return(list_data)

def read_items(url_list):
    download_dir = 'E:/workspace/python/mywork/download'
    headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Cache-Control': 'max-age=0',
            'User-Agent': UserAgent(),
            'Connection': 'close'
            }
    web_att = web_d(headers=headers,download_dir=download_dir)
    web_att.init_driver()
    for url in url_list:
        web_att.read_data_from(url)
        list_data = read_fromItemPage(web_att.driver)
        insert_database('item_info', list_data)
        download_action(web_att.driver,download_dir=download_dir)
    web_att.close()
