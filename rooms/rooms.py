import requests
from bs4 import BeautifulSoup
import lxml
import csv
import json
import pandas as pd
import os.path
import time

def get_rooms():

    app_arr = []
    app_dict = {}

    # headers = {"user-agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36"}

    main_url = 'https://www.moyareklama.by'

    for i in range(1,3):
        url = f"https://moyareklama.by/Гомель/комнаты_продажа/все/8/{i}/"
        data = requests.get(url)
        print(url)

        soup = BeautifulSoup(data.text, 'lxml')
        # print(soup.prettify)

        items = soup.find_all('div', class_="one_advert_list")
        # print(len(items))
        num = 0
             
        for item in items:
            num = num + 1
            item_id = item.find('div', class_="title").find('a').get('href').replace('/single/ad/', '')
            link = main_url + item.find('div', class_="title").find('a').get('href')
            title = item.find('div', class_="title").text
            address = item.find('div', class_="address").text
            price = item.find('div', class_="price_block").text
            try:
                company_link = item.find('a', class_="realty_link")
                if company_link:
                    company_link = item.find('a', class_="realty_link").get('href')
                else:
                    company_link = "None"
            except:
                continue

            company_name = item.find('div', class_="company").text
                
            app_dict ={
                    'number': num,
                    'id': item_id,
                    'link': link,
                    'title': title.strip(),
                    'address': address,
                    'price': price.strip(),
                    'company_link': company_link,
                    'company_name': company_name.strip(),
                    # 'count': counter(count)
            }

            # app_arr.append([link, item_id, title, address, price, company_name, company_link])
            app_arr.append(app_dict)

        print(len(app_arr))

    with open(f'files/json/rooms.json', 'w', encoding='utf-8') as f:
            json.dump(app_arr, f, ensure_ascii = False, indent =4, sort_keys=False)

    print("JSON File write!")

    df = pd.read_json('files/json/rooms.json')
    df.to_csv('files/csv/rooms.csv')

    print('CSV File write!')

    # df = pd.DataFrame(app_arr)
    # df.to_csv('files/csv/rooms.csv')

get_rooms() 
            