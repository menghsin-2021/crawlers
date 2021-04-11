import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

import pandas as pd

'''
把 POST 用 form 給伺服器指令的資料 用問號 接在網址後面 轉成 get 再 request
'''

def crawl(date):
    r = requests.get('https://www.taifex.com.tw/cht/3/futContractsDate?queryType=1&goDay=&doQuery=1&dateaddcnt=&queryDate={}%2F{}%2F{}&commodityId='.format(date.year, date.month, date.day))
    if r.status_code == requests.codes.ok:
        soup = BeautifulSoup(r.text, 'html.parser') 
        # 可換成 lxml  #html.parser
        # print(soup.prettify()) # 檢查整個程式碼
        # print(soup.text) # 檢查整個程式碼
        # print('successfully get data from', date)
    
    try:
        table = soup.find('table', class_='table_f')
        trs = table.find_all('tr')
    except AttributeError:
        print(f'{date}沒資料')
        return

    rows = trs[3:]
    for row in rows:
        tds = row.find_all('td')
        cells = [td.text.strip() for td in tds]
        if cells[0] == '期貨小計':
            break
        if len(cells) == 15:
            product = cells[1]
            data = cells[1:]
        else: 
            data = [product] + cells
        print(data)
        
        converted = [int(d.replace(',','')) for d in data[2:]]

        print(data[:2] + converted)
        

        

        # if cells[0] == '期貨小計':
        #     break

        






date = datetime.today()
while True:
    crawl(date)
    date = date - timedelta(days=1)
    if date <= datetime.today() - timedelta(days=5):
        break
    


#     tables = soup.find_all('table', attrs={'cellpadding':'2'})  #  attrs = Attributes 決定屬性
#     # print(tables[0].text)
#     for table in tables:
#         trs = table.find_all('tr')
#         for tr in trs:
#             date, value, price = [td.text for td in tr.find_all('td')]
#             if date == '日期':
#                 title = []
#                 title.append([date, value, price])
#             else:
#                 data.append([date, value, price])

# df = pd.DataFrame(data, columns=title)
# # df.to_csv('big_eight.csv')
# # df.to_excel('big_eight.xlsx')
# df.to_html('big_eight.html')
# # print(data)



