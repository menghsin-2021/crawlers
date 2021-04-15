import os
import json
from pprint import pprint
from dateutil.parser import parse 
from datetime import datetime, timedelta
from matplotlib import pyplot as plt


def start_date():
    start_year = input('請輸入起始西元年: ')
    start_month = input('請輸入起始月: ')
    start_day = input('請輸入起始日: ')
    start_date = parse(f'{start_month}-{start_day}-{start_year}') # 2021-04-12
    # print(date) #> 2021-04-12 00:00:00
    return start_date


def end_date():
    end_year = input('請輸入結束西元年: ')
    end_month = input('請輸入結束月: ')
    end_day = input('請輸入結束日: ')
    end_date = parse(f'{end_month}-{end_day}-{end_year}')
    return end_date


def get_data(start_date, end_date):
    delta = timedelta(days=1)
    date_duration = []
    future_numbers = []
    while start_date >= end_date:
        file_name = str(start_date.strftime('%Y-%m-%d'))
        file = os.path.join('./downloads/', '{}.json'.format(file_name))
        with open(file, 'r') as obj:
            data = json.load(obj)
        try:
            future_number = data[str(start_date.strftime('%Y/%m/%d'))]['臺股期貨']['外資']['未平倉淨口數']
            pprint(future_number)
            date_duration.append(start_date.strftime('%Y/%m/%d'))
            future_numbers.append(future_number)
            start_date -= delta
        except:
            print('none')
            start_date -= delta
            continue
    return date_duration, future_numbers


def plot(date_duration, future_numbers):
    
    # 設定圖片大小
    fig = plt.figure(figsize=(40,10),dpi=400,linewidth = 0.6)
    # 建立折線圖，x軸 年分, Y軸 臺股期貨外資未平倉淨口數
    plt.plot(date_duration, future_numbers, color='green', marker='o', linestyle='solid')
    # 加個標題
    plt.title('future numbers/years')
    # 在Y軸加標簽
    plt.ylabel('future numbers')
    # 在X軸加標簽
    plt.xlabel('years')
    # 旋轉x軸標籤
    plt.xticks(rotation=90)
    # x軸刻度設定字體大小
    plt.xticks(fontsize=8)
    # y軸刻度設定字體大小
    plt.yticks(fontsize=8)
#     plt.show
    fig.savefig('future.pdf')

if __name__ == "__main__":
    start_date = start_date()
    end_date = end_date()
    date_duration, future_numbers = get_data(start_date, end_date)
    print(date_duration)
    print(future_numbers)
    plot(date_duration, future_numbers)



