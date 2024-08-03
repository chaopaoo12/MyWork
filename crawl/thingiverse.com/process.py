# -*- encoding: utf-8 -*-
'''
@File    :   process.py
@Time    :   2024/08/03 10:39:12
@Author  :   chaopaoo12 
@Version :   1.0
@Contact :   chaopaoo12@hotmail.com
'''

# here put the import lib

from read_format import get_soup,download_files,cancel_modal,read_itemPage,read_listPage,check_success
from util import check_files

def read_fromListPage(driver):
    html = get_soup(driver)
    list_data = read_listPage(html)
    return(list_data)

def read_fromItemPage(driver):
    html = get_soup(driver)
    list_data = read_itemPage(html)
    return(list_data)

def download_action(driver, download_dir):
    list_data = read_fromItemPage(driver)
    file_name1 = str(list_data['itemTitle'] + ' - ' + list_data['itemId'] + '.zip')
    file_name2 = str(list_data['itemTitle'] + '(Must Use Supports) - ' + list_data['itemId'] + '.zip')
    while check_files(file_name1, download_dir) is not True or check_files(file_name2, download_dir) is not True:
        download_files(driver)
        if check_success(driver) is not True:
            cancel_modal(driver)
        else:
            pass
            
        
    