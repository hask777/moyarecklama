import requests
from bs4 import BeautifulSoup
import html5lib
import json
import pandas as pd
import os.path

url = "https://moyareklama.by/Гомель/квартиры_продажа/"
data = requests.get(url)


# with open("html/flats.html", "w", encoding="utf-8") as f:
#         f.write(data.text)

# with open("html/flats.html", 'r', encoding='utf-8') as f:
#     page = f.read()

soup = BeautifulSoup(data.text, 'lxml')
# print(soup.prettify)

items = soup.find_all('div', class_="one_advert_list")
# print(len(items))
app_dict = {}
app_arr = []

num = 0

for item in items:
    num = num + 1
    item_id = item.find('div', class_="title").find('a').get('href').replace('/single/ad/', '')
    link = item.find('div', class_="title").find('a').get('href')
    title = item.find('div', class_="title").text
    address = item.find('div', class_="address").text
    price = item.find('div', class_="price_block").text
    try:
        company_link = item.find('div', class_="company").find('a').get('href')
    except:
        continue
    company_name = item.find('div', class_="company").text
    
    app_dict ={
        'number': num,
        'id': item_id,
        'link': link,
        'title': title,
        'address': address,
        'price': price,
        'company_link': company_link,
        'company_name': company_name
    }

    app_arr.append(app_dict)

with open('json/flats.json', 'w', encoding='utf-8') as f:
    json.dump(app_arr, f, ensure_ascii = False, indent =4, sort_keys=False)


# print(app_arr)