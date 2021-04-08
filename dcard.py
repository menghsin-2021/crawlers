import time
from concurrent.futures import ThreadPoolExecutor
import requests
from bs4 import BeautifulSoup



DCARD_PAGE = 'https://www.dcard.tw/f/youtuber/p/235712393/'

def get_url(url):
    craw = requests.get(url)
    soup = BeautifulSoup(craw.text, 'html.parser')
    return soup

def get_response_count(url):
    soup = get_url(url)
    res = soup.find('div', class_='fiw2dr-2 dlNVms')
    res_count = int(res.text.split()[1])
    return res_count

def get_url_list(res_count):
    url_list = []
    for i in range(res_count):
        url = f'{DCARD_PAGE}b/{i}'
        # print(url)
        url_list.append(url)
    return url_list

def get_data(res_count):
    data = {}
    url_list = get_url_list(res_count)
    
    with ThreadPoolExecutor(max_workers=5) as executor:
        soups = executor.map(get_url, url_list)
        i = 0
        for soup in soups:
            i += 1
            name = soup.find('div', class_='sc-7fxob4-4 dbFiwE').text
            comment = soup.find('div', class_='phqjxq-0 fQNVmg').text.strip()
            if name in data:
                data[name].append(comment)
            else:
                data[name] = [comment]
            print(f'已裝入{i}筆留言')
    return data
  

if __name__ == "__main__":
    start = time.time()

    res_count = get_response_count(DCARD_PAGE)
    data = get_data(res_count)
    
    end = time.time()
    
    data_ordered = sorted(data.items(), key=lambda x: len(x[1]), reverse=True)
    for d in data_ordered:
        print(f'{d[0]} 總留言數{len(d[1])}')
    
    print(f'一共有{res_count}筆留言')
    print(f'裝這些資料共花了 {end - start} 秒')
