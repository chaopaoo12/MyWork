# -*- encoding: utf-8 -*-
'''
@File    :   util.py
@Time    :   2024/08/03 10:13:56
@Author  :   chaopaoo12 
@Version :   1.0
@Contact :   chaopaoo12@hotmail.com
'''

# here put the import lib

import os

def check_files(name, path=None):
    '''
    
    :param name: 需要检测的文件或文件夹名
    :param path: 需要检测的文件或文件夹所在的路径，当path=None时默认使用当前路径检测
    :return: True/False 当检测的文件或文件夹所在的路径下有目标文件或文件夹时返回Ture,
            当检测的文件或文件夹所在的路径下没有有目标文件或文件夹时返回False
    '''
    
    if path is None:
        path = os.getcwd()
    if os.path.exists(path + '/' + name):
        print("Under the path: " + path + '\n' + name + " is exist")
        return True
    else:
        if (os.path.exists(path)):
            print("Under the path: " + path + '\n' + name + " is not exist")
        else:
            print("This path could not be found: " + path + '\n')
        return False