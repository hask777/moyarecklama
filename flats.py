import requests
from bs4 import BeautifulSoup
import html5lib
import json
import pandas as pd
import os.path

url = "https://moyareklama.by/Гомель/квартиры_продажа/"
page = requests.get(url)
page = page.text

# path = os.path.exists('html/flats.html')

# if path != True:
#     with open("html/flats.html", "w", encoding="utf-8") as f:
#         f.write(page)
# else:
#     print("this file allready exists!")

# with open("html/flats.html", 'r', encoding='utf-8') as f:
#     page = f.read()
# print(data)

soup = BeautifulSoup(page, 'html5lib')
items = soup.find_all('div', class_="one_advert_list")

main_url = 'https://www.moyareklama.by/'

app_dict = {}
app_arr = []

for item in items:
    try:
        item_id = item.find('div', class_='block-for-slider').get('rel')
    except:
        continue
    
    try:
        title = item.find('div', class_='title').text
    except:
        continue

    try:
        # single_link = item.find('a', class_="premium").get('href')
        single_link = item.find_all('a')[0].get('href')
    except:
        # single_link = item.find_all('a')[0].get('href')
        continue

    try:
        address = item.find('div', class_='address').text
    except:
        continue

    try:
        price = item.find('div', class_='price').text
    except:
        continue

    try:
        price_info = item.find('div', class_='price_info').text
    except:
        continue

    try:
        company_link = item.find('a', class_='realty_link').get('href')
    except:
        continue

    try:
        company_name = item.find('a', class_='realty_link').text
    except:
        continue
    
    try:
        date = item.find('div', class_='date').text
    except:
        continue

    print(item_id)
    app_dict = {
                    'id': item_id,
                    'title': title,
                    'single_link': single_link,
                    'address': address,
                    'price': price,
                    'price_info': price_info,
                    'company_link': company_link,
                    'company_name': company_name,
                    'date': date
                }


    app_arr.append(app_dict)

with open('json/flats.json', 'w', encoding='utf-8') as f:
    json.dump(app_arr, f, ensure_ascii = False, indent =4, sort_keys=False)

df = pd.read_json('json/flats.json')
df.to_csv('csv/flats.csv')
