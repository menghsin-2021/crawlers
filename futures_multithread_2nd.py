import os
import time
from concurrent.futures import ThreadPoolExecutor
import json
from collections import defaultdict
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from pprint import pprint

import pandas as pd

'''
把 POST 用 form 給伺服器指令的資料 用問號 接在網址後面 轉成 get 再 request
'''

def date_list(date):
    date_list = [date]
    while True:    # 限定爬取天數
        date = date - timedelta(days=1)
        if date <= datetime.today() - timedelta(days=730):
            break
        date_list.append(date)
    return date_list
            # pprint('2021/04/13臺股期貨外資未平倉淨口數：' + str(date_data['2021/04/13']['臺股期貨']['外資']['未平倉淨口數']))
            # check 用

def crawl(date):
    
    r = requests.get('https://www.taifex.com.tw/cht/3/futContractsDate?queryType=1&goDay=&doQuery=1&dateaddcnt=&queryDate={}%2F{}%2F{}&commodityId='.format(date.year, date.month, date.day))
    if r.status_code == requests.codes.ok:
        soup = BeautifulSoup(r.text, 'html.parser')
    return soup, date 
                    # print(soup.prettify()) # 檢查整個程式碼

def crawl_data(soup, date):    
    # 解決沒資料的日期
    try:
        print('crawling', date.strftime('%Y/%m/%d'))
        table = soup.find('table', class_='table_f')
        trs = table.find_all('tr')
           
    # 爬特定資料 product -> who -> what
        rows = trs[3:]
        data = defaultdict(dict)
        for row in rows:
            tds = row.find_all('td')
            cells = [td.text.strip() for td in tds]
            if cells[0] == '期貨小計':
                break
            if len(cells) == 15:
                product = cells[1]
                row_data = cells[1:]
            else: 
                row_data = [product] + cells
                            # print(data)  #check 用       
            converted = [int(d.replace(',','')) for d in row_data[2:]]
            row_data = row_data[:2] + converted
                            # print(row_data)  #check 用       
            headers = ['商品', '身份別', '交易多方口數', '交易多方金額', '交易空方口數', '交易空方金額', '交易多空淨口數', '交易多空淨額',
                       '未平倉多方口數', '未平倉多方金額', '未平倉空方口數', '未平倉空方金額', '未平倉淨口數', '未平倉多空淨額']
            # product -> who -> what
            product = row_data[0]
            who = row_data[1]
            data[product][who] = {headers[i]: row_data[i] for i in range(2, len(headers))}
                            # pprint(data)
                            # data = {row_data[0]: row_data[1:] for row}
        return data

    except AttributeError:
        print('{}沒資料'.format(date.strftime('%Y/%m/%d')))

        
# 建立 download 資料夾
os.makedirs('downloads', exist_ok=True)

# 將日期設為今日
date = datetime.today()
# main()
date_list = date_list(date)
if __name__ == "__main__":
    start = time.time()
    with ThreadPoolExecutor(max_workers=5) as executor:
        soups = executor.map(crawl, date_list)
        for soup_date in soups:
            # 建立字典
            date_data = defaultdict(dict)
            data = crawl_data(soup_date[0], soup_date[1])
            date = soup_date[1]
            # print(date, data)
            date_data[date.strftime('%Y/%m/%d')] = data
            try: 
                print('{}臺股期貨外資未平倉淨口數：{}'.format(date.strftime('%Y/%m/%d'), date_data[date.strftime('%Y/%m/%d')]['臺股期貨']['外資']['未平倉淨口數']))
            except TypeError:
                print('{}沒資料'.format(date.strftime('%Y/%m/%d')))    
            # 存成json檔
            path_name = os.path.join('./downloads/', '{}.json'.format(str(date.strftime('%Y-%m-%d'))))
            with open(path_name, 'w', encoding='utf-8') as f:
                jsonStr = json.dumps(date_data, ensure_ascii=False, indent=5)
                json.dump(jsonStr, f)
                # pprint(jsonStr)  # check 用
    end = time.time()            
    print(f'下載這些資料共花了 {end - start} 秒')  # 下載這些資料共花了 217.32458519935608 秒 
                
    
    # json 存檔說明
    # Ensure_ascii，默認True, 如果dict內含有non-ASCII的中文字符，則會類似\uXXXX的顯示數據，設置成False後，就能正常顯示
    # encoding，默認是UTF-8,用來設置生成的json數據的編碼方式
    # 原文網址：https://kknews.cc/code/9omly2q.html
    


