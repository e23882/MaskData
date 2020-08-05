import urllib.parse
import requests
import time
import json
import os
from bs4 import BeautifulSoup as bs
import datetime
from datetime import datetime, timedelta
import random


# LineNotify相關
def lineNotifyMessage(token, msg, url):
    headers = {
        "Authorization": "Bearer " + token,
        "Content-Type": "application/x-www-form-urlencoded"
    }

    payload = {'message': msg + "\r\n" + url}
    r = requests.post("https://notify-api.line.me/api/notify", headers=headers, params=payload)
    return r.status_code

def rakuten():
    url = 'https://www.rakuten.com.tw/%E4%B8%AD%E8%A1%9B%E5%8F%A3%E7%BD%A9/'
    headerlist = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36 OPR/43.0.2442.991",
        "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36 OPR/42.0.2393.94",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.78 Safari/537.36 OPR/47.0.2631.39",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36",
        "Mozilla/5.0 (Windows NT 5.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0",
        "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0",
        "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:56.0) Gecko/20100101 Firefox/56.0",
        "Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko"]
    user_agent = random.choice(headerlist)
    headers = {'User-Agent': user_agent}
    resp = requests.get(url, headers=headers)
    if resp.status_code == 200:
        result = resp.text
        startIndex = result.index('page_products')
        endIndex = result.index('page_cat')
        tempData = result[startIndex:endIndex]
        data = tempData[tempData.index('['):tempData.index(']') + 1]
        jsonData = json.loads(data)
        for item in jsonData:
            if (str(item['brand']) == 'CSD中衛' and '口罩' in str(item['prod_name'])):
                print(str(item['prod_name']) + '\r\n' + str(item['prod_url']))
                lineNotifyMessage("FQdRLF5IMZFyXXuUIFPcYFnnh4Cw8CkKr9fmNcrIiol", str(item['prod_name']), str(item['prod_url']))
                # call Leo for debug
                lineNotifyMessage("yHK9SdTM9CLSOg798YVDcK5WxSdxpgYe6LOhHIr3HeE", str(item['prod_name']), str(item['prod_url']))
            else:
                print('沒找到口罩')
    else:
        print('fail')

def rakutenWithRule():
    url = 'https://www.rakuten.com.tw/shop/amart/category/ea07a00/?l-id=tw_product_breadcrumbs_5'
    headerlist = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36 OPR/43.0.2442.991",
        "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36 OPR/42.0.2393.94",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.78 Safari/537.36 OPR/47.0.2631.39",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36",
        "Mozilla/5.0 (Windows NT 5.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0",
        "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0",
        "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:56.0) Gecko/20100101 Firefox/56.0",
        "Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko"]
    user_agent = random.choice(headerlist)
    headers = {'User-Agent': user_agent}
    resp = requests.get(url, headers=headers)
    if resp.status_code == 200:
        result = resp.text
        print("ok")
    else:
        print('fail')

def costco():
    url = 'https://www.costco.com.tw/Health-Beauty/Home-Health-Care/Hygiene-Masks-First-Aid/c/70404'
    headerlist = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36 OPR/43.0.2442.991",
        "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36 OPR/42.0.2393.94",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.78 Safari/537.36 OPR/47.0.2631.39",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36",
        "Mozilla/5.0 (Windows NT 5.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0",
        "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0",
        "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:56.0) Gecko/20100101 Firefox/56.0",
        "Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko"]
    user_agent = random.choice(headerlist)
    headers = {'User-Agent': user_agent}
    resp = requests.get(url, headers=headers)
    if resp.status_code == 200:
        result = resp.text
        print("ok")
    else:
        print('fail')

# 檢查曲程式有沒有賣口罩
def wastons():
    # url= 'https://www.watsons.com.tw/search?text=%E4%B8%AD%E8%A1%9B%E9%86%AB%E7%99%82%E5%8F%A3%E7%BD%A9'
    url = 'https://www.watsons.com.tw/search?text=%E4%B8%AD%E8%A1%9B%E9%86%AB%E7%99%82%E5%8F%A3%E7%BD%A9'
    headerlist = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36 OPR/43.0.2442.991",
        "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36 OPR/42.0.2393.94",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.78 Safari/537.36 OPR/47.0.2631.39",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36",
        "Mozilla/5.0 (Windows NT 5.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0",
        "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0",
        "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:56.0) Gecko/20100101 Firefox/56.0",
        "Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko"]
    resp = requests.get(url)
    if resp.status_code == 200:
        soup = bs(resp.text, 'html.parser')
        data = soup.findAll("a", class_="gtmAlink")
        for item in data:
            if (len(item.attrs['class']) == 1):
                if ('暫無存貨' not in str(item.contents[0])):
                    if ('口罩' in item.attrs['href'] and '中衛' in item.attrs['href']):
                        lineNotifyMessage("FQdRLF5IMZFyXXuUIFPcYFnnh4Cw8CkKr9fmNcrIiol", str(item.attrs['href']), str(item['href']))
                        # call Leo for debug
                        lineNotifyMessage("yHK9SdTM9CLSOg798YVDcK5WxSdxpgYe6LOhHIr3HeE", str(item['href']), str(item['href']))
                        print('https://www.watsons.com.tw/' + item.attrs['href'])
                    else:
                        pass
                else:
                    pass
    else:
        print('fail')
def GetWastonMaskDataTask():
    while 1 == 1:
        try:
            wastons()
            print("等待一分鐘")
            time.sleep(60)
        except Exception:
            lineNotifyMessage("KWzI24w8OJ6MjgcNPHT4ffvvYOLc0z4gNy5mR2o6J8N", '口罩資料異常')
            time.sleep(60)

#樂天口罩Task
def GetRakutenMaskDataTask():
    while 1 == 1:
        try:
            rakuten()
            print("等待一分鐘")
            time.sleep(60)
        except Exception:
            lineNotifyMessage("KWzI24w8OJ6MjgcNPHT4ffvvYOLc0z4gNy5mR2o6J8N", '口罩資料異常')
            time.sleep(60)


if __name__ == '__main__':
    GetWastonMaskDataTask()
    # GetRakutenMaskDataTask()

