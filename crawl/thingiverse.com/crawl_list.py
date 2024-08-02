import pandas as pd
from selenium import webdriver
import requests
import json
import datetime
import time
from bs4 import BeautifulSoup

class web_d():

    def __init__(self,headers) -> None:
        self.headers = headers

    def get_headers(self):
        url = 'https://www.thingiverse.com/'
        self.options = webdriver.ChromeOptions()
        for (key,value) in self.headers.items():
            self.options.add_argument('%s="%s"' % (key, value))
        self.options.add_argument('headless')
        driver = webdriver.Chrome(chrome_options=self.options)
        driver.get(url)
        cookies=driver.get_cookies()
        driver.quit()
        ck = dict()
        for i in cookies:
            ck[i['name']] = i['value']
        self.headers.update({"Cookie":' ;'.join([k+'='+v for (k,v) in ck.items()])})

    def get_options(self,ip_proxy=None):
        self.options = webdriver.chrome.options.Options()
        for (key,value) in self.headers.items():
            self.options.add_argument('%s="%s"' % (key, value))
        self.options.add_argument('headless')
        self.options.add_argument("--no-sandbox")
        self.options.add_argument('--disable-gpu')
        self.options.add_argument("--disable-dev-shm-usage")
        self.options.add_experimental_option("excludeSwitches", ["enable-automation"])
        self.options.add_experimental_option('useAutomationExtension', False)
        if ip_proxy is not None:
            self.options.add_argument(ip_proxy)

    def get_driver(self,ip_proxy=None):
        self.get_options(ip_proxy)
        driver = webdriver.Chrome(options=self.options)
        driver.get('https://www.thingiverse.com/')
        cookies=driver.get_cookies()
        driver.quit()
        ck = dict()
        for i in cookies:
            ck[i['name']] = i['value']

        self.headers.update({"Cookie":' ;'.join([k+'='+v for (k,v) in ck.items()])})
        option = self.get_options(ip_proxy)
        self.driver = webdriver.Chrome(options=option)
        return(self.driver)

    
def get_soup(driver):
    soup = BeautifulSoup(driver.page_source, "html.parser").body
    #k = 1
    #while soup is None or soup.text == 'Request was throttled. Please wait a moment and refresh the page':
    #    print('get soup {} times.'.format(k))
    #    k += 1
    #    driver.refresh()
    #    time.sleep(3)
    #    soup = BeautifulSoup(driver.page_source, "html.parser").body
    return(soup)

def read_data_from(driver, url):
    print('read data from:', url.encode('ascii', 'ignore').decode('unicode_escape'))
    driver.get(url.encode('ascii', 'ignore').decode('unicode_escape'))
    # if url is not None:
    #     try:
    #         driver.get(url.encode('ascii', 'ignore').decode('unicode_escape'))
    #         #element = EC.url_changes(url)
    #         #try:
    #         #    WebDriverWait(driver, 5).until(element)
    #         #    flag1 = element(driver)
    #         #except:
    #         #    flag1 = element(driver)

    #         #if flag1
    #         #driver.implicitly_wait(10)
    #     except:
    #         print(url)
    return(driver)

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
            if doc.find(class_='ItemCardHeader__itemCardHeader--cPULo') is not None else None for doc in docs]
           #[doc.find(class_='ItemCardHeader__itemCardHeader--cPULo').get('href') for doc in docs],
           #[doc.find('div',{'class':['_cDEzb_p13n-sc-css-line-clamp-3_g3dy1',
           #                         '_cDEzb_p13n-sc-css-line-clamp-4_2q2cc']}).text if doc.find('div',{'class':['_cDEzb_p13n-sc-css-line-clamp-3_g3dy1','_cDEzb_p13n-sc-css-line-clamp-4_2q2cc']}) is not None else None for doc in docs],
           #[doc.find(attrs={'class':'a-link-normal','tabindex':'-1'}).get('href') if doc.find(attrs={'class':'a-link-normal','tabindex':'-1'}) is not None else None for doc in docs],
           #[doc.find(class_='p13n-sc-uncoverable-faceout').get('id') if doc.find(class_='p13n-sc-uncoverable-faceout') is not None else None for doc in docs],
           #[doc.find(class_='a-icon-alt').text.replace(' out of 5 stars','') if doc.find(class_='a-icon-alt') is not None else None for doc in docs],
           #[doc.find(class_='a-size-small').text.replace(',','') if doc.find(class_='a-size-small') is not None else 0 for doc in docs],
           #[doc.find(class_='a-size-base').text.replace('$','').replace('\xa0','') if doc.find(class_='a-size-base') is not None else 0 for doc in docs]
           )

def read_info_listPage(html):
    username, userlink, itemlink, itemtitle, itemid = get_info_listPage(html)
    #, comments, price 
    temp = pd.DataFrame({'username':username,
                         'userlink':userlink,
                         'itemlink': itemlink,
                         'itemtitle': itemtitle,
                         'itemid': itemid
                         #'itemjpg': href,
                         #'itemlike': star,
                         #'itemcollect': comments,
                         #'itemcomments': price
                         })
    return(temp)


def get_info_itemPage(html):
    docs = html.find_all(class_='DetailPageTitle__thingTitleMeta--P5VUn') #上架日期

    docs = html.find_all(class_='TagList__tagList--DkseJ').find_all(class_='Button__buttonContent--AZZB4 button-content').text #tags

    docs = html.find_all(class_='License__licenseText--iIyuZ').find_all(class_='Button__buttonContent--AZZB4 button-content') #license
    pass

    #return([doc.find(class_='ItemCardContent__itemCardUserLink--gMgsV').text for doc in docs],
    #       [doc.find(class_='ItemCardContent__itemCardUserLink--gMgsV').get('href') for doc in docs],
    #       [doc.find(class_='ItemCardHeader__itemCardHeader--cPULo').get('href') for doc in docs],
    #       [doc.find(class_='ItemCardHeader__itemCardHeader--cPULo').text for doc in docs],
    #       [doc.find(class_='ItemCardHeader__itemCardHeader--cPULo').get('href') for doc in docs]
           #[doc.find(class_='ItemCardHeader__itemCardHeader--cPULo').get('href') for doc in docs],
           #[doc.find('div',{'class':['_cDEzb_p13n-sc-css-line-clamp-3_g3dy1',
           #                         '_cDEzb_p13n-sc-css-line-clamp-4_2q2cc']}).text if doc.find('div',{'class':['_cDEzb_p13n-sc-css-line-clamp-3_g3dy1','_cDEzb_p13n-sc-css-line-clamp-4_2q2cc']}) is not None else None for doc in docs],
           #[doc.find(attrs={'class':'a-link-normal','tabindex':'-1'}).get('href') if doc.find(attrs={'class':'a-link-normal','tabindex':'-1'}) is not None else None for doc in docs],
           #[doc.find(class_='p13n-sc-uncoverable-faceout').get('id') if doc.find(class_='p13n-sc-uncoverable-faceout') is not None else None for doc in docs],
           #[doc.find(class_='a-icon-alt').text.replace(' out of 5 stars','') if doc.find(class_='a-icon-alt') is not None else None for doc in docs],
           #[doc.find(class_='a-size-small').text.replace(',','') if doc.find(class_='a-size-small') is not None else 0 for doc in docs],
           #[doc.find(class_='a-size-base').text.replace('$','').replace('\xa0','') if doc.find(class_='a-size-base') is not None else 0 for doc in docs]
    #       )

def read_info_itemPage(html):
    username, userlink, itemlink, itemtitle, itemid = get_info_listPage(html)
    #, comments, price 
    temp = pd.DataFrame({'username':username,
                         'userlink':userlink,
                         'itemlink': itemlink,
                         'itemtitle': itemtitle,
                         'itemid': itemid
                         #'itemjpg': href,
                         #'itemlike': star,
                         #'itemcollect': comments,
                         #'itemcomments': price
                         })
    return(temp)


def read_userpage(web_d, url):
    pass

def download_files(web_d, url):
    pass


def get_product_info_listpage(url, driver):

    driver = read_data_from(driver, url)
    print('load url success')
    html = get_soup(driver)
    print('bs4 success')
    temp = read_info_listPage(html)
    print('read html success')
    driver.quit()
    return(temp)


if __name__ == '__main__':
    url = 'https://www.thingiverse.com/?page=1&sort=newest'
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