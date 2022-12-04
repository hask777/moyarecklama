import requests
from bs4 import BeautifulSoup
import lxml
import csv
import json
import pandas as pd
import os.path
import time
import re

def get_appartments_single():

    app_arr = []
    app_dict = {}

    # headers = {"user-agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36"}

    main_url = 'https://www.moyareklama.by'

    for i in range(1,2):
        url = f"https://moyareklama.by/Гомель/квартиры_продажа/все/8/{i}/"
        data = requests.get(url)
        print(url)

        soup = BeautifulSoup(data.text, 'lxml')
        # print(soup.prettify)

        items = soup.find_all('div', class_="one_advert_list")
        
        num = 0
             
        for item in items:
            num = num + 1
            link = main_url + item.find('div', class_="title").find('a').get('href')
            data = requests.get(link)
            soup = BeautifulSoup(data.text, 'lxml')
            # content
            item_id = link.replace('https://www.moyareklama.by/single/ad/', '')
            content = soup.find('div', class_="adsContent")
            title = content.find('h1').text
            # title = image.get('style')
            pattern = "\w+"
            title =  re.findall(pattern, title)
            address = content.find('div', class_="address").text
            # propierties
            square = content.find('div', class_="square full").text
            type_house = content.find('div', class_="type_house").text
            floor = content.find('div', class_="floor").text

            try:
                water = content.find('div', class_="water").text
            except:
                water = None
            try:
                bathroom = content.find('div', class_="bathroom").text
            except:
                bathroom = None
            try:
                balcony = content.find('div', class_="balcony").text
            except:
                balcony = None
            try:
                repair = content.find('div', class_="repair").text
            except:
                repair = None

            images = []

            try:
                photo = content.find('div', class_="pv1_big_img_container").find('img').get('src')
            except:
                photo = None

            try:
                photos = content.find_all('div', class_='photo_preview')
                for image in photos:
                    style = image.get('style')
                    pattern = "\w+"
                    img_url =  re.findall(pattern, style)
                    image = 'https://media1.moyareklama.by/i/p/'+ img_url[8] +'/'+ img_url[9] +'/'+ img_url[10] +'.jpg'
                    images.append(image)
                    # print(num)
            except:
                images = None
                          
            app_dict = {
                            'number': num,
                            'id': item_id,
                            'link': link,
                            'tile': title,
                            'address': address,
                            'square': square.strip(),
                            'type_house': type_house.strip(),
                            'floor': floor.split(),
                            'water': water,
                            'bathroom': bathroom,
                            'balcony': balcony,
                            'repair': repair,
                            'photo': photo,
                            'images': images,
                        }

            # app_arr.append([link, item_id, title, address, square, type_house, floor, water, bathroom, balcony, repair, photo, images])
            app_arr.append(app_dict)

        print(len(app_arr))

    with open(f'files/json/flats_single.json', 'w', encoding='utf-8') as f:
            json.dump(app_arr, f, ensure_ascii = False, indent =4, sort_keys=False)

    print("JSON File write!")

    # df = pd.read_json('files/json/flats_single.json')
    # df.to_csv('files/csv/flats_single.csv')

    # print('CSV File write!')

    df = pd.DataFrame(app_arr)
    df.to_csv('files/csv/flats_single.csv')

    print('CSV File write!')
       
get_appartments_single()         