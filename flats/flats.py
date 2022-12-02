import requests
from bs4 import BeautifulSoup
import lxml
import csv
import json
import pandas as pd
import os.path
import time

def get_appartments():

    app_arr = []
    app_dict = {}

    # headers = {"user-agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36"}

    main_url = 'https://www.moyareklama.by'

    for i in range(1,66):
        url = f"https://moyareklama.by/Гомель/квартиры_продажа/все/8/{i}/"
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
            data = requests.get(link)
            soup = BeautifulSoup(data.text, 'lxml')
            try:
                items = soup.find('div', class_='slider')
                if items != None:
                    images = items.find_all('div', class_='photo_preview')
                    for image in images:
                        image = image.get('style')
                        image = image.replace("background:url(", '').replace(') no-repeat 50% 50% #f5f5f5; background-size: contain', '')
                        print(image)
                else:
                    images = 'None'
            except:
                continue

            title = item.find('div', class_="title").text
           
            # rooms
            if '1-ком' in title:
                rooms = 1
            if '2-ком' in title:
                rooms = 2
            if '3-ком' in title:
                rooms = 3
            if '4-ком' in title:
                rooms = 4
            if '5-ком' in title:
                rooms = 5
            if '6-ком' in title:
                rooms = 6

            address = item.find('div', class_="address").text

             # area
            if 'Железнодорожный' in address:
                area = 'Железнодорожный'
            if 'Центральный' in address:
                area = 'Центральный'
            if 'Советский' in address:
                area = 'Советский'
            if 'Новобелицкий' in address:
                area = 'Новобелицкий'
            if 'Гомельский' in address:
                area = 'Гомельский'

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
                    'images': images,
                    'title': title.strip(),
                    'area': area,
                    'rooms': rooms,
                    'address': address,
                    'price': price.strip(),
                    'company_link': company_link,
                    'company_name': company_name.strip(),
                    # 'count': counter(count)
            }

            # app_arr.append([link, item_id, title, address, price, company_name, company_link])
            app_arr.append(app_dict)

        print(len(app_arr))

    with open(f'files/json/flats.json', 'w', encoding='utf-8') as f:
            json.dump(app_arr, f, ensure_ascii = False, indent =4, sort_keys=False)

    print("JSON File write!")

    df = pd.read_json('files/json/flats.json')
    df.to_csv('files/csv/flats.csv')

    print('CSV File write!')

    # df = pd.DataFrame(app_arr)
    # df.to_csv('files/csv/flats.csv')
       
get_appartments()         