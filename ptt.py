# 學習 find_all / find / .text / .get / CSS selector ex. span.listTitle / p a

import requests
from bs4 import BeautifulSoup 

root_url = 'https://disp.cc/b/'

r = requests.get('https://disp.cc/b/PttHot')   
soup = BeautifulSoup(r.text, 'html.parser')
# spans = soup.find_all('span', class_='listTitle')
# for span in spans:
#     href = span.find('a').get('href')  # print(span.find('a')['href'])  # 也可以這樣寫
#     if href == '796-59l9':
#         break

#     else:
#         url = root_url + href
#         title = span.text
#         print(f'{title}\n{url}')
    
'''
-----------------------------------------
'''

# CSS selector

for span in soup.select('div#list span.listTitle.L34.nowrap'):
    # div tag  裡面的所有 span tag 然後要吻合 listTitle/L34/nowrap class
    # #list 代表 id = list (直接寫 id 就不用寫 tag)
    # .listTitle 代表 class = listTitle
    # .select('p a')兩種東西用空格分開 (這個p裡面的這種a東西)
    href = span.find('a').get('href')  # print(span.find('a')['href'])  # 也可以這樣寫
    if href == '796-59l9':
        break

    else:
        url = root_url + href
        title = span.text
        print(f'{title}\n{url}')
    





# print([s.text for s in spans])
# p a — 所有在 p tag 裡的  a tag
# body p a — 所有在 body tag 裡的 p tag 裡的 a tag
# p.outer-text — 所有有outer-text這個class 的 p tag
# p#first — 所有有 first 這個 id 的 p tag