import requests
from bs4 import BeautifulSoup
import lxml
import csv
import json
import pandas as pd
import os.path
import time
import datetime
from tqdm import tqdm

def get_appartments():

    current_date = datetime.datetime.now().strftime('%d_%m_%Y')
    print(current_date)
    # convert = datetime.strptime(date_string, format)
    # datetime_str = '09/19/22 13:55:26'
    # datetime_object = datetime.strptime(datetime_str, '%m/%d/%y %H:%M:%S')

    app_arr = []
    app_dict = {}
    posts_ids = []
    new_flats_list = []
    last_new_flats = [] 

    main_url = 'https://www.moyareklama.by/Гомель/квартиры_продажа/'

    req = requests.get(main_url)
    soup = BeautifulSoup(req.text, 'lxml')
    pages = int(soup.find_all('li', class_='page-item')[-2].text)
    items_count = soup.find('div', class_="current").text
    print(f"{items_count}страниц: {pages}")

    for i in tqdm(range(1, pages + 1)):
        url = f"https://moyareklama.by/Гомель/квартиры_продажа/все/8/{i}"
        data = requests.get(url)
        print(url)

        soup = BeautifulSoup(data.text, 'lxml')
        items = soup.find_all('div', class_="one_advert_list")

        num = 0
             
        for item in items:
            num = num + 1
            item_id = item.find('div', class_="title").find('a').get('href').replace('/single/ad/', '')
            link = main_url + item.find('div', class_="title").find('a').get('href')
            data = requests.get(link)
            soup = BeautifulSoup(data.text, 'lxml')
            title = item.find('div', class_="title").text
            title = title.strip()
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
                    'title': title,
                    'area': area,
                    'rooms': rooms,
                    'address': address,
                    'price': price.strip(),
                    'company_link': company_link,
                    'company_name': company_name.strip(),
                    'date': date.strip()
            }

            # app_arr.append(current_date)
            app_arr.append(app_dict)
            # posts_ids.append(current_date)
            posts_ids.append(item_id)

        print(len(app_arr))
    # print(posts_ids)

    '''START wirte today data'''
    # Every time rewrite all flats posts
    with open(f'flats/files/json/flats.json', 'w', encoding='utf-8') as f:
        json.dump(app_arr, f, ensure_ascii = False, indent =4, sort_keys=False)

    # with open(f'flats/files/json/flats{current_date}.json', 'w', encoding='utf-8') as f:
    #     json.dump(app_arr, f, ensure_ascii = False, indent =4, sort_keys=False)

    # Creates only if does not exist
    if not os.path.exists(f'flats/files/json/flats_ids.json'):
        print("File with flats ids is not exists! Create this FILE!!!")

        with open(f'flats/files/json/flats_ids.json', 'w', encoding='utf-8') as f:          
            json.dump(posts_ids, f, ensure_ascii = False, indent =4, sort_keys=False)

        # with open(f'flats/files/txt/flats_ids{current_date}.txt', 'w', encoding='utf-8') as f:          
        #     f.write(str(posts_ids))

    else:
        
        with open(f'flats/files/json/flats.json', 'r', encoding='utf-8') as f:
            new_flats = json.loads(f.read())

        with open(f'flats/files/json/flats_ids.json', 'r', encoding='utf-8') as f:
            flats_ids = json.loads(f.read())

        for new_flat in new_flats:       
            if new_flat['id'] not in flats_ids:
                print(new_flat['id'])
                new_flats_list.append(new_flat['id'])

        with open('flats/files/json/new_flats.json',  'w', encoding='utf-8') as f:
            json.dump(new_flats_list, f, ensure_ascii = False, indent =4, sort_keys=False)           
                    
        for new_flat in new_flats:
            last_new_flats.append(new_flat['id'])
            with open(f'flats/files/json/flats_ids.json', 'w', encoding='utf-8') as f:
                json.dump(last_new_flats, f, ensure_ascii = False, indent =4, sort_keys=False)
     
    print("JSON File write!")

    df = pd.read_json(f'flats/files/json/flats.json')
    df.to_csv('flats/files/csv/flats.csv')

    print('CSV File write!')
       
get_appartments()         