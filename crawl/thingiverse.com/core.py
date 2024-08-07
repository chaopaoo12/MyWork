# -*- encoding: utf-8 -*-
'''
@File    :   core.py
@Time    :   2024/08/03 10:14:36
@Author  :   chaopaoo12 
@Version :   1.0
@Contact :   chaopaoo12@hotmail.com
'''

# here put the import lib
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import re
import time

def enable_download(driver, download_dir):
    driver.execute_cdp_cmd("Page.setDownloadBehavior", {
        "behavior": "allow",
        "downloadPath": download_dir
    })
    
class web_d():

    def __init__(self,headers,DRIVER_PATH='C:\\ProgramData\\anaconda3\\Scripts\\chromedriver.exe',download_dir=None) -> None:
        self.headers = headers
        self.DRIVER_PATH = DRIVER_PATH
        self.download_dir = download_dir
        
    def init_options(self,ip_proxy=None): 
        self.options = webdriver.ChromeOptions()
        #for (key,value) in self.headers.items():
        #    self.options.add_argument('%s="%s"' % (key, value))
        self.options.page_load_strategy = 'none'
        self.options.add_argument('--blink-settings=imagesEnabled=false')
        ##self.options.add_argument('headless')
        self.options.add_argument('–-disable-javascript')   #禁用javascript
        self.options.add_argument('--disable-plugins')   #禁用插件
        self.options.add_argument("--disable--gpu")#禁用显卡
        self.options.add_argument("--disable-images")#禁用图像
        self.options.add_argument("--no-sandbox")
        self.options.add_argument("--disable-dev-shm-usage")
        self.options.add_experimental_option("excludeSwitches", ["enable-automation"])
        self.options.add_experimental_option('useAutomationExtension', False)
        prefs = {'profile.default_content_settings.popups': 0, 'download.default_directory': self.download_dir}
        self.options.add_experimental_option('prefs', prefs)
        if ip_proxy is not None:
            self.options.add_argument(ip_proxy)
    
    def update_cookie(self, driver):
        cookies=driver.get_cookies()
        ck = dict()
        for i in cookies:
            ck[i['name']] = i['value']
        self.options.add_argument('Cookie="%s"' % (' ;'.join([k+'='+v for (k,v) in ck.items()])))
    
    def update_options(self):
        for (key,value) in self.headers.items():
            self.options.add_argument('%s="%s"' % (key, value))

    def init_driver(self, url='https://www.thingiverse.com/'):
        self.init_options()
        service = Service(executable_path=self.DRIVER_PATH)
        self.driver = webdriver.Chrome(service=service,options=self.options)
        self.driver.get(url)
        self.update_cookie(self.driver)
        self.get_authorization()
        self.driver.quit()
        self.driver = webdriver.Chrome(service=service,options=self.options)
        self.driver.header_overrides={"Authorization":self.authorization}
        for request in self.driver.requests:
            print(request.headers)
            break  #只打印一次即可

    
    def interceptor(self, request):
        request.headers['Authorization'] = self.authorization
        print(request.headers)
    
    def refresh_driver(self):
        self.update_cookie(self.driver)
        self.driver.quit()
        service = Service(executable_path=self.DRIVER_PATH)
        self.driver = webdriver.Chrome(service=service,options=self.options)
        
    def read_data_from(self, url):
        print('read data from:', url.encode('ascii', 'ignore').decode('unicode_escape'))
        self.driver.get(url.encode('ascii', 'ignore').decode('unicode_escape'))
        return(self.driver)
    
    def get_authorization(self):
        self.driver.get("""https://cdn.thingiverse.com/site/js/app.bundle.js""")
        time.sleep(3)
        ddd = self.driver.page_source
        self.authorization = 'Bearer ' + re.findall("""d=.*,f=""",re.findall("""86744.*;""",ddd)[0])[0].split(',')[0].split('"')[1]
        print(self.authorization)
    
    def close(self):
        self.driver.quit()
        
def download_files1(web_d,itemId):
    print(web_d.authorization)
    web_d.read_data_from('https://www.thingiverse.com/api/things/{}/FilesDownloadCounterIncrease?t={}'.format(itemId,int(round(time.time()*1000))))
    