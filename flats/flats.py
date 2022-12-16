import requests
from bs4 import BeautifulSoup
import lxml
import csv
import json
import pandas as pd
import os.path
import time
from tqdm import tqdm

def get_appartments():

    app_arr = []
    app_dict = {}

    posts_ids = []

    # headers = {"user-agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36"}

    main_url = 'https://www.moyareklama.by/Гомель/квартиры_продажа/'

    req = requests.get(main_url)
    soup = BeautifulSoup(req.text, 'lxml')
    # pages = soup.find_all('li', class_='page-item')
    # last = pages[-2].text
    # last = int(last)

    pages = int(soup.find_all('li', class_='page-item')[-2].text)

    items_count = soup.find('div', class_="current").text
    print(f"{items_count}страниц: {pages}")

    for i in tqdm(range(1, pages + 1)):
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
            try:       
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
            except:
                rooms = None
            # Address
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
            # Price 
            price = item.find('div', class_="price_block").text   
            # ompany link
            try:
                company_link = item.find('a', class_="realty_link")
                if company_link:
                    company_link = item.find('a', class_="realty_link").get('href')
                else:
                    company_link = "None"
            except:
                continue
            # Company name
            try:
                company_name = item.find('div', class_="company").text
            except:
                company_name = None
            # date
            date = item.find('div', class_='date').text

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
                    'date': date
            }

            # app_arr.append([link, item_id, title, address, price, company_name, company_link])
            app_arr.append(app_dict)
            posts_ids.append(item_id)

        print(len(app_arr))
    # print(posts_ids)

    # Every time rewrite all flats posts
    with open('flats/files/json/flats.json', 'w', encoding='utf-8') as f:
        json.dump(app_arr, f, ensure_ascii = False, indent =4, sort_keys=False)

    # Creates only if does not exist
    if not os.path.exists('flats/files/txt/flats_ids.txt'):
        print("File with flats ids is not exists! Create this FILE!!!")

        with open('flats/files/txt/flats_ids.txt', 'w') as f:
            for item in posts_ids:
                f.write(str(item) + "\n")
    else:
        # Grab all old ids
        with open('flats/files/json/flats.json', 'r', encoding='utf-8') as f:
            # flats = f.read()
            new_flats = json.loads(f.read())

        with open('flats/files/txt/flats_ids.txt', 'r', encoding='utf-8') as f:
            flats_ids = f.read()

        # For old ids in old list
        for new_flat in new_flats:
            if new_flat['id'] not in flats_ids:

                print(f'new flat: {new_flat["id"]}')
                
                posts_ids.append(f'{new_flat["id"]} new')

                with open('flats/files/txt/flats_ids.txt', 'w') as f:
                    for item in posts_ids:
                        f.write(str(item) + "\n")
            # else:
            #     print(f'no new: {new_flat["id"]}')
        
    # print(new_arr)
    print("JSON File write!")

    df = pd.read_json('flats/files/json/flats.json')
    df.to_csv('flats/files/csv/flats.csv')

    print('CSV File write!')
       
get_appartments()         