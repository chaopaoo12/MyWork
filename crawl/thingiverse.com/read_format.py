# -*- encoding: utf-8 -*-
'''
@File    :   read_format.py
@Time    :   2024/08/03 10:29:01
@Author  :   chaopaoo12 
@Version :   1.0
@Contact :   chaopaoo12@hotmail.com
'''

# here put the import lib
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time

    
def get_soup(driver):
    WebDriverWait(driver,60).until(EC.presence_of_element_located((By.CLASS_NAME,'ItemCardContent__itemCardLinkFiller--uj5HM'))) 
    try:
        driver.find_element(By.ID,'CybotCookiebotDialogBodyLevelButtonLevelOptinAllowAll').click()
    except:
        pass
    soup = BeautifulSoup(driver.page_source, "html.parser").body
    return(soup)

def get_nextPage(driver):
    try:
        if driver.find_element(By.XPATH,'//*[@aria-label="Next page"]').get_attribute('disabled') == 'true':
            return(True)
        else:
            driver.find_element(By.XPATH,'//*[@aria-label="Next page"]').click()
            return(False)
    except:
        return(True)

def download_files(driver):
    if len(driver.find_elements(By.XPATH,'//*[@aria-label="Open download modal"]')) != 0:
        driver.find_element(By.XPATH,'//*[@aria-label="Open download modal"]').click()
    int(round(time.time()*1000))

def check_success(driver):
    while driver.find_element(By.CLASS_NAME,'Modal__modalTitle--Sk0ox').text != 'Downloading...':
        print('wait',int(driver.find_element(By.CLASS_NAME,'Modal__modalTitle--Sk0ox').text.split(' ')[-1])+35)
        time.sleep(int(driver.find_element(By.CLASS_NAME,'Modal__modalTitle--Sk0ox').text.split(' ')[-1])+35)
        
def cancel_modal(driver):
    if len(driver.find_elements(By.XPATH,'//*[@aria-label="Close modal"]')) != 0:
        driver.find_element(By.XPATH,'//*[@aria-label="Close modal"]').click()

def get_listPage(html):
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

def read_listPage(html):
    userName, userLink, itemLink, itemTitle, itemId, itemImg, itemLike, itemCollect, itemComments = get_listPage(html)
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
    temp = temp.dropna(axis=0,subset=['itemLink'])
    temp['itemId'] = temp['itemId'].apply(lambda x:str(x).split(':')[-1])
    temp['itemLink'] = temp['itemLink'].apply(lambda x:'https://www.thingiverse.com'+str(x))
    return(temp)

def get_itemPage(html):
    if html.find(class_='TagList__tagList--DkseJ') is None:
        Tags = None 
    else:
        Tags = ','.join([i.text for i in html.find(class_='TagList__tagList--DkseJ').find_all(class_='Button__buttonContent--AZZB4 button-content')])
    upLoadDate = html.find(class_='DetailPageTitle__thingTitleMeta--P5VUn').find('div').text
    license = html.find(class_='License__licenseText--iIyuZ').text
    licenseLink = html.find(class_='License__licenseText--iIyuZ').find_all('a')[2].get('href')
    itemTitle = html.find(class_='DetailPageTitle__thingTitleName--sGpkS').text
    itemId = html.find(class_='License__licenseText--iIyuZ').find_all('a')[0].get('href').split(':')[-1]
    
    return([upLoadDate, Tags, license,licenseLink, itemTitle, itemId])

def read_itemPage(html):
    upLoadDate, Tags, license,licenseLink, itemTitle, itemId = get_itemPage(html)
    temp = pd.DataFrame({
                         'upLoadDate':upLoadDate,
                         'Tags': Tags,
                         'license': license,
                         'licenseLink': licenseLink,
                         'itemTitle':itemTitle,
                         'itemId':itemId
                         },index=[0])
    return(temp)