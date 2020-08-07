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


# 樂天
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
        foundItemCount = 0
        for item in jsonData:
            foundItemCount = foundItemCount + 1
            if (str(item['brand']) == 'CSD中衛' and '口罩' in str(item['prod_name'])):
                print(str(item['prod_name']) + '\r\n' + str(item['prod_url']))
                lineNotifyMessage("fK4xZMV7HsgejH8h7dESqKshxSUqhgizPa8FiGzUJuN", str(item['prod_name']),
                                  str(item['prod_url']))
                # call Leo for debug
                lineNotifyMessage("FQdRLF5IMZFyXXuUIFPcYFnnh4Cw8CkKr9fmNcrIiol", str(item['prod_name']),
                                  str(item['prod_url']))
            else:
                print('沒找到口罩')
        lineNotifyMessage("KWzI24w8OJ6MjgcNPHT4ffvvYOLc0z4gNy5mR2o6J8N", '樂天找到'+str(foundItemCount)+'個項目, 沒有品牌符合 CSD中衛, 口罩商品',
                          'https://www.rakuten.com.tw/%E4%B8%AD%E8%A1%9B%E5%8F%A3%E7%BD%A9/')
    else:
        print('fail')


# Costco
def Costco():
    url = 'https://www.costco.com.tw/Health-Beauty/Home-Health-Care/Hygiene-Masks-First-Aid/c/70404'
    headers = {'User-Agent': 'mozilla/5.0 (Linux; Android 6.0.1; '
                             'Nexus 5x build/mtc19t applewebkit/537.36 (KHTML, like Gecko) '
                             'Chrome/51.0.2702.81 Mobile Safari/537.36'}
    # 對網頁伺服器送出請求
    resp = requests.get(url, headers=headers)
    # 檢查狀態(200:成功)
    if resp.status_code == 200:
        # result = resp.text
        # 網頁主機回應結果 放到分類器裡面
        soup = bs(resp.text, 'html.parser')
        data = soup.findAll("div", class_="product-image")

        foundItemCount = 0
        for item in data:
            foundItemCount = foundItemCount +1
            if '缺貨' in str(item.contents[1]):
                pass
            else:
                if 'CSD' in str(item.contents[1]) and '口罩' in str(item.contents[1]):
                    lineNotifyMessage('fK4xZMV7HsgejH8h7dESqKshxSUqhgizPa8FiGzUJuN',
                                      str(item.contents[1].attrs['title']),
                                      'https://www.costco.com.tw/' + str(item.contents[1].attrs['href']))
                    lineNotifyMessage('FQdRLF5IMZFyXXuUIFPcYFnnh4Cw8CkKr9fmNcrIiol',
                                      str(item.contents[1].attrs['title']),
                                      'https://www.costco.com.tw/' + str(item.contents[1].attrs['href']))
        print("Get data ok.")
        lineNotifyMessage("KWzI24w8OJ6MjgcNPHT4ffvvYOLc0z4gNy5mR2o6J8N",
                          'Costco找到' + str(foundItemCount) + '個項目, 關鍵字沒有符合 ''CSD'', ''口罩'' 的商品',
                          'https://www.costco.com.tw/Health-Beauty/Home-Health-Care/Hygiene-Masks-First-Aid/c/70404')
    else:
        print('Get data fail.')


# wastons
def wastons():
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
        foundItemCount = 0
        for item in data:
            foundItemCount = foundItemCount +1
            if (len(item.attrs['class']) == 1):
                if ('暫無存貨' not in str(item.contents[0])):
                    if ('口罩' in item.attrs['href'] and '中衛' in item.attrs['href']):
                        # benny
                        lineNotifyMessage("fK4xZMV7HsgejH8h7dESqKshxSUqhgizPa8FiGzUJuN", str(item.attrs['href']),
                                          str(item['href']))
                        # leo
                        lineNotifyMessage('FQdRLF5IMZFyXXuUIFPcYFnnh4Cw8CkKr9fmNcrIiol', str(item.attrs['href']),
                                          str(item['href']))
                        print('https://www.watsons.com.tw/' + item.attrs['href'])
                    else:
                        pass
                else:
                    pass
        lineNotifyMessage("KWzI24w8OJ6MjgcNPHT4ffvvYOLc0z4gNy5mR2o6J8N",
                          'Wastons找到' + str(foundItemCount) + '個項目, 關鍵字沒有符合 ''中衛'', ''口罩'' 的商品',
                          'https://www.watsons.com.tw/search?text=%E4%B8%AD%E8%A1%9B%E9%86%AB%E7%99%82%E5%8F%A3%E7%BD%A9')
    else:
        print('fail')

# Costco Task
def GetCostcoMaskDataTask():
    while 1 == 1:
        try:
            Costco()
            print("等待一分鐘")
            time.sleep(60)
        except Exception:
            lineNotifyMessage("KWzI24w8OJ6MjgcNPHT4ffvvYOLc0z4gNy5mR2o6J8N", 'Costco口罩資料異常',
                              'https://www.costco.com.tw/Health-Beauty/Home-Health-Care/Hygiene-Masks-First-Aid/c/70404')
            time.sleep(60)


# wastonTask
def GetWastonMaskDataTask():
    while 1 == 1:
        try:
            wastons()
            print("等待一分鐘")
            time.sleep(60)
        except Exception:
            lineNotifyMessage("KWzI24w8OJ6MjgcNPHT4ffvvYOLc0z4gNy5mR2o6J8N", 'Waston口罩資料異常',
                              'https://www.watsons.com.tw/search?text=%E4%B8%AD%E8%A1%9B%E9%86%AB%E7%99%82%E5%8F%A3%E7%BD%A9')
            time.sleep(60)


# 樂天口罩Task
def GetRakutenMaskDataTask():
    while 1 == 1:
        try:
            rakuten()
            print("等待一分鐘")
            time.sleep(60)
        except Exception:
            lineNotifyMessage("KWzI24w8OJ6MjgcNPHT4ffvvYOLc0z4gNy5mR2o6J8N", '樂天口罩資料異常',
                              'https://www.rakuten.com.tw/%E4%B8%AD%E8%A1%9B%E5%8F%A3%E7%BD%A9/')
            time.sleep(60)


# Pchome爬蟲 https://24h.m.pchome.com.tw/store/DGBJDE
# def getPcohmeData():
#     url = 'https://24h.m.pchome.com.tw/ecapi/ecshop/prodapi/v2/prod/button&id=DDYAA4K-A900AS6R6&fields=Seq,Id,Price,Qty,ButtonType,SaleStatus,Store,Group&_callback=jsonp_buttonget?_callback=jsonp_buttonget'
#     headerlist = [
#         "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36",
#         "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36 OPR/43.0.2442.991",
#         "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36 OPR/42.0.2393.94",
#         "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.78 Safari/537.36 OPR/47.0.2631.39",
#         "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36",
#         "Mozilla/5.0 (Windows NT 5.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36",
#         "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36",
#         "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0",
#         "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0",
#         "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:56.0) Gecko/20100101 Firefox/56.0",
#         "Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko"]
#     user_agent = random.choice(headerlist)
#     headers = {'User-Agent': user_agent}
#     resp = requests.get(url, headers=headers)
#     if not resp:
#         print("no data")
#         print("被封鎖了" + str(datetime.now()))
#     else:
#         resp.encoding = 'utf-8'
#         data = resp.text
#         data = data[data.index('['):data.index(']') + 1]
#         data = json.loads(data)
#         totalCount = 0
#         matchCount = 0
#         for item_obj in data:
#             totalCount = totalCount + 1
#             try:
#                 if item_obj['Qty'] > 0 and item_obj['ButtonType'] != 'NotReady':
#                     matchCount = matchCount + 1
#                     Id = item_obj['Id']
#                     url = "https://24h.pchome.com.tw/prod/" + Id
#
#                     # call Leo for debug
#                     lineNotifyMessage("yHK9SdTM9CLSOg798YVDcK5WxSdxpgYe6LOhHIr3HeE",
#                                       "$" + str(item_obj['Price']['P']) + "數量" + str(item_obj['Qty']) + "---thread0522",
#                                       url)
#
#             except Exception:
#                 print(str(datetime.now()) + "商品有庫存，處裡有庫存商品時發生例外")
#                 pass
#
#         print(str(datetime.now()) + " OK,Total " + str(totalCount) + ", Enable " + str(matchCount))


if __name__ == '__main__':
    lineNotifyMessage('fK4xZMV7HsgejH8h7dESqKshxSUqhgizPa8FiGzUJuN', 'test', 'test')
# GetWastonMaskDataTask()
# GetRakutenMaskDataTask()
