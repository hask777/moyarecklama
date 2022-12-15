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

    posts_ids = []

    # headers = {"user-agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36"}

    main_url = 'https://www.moyareklama.by/Гомель/квартиры_продажа/'

    req = requests.get(main_url)
    soup = BeautifulSoup(req.text, 'lxml')
    pages = soup.find_all('li', class_='page-item')
    last = pages[-2].text
    last = int(last)

    items_count = soup.find('div', class_="current").text
    print(f"{items_count}страниц: {last}")

    for i in range(1, 2):
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

            
            app_dict = {
                    'number': num,
                    'id': item_id,
                    'link': link,
                    'title': title.strip(),
                    'area': area,
                    'rooms': rooms,
                    'address': address,
                    'price': price.strip(),
                    'company_link': company_link,
                    'company_name': company_name.strip(),
            }

            # app_arr.append([link, item_id, title, address, price, company_name, company_link])
            app_arr.append(app_dict)
            posts_ids.append(item_id)

        print(len(app_arr))
    # print(posts_ids)

    # Every time rewrite all flats posts
    with open('files/json/flats.json', 'w', encoding='utf-8') as f:
        json.dump(app_arr, f, ensure_ascii = False, indent =4, sort_keys=False)

    # Creates only if does not exist
    if not os.path.exists('flats/flats_ids.txt'):
        print("File with flats ids is not exists! Create this FILE!!!")

        with open('flats/flats_ids.txt', 'w') as f:
            for item in posts_ids:
                f.write(str(item) + "\n")
    else:
        new_arr = []
        old_arr =[]
        # Grab all old ids
        with open('files/json/flats.json', 'r', encoding='utf-8') as f:
            flats = f.read()
        new_flats = json.loads(flats)
        # print(flats[0])
        # For old ids in old list
        for new_flat in new_flats:
            # print(flat['id'])
            new_flat_id = new_flat['id']
            new_arr.append(new_flat_id)
        # this the same is posts array
        for old in posts_ids:
            old_arr.append(old)

        
                
        

     
                   
    # print(new_arr)
    print("JSON File write!")

    df = pd.read_json('files/json/flats.json')
    df.to_csv('files/csv/flats.csv')

    print('CSV File write!')

    # df = pd.DataFrame(app_arr)
    # df.to_csv('files/csv/flats.csv')
       
get_appartments()         