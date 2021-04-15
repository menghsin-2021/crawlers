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
    # 解決沒資料的日期
    try:
        print('crawling', date.strftime('%Y/%m/%d'))
        table = soup.find('table', class_='table_f')
        trs = table.find_all('tr')
        # 爬特定資料 product -> who -> what
        rows = trs[3:]
        # 零參數函式，當檢查的key不存在，會用零參數函式添加一個新值
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
            # 將逗點去除
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
            date_data = defaultdict(dict)
            date_data[date.strftime('%Y/%m/%d')] = data
            # print(date_data)
        return date, date_data

    except AttributeError:
        print('{}沒資料'.format(date.strftime('%Y/%m/%d')))
        return date, 'None'  # 要 return 東西 如果為 None 沒辦法 call 出來
       

# 建立 download 資料夾
os.makedirs('downloads', exist_ok=True)
# 將日期設為今日
date = datetime.today()
# 存成 date_list
date_list = date_list(date)
if __name__ == "__main__":
    start = time.time()
    with ThreadPoolExecutor(max_workers=5) as executor:
        date_datas = executor.map(crawl, date_list)
        for date_data in date_datas:
            date = date_data[0]
            date_data = date_data[1]  # 要 return 東西 如果為 None 沒辦法 call 出來
            try: 
                print('{}臺股期貨外資未平倉淨口數：{}'.format(date.strftime('%Y/%m/%d'), date_data[date.strftime('%Y/%m/%d')]['臺股期貨']['外資']['未平倉淨口數']))
            except TypeError:
                print('{}沒資料'.format(date.strftime('%Y/%m/%d')))    
            # 存成json檔
            path_name = os.path.join('./downloads/', '{}.json'.format(str(date.strftime('%Y-%m-%d'))))
            with open(path_name, 'w') as f:
                jsonStr = json.dumps(date_data, ensure_ascii=False, indent=5)
                jsonStr = json.loads(jsonStr)
                json.dump(jsonStr, f)
    end = time.time()            
    print(f'下載這些資料共花了 {end - start} 秒')  #下載這些資料共花了 233.09515166282654 秒
                    # pprint(jsonStr)  # check 用

        
    
    # json 存檔說明
    # ensure_ascii，默認True, 如果dict內含有non-ASCII的中文字符，則會類似\uXXXX的顯示數據，設置成False後，就能正常顯示
    # encoding，默認是UTF-8,用來設置生成的json數據的編碼方式
    # .dumps .loads 兩者在 python 當中處理字串轉換
    # .dump .load 兩者在 python 當中處理檔案轉換

    


