# -*- encoding: utf-8 -*-
'''
@File    :   crawl_list.py
@Time    :   2024/08/03 13:56:18
@Author  :   chaopaoo12 
@Version :   1.0
@Contact :   chaopaoo12@hotmail.com
'''

# here put the import lib
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup


class web_d():

    def __init__(self,headers) -> None:
        self.headers = headers

    def get_headers(self):
        url = 'https://www.thingiverse.com/'
        self.options = webdriver.ChromeOptions()
        self.options.page_load_strategy = 'none'
        for (key,value) in self.headers.items():
            self.options.add_argument('%s="%s"' % (key, value))
        self.options.add_argument('headless')
        service = Service(executable_path='C:\\ProgramData\\anaconda3\\Scripts\\chromedriver.exe')
        driver = webdriver.Chrome(service=service,chrome_options=self.options)
        driver.get(url)
        cookies=driver.get_cookies()
        driver.quit()
        ck = dict()
        for i in cookies:
            ck[i['name']] = i['value']
        self.headers.update({"Cookie":' ;'.join([k+'='+v for (k,v) in ck.items()])})

    def get_options(self,ip_proxy=None):
        self.options = webdriver.chrome.options.Options()
        self.options.page_load_strategy = 'none'
        for (key,value) in self.headers.items():
            self.options.add_argument('%s="%s"' % (key, value))
        self.options.add_argument('--blink-settings=imagesEnabled=false')
        self.options.add_argument('headless')
        self.options.add_argument('–-disable-javascript')   #禁用javascript
        self.options.add_argument('--disable-plugins')   #禁用插件
        self.options.add_argument("--disable--gpu")#禁用显卡
        self.options.add_argument("--disable-images")#禁用图像
        self.options.add_argument("--no-sandbox")
        self.options.add_argument("--disable-dev-shm-usage")
        self.options.add_experimental_option("excludeSwitches", ["enable-automation"])
        self.options.add_experimental_option('useAutomationExtension', False)
        if ip_proxy is not None:
            self.options.add_argument(ip_proxy)

    def get_driver(self,ip_proxy=None):
        #self.get_options(ip_proxy)
        service = Service(executable_path='C:\\ProgramData\\anaconda3\\Scripts\\chromedriver.exe')
        # driver = webdriver.Chrome(service=service,options=self.options)
        # driver.get('https://www.thingiverse.com/')
        # print(driver.page_source)
        # cookies=driver.get_cookies()
        # driver.quit()
        # ck = dict()
        # for i in cookies:
        #     ck[i['name']] = i['value']
        # self.headers.update({"Cookie":' ;'.join([k+'='+v for (k,v) in ck.items()])})
        # option = self.get_options(ip_proxy)
        # print(option)
        options = webdriver.ChromeOptions()
        options.add_argument('--blink-settings=imagesEnabled=false')
        options.add_argument('headless')
        options.add_argument('–-disable-javascript')   #禁用javascript
        options.add_argument('--disable-plugins')   #禁用插件
        options.add_argument("--disable--gpu")#禁用显卡
        options.add_argument("--disable-images")#禁用图像
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        prefs = {'profile.default_content_settings.popups': 0, 'download.default_directory': 'E:\\workspace\\python\\mywork\\download'}
        options.add_experimental_option('prefs', prefs)
        self.driver = webdriver.Chrome(service=service,options=options)
        return(self.driver)
    
def get_soup(driver):
    driver.find_element(By.ID,'CybotCookiebotDialogBodyLevelButtonLevelOptinAllowAll').click()
    soup = BeautifulSoup(driver.page_source, "html.parser").body
    return(soup)

def read_data_from(driver, url):
    print('read data from:', url.encode('ascii', 'ignore').decode('unicode_escape'))
    driver.get(url.encode('ascii', 'ignore').decode('unicode_escape'))
    return(driver)

def get_nextPage(driver):
    if driver.find_element(By.XPATH,'//*[@aria-label="Next page"]').get_attribute('disabled') is True:
        return(True)
    else:
        driver.find_element(By.XPATH,'//*[@aria-label="Next page"]').click()

def get_info_listPage(html):
    docs = html.find_all(class_='item-card-container')
    return([doc.find(class_='ItemCardContent__itemCardUserLink--gMgsV').text  
            if doc.find(class_='ItemCardContent__itemCardUserLink--gMgsV') is not None else None for doc in docs],
           [doc.find(class_='ItemCardContent__itemCardUserLink--gMgsV').get('href') 
            if doc.find(class_='ItemCardContent__itemCardUserLink--gMgsV') is not None else None for doc in docs],
           [doc.find(class_='ItemCardHeader__itemCardHeader--cPULo').get('href') 
            if doc.find(class_='ItemCardHeader__itemCardHeader--cPULo') is not None else None for doc in docs],
           [doc.find(class_='ItemCardHeader__itemCardHeader--cPULo').text 
            if doc.find(class_='ItemCardHeader__itemCardHeader--cPULo') is not None else None for doc in docs],
           [doc.find(class_='ItemCardHeader__itemCardHeader--cPULo').get('href') 
            if doc.find(class_='ItemCardHeader__itemCardHeader--cPULo') is not None else None for doc in docs],
           [doc.find(class_='Image__image--MeY7Y ItemCardContent__itemCardContentImage--uzD0A').get('src') 
            if doc.find(class_='Image__image--MeY7Y ItemCardContent__itemCardContentImage--uzD0A') is not None else None for doc in docs],
           [doc.find(attrs={'aria-label':'Like'}).find(class_='ButtonCounterWrapper__buttonCounter--YXhXL') 
            if doc.find(attrs={'aria-label':'Like'}) is not None else None for doc in docs],
           [doc.find(attrs={'aria-label':'Collect Thing'}).find(class_='ButtonCounterWrapper__buttonCounter--YXhXL') 
            if doc.find(attrs={'aria-label':'Collect Thing'}) is not None else None for doc in docs],
            [doc.find(attrs={'aria-label':'Thing comments'}).find(class_='ButtonCounterWrapper__buttonCounter--YXhXL') 
            if doc.find(attrs={'aria-label':'Thing comments'}) is not None else None for doc in docs]
           )

def read_info_listPage(html):
    userName, userLink, itemLink, itemTitle, itemId, itemImg, itemLike, itemCollect, itemComments = get_info_listPage(html)
    temp = pd.DataFrame({'userName':userName,
                         'userLink':userLink,
                         'itemLink': itemLink,
                         'itemTitle': itemTitle,
                         'itemId': itemId,
                         'itemImg': itemImg,
                         'itemLike': itemLike,
                         'itemCollect': itemCollect,
                         'itemComments': itemComments
                         })
    return(temp)

def get_info_itemPage(html):
    return([html.find(class_='DetailPageTitle__thingTitleMeta--P5VUn').find('div').text, #上架日期
            ','.join([i.text for i in html.find(class_='TagList__tagList--DkseJ').find_all(class_='Button__buttonContent--AZZB4 button-content')]), #tags
            html.find(class_='License__licenseText--iIyuZ').text, #license
            html.find(class_='DetailPageTitle__thingTitleName--sGpkS').text 
            ]
           )

def read_info_itemPage(html):
    upLoadDate, Tags, license,itemTitle = get_info_listPage(html)
    #, comments, price 
    temp = pd.DataFrame({
                         'upLoadDate':upLoadDate,
                         'Tags': Tags,
                         'license': license,
                         'itemTitle':itemTitle
                         })
    return(temp)

def read_userpage(web_d, url):
    pass

def download_files(web_d, url):
    pass

def get_product_info_listpage(url, driver, next_page = True):

    driver = read_data_from(driver, url)
    print('load url success')
    html = get_soup(driver)
    print('bs4 success')
    temp = read_info_listPage(html)
    print('read html success')
    driver.quit()
    return(temp)

if __name__ == '__main__':
    url = 'https://www.thingiverse.com/?page=500&sort=newest#google_vignette'
    headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
               'Accept-Language': 'zh-CN,zh;q=0.9',
               'Cache-Control': 'max-age=0',
               'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36',
               'Connection': 'close'
               }
    driver = web_d(headers)
    driver = driver.get_driver()
    data = get_product_info_listpage(url,driver)
    driver.quit()
    print(data)