import requests
import time
from bs4 import BeautifulSoup
import re
import random
# from selenium import webdriver       #開網頁用
import pandas as pd
import pygsheets                     #Google sheets上傳用

#延遲幾秒再爬網頁
time.sleep(1)

#表特版網址
url = "https://www.ptt.cc/bbs/Beauty/index.html"

#agent
useragent={
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36"
}

#Google sheets憑證
gc = pygsheets.authorize(service_file='你的Google sheets憑證')

#開啟表特版首頁
response = requests.get(url)
soup = BeautifulSoup(response.text,"lxml")

#選取上一頁
items = soup.select(".btn-group-paging a:nth-of-type(2)")

#全域變數image_list，用來裝所有的網址
image_list = []

#取得表特版倒數第二頁網址，
for item in items:
    page_url = item.get("href")
match = re.search(r"[0-9]+",page_url)
a = int(match.group())
#從倒數第四頁開始跑迴圈三次，取得倒數四至二頁的網址
for i in range (a-2,a+1):
    url_new =  "https://www.ptt.cc/bbs/Beauty/index" + str(i) + ".html"
    response = requests.get(url_new)
    soup = BeautifulSoup(response.text,"lxml")
    print(url_new)
# print(soup.prettify())

    #選取所有黃標的標題(class = f3)
    # items_2 = soup.select(".f3")
    # url_list = []
    # for item_2 in items_2:
    #     url_list = url_list + [item_2.parent.parent.find('a').get("href")]

    #選取所有標記[正妹]的標題(text=re.compile("[正妹]"))
    items_2 = soup.find_all("a",text=re.compile("[正妹]"))
    # print(items_2)
    url_list = []
    for item_2 in items_2:
        url_list = url_list + [item_2.parent.parent.find('a').get("href")]

    #開啟全部黃標標題

    for url_1 in url_list:
        url_2 =  "https://www.ptt.cc" + (url_1) 
        response = requests.get(url_2)
        soup = BeautifulSoup(response.text,"lxml")

        #讀取網頁中開頭是「https」且副檔名是「jpg」的網址並加入list
        #使用正則表達式「不匹配」刷掉3個無法由LINE傳出的網址https://ilarge，https://imgur，https://iv1
        soup_https =soup.find_all("a",{"href":re.compile('^(?!.*https://ilarge)''^(?!.*https://imgur)''^(?!.*https://iv1)''^https''.*?\.jpg')})
        # soup_https =soup_jpg.find_all("a",{"href":re.compile('^https')})
        #讀取網頁中網址開頭是「https://i」的網址並加入list
        # soup_https =soup.find_all("a",{"href":re.compile('^https://i')})
        for element in soup_https:
            image_list = image_list + [[len(image_list),element.string]]
            # print(image_list)
            print(len(image_list))

# image_Series = pd.Series(image_list)
# print(image_Series)

# #open the google spreadsheet (where 'Ptt beauty' is the name of my sheet)
# sh = gc.open('Ptt beauty')

# #select the first sheet 
# wks = sh[0]

# #update the first sheet with df, starting at cell B2. 
# wks.set_dataframe(image_Series,(1,1))



#將取出的網址轉成DataFrame檔案
name=['Number','Website']
image_dataframe=pd.DataFrame(columns=name,data=image_list)
# image_dataframe=pd.DataFrame(image_list)
print(image_dataframe)

#儲存DataFrame檔案成.csv檔
# image_dataframe.to_csv('./image_dataframe.csv',encoding='utf-8')

#隨機抽出list中的一個網址並回傳
print(len(image_list))
image_show = random.choice(image_list)
print(image_show)

#用Chrome瀏覽器開啟圖片
# driver = webdriver.Chrome()
# driver.get(image_show[1])


#open the google spreadsheet (where 'Ptt beauty' is the name of my sheet)
sh = gc.open('Ptt beauty')

#select the first sheet 
wks = sh[0]

#update the first sheet with df, starting at cell B2. 
wks.set_dataframe(image_dataframe,(1,1))


print("down")