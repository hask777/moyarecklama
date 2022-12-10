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

    main_url = 'https://www.moyareklama.by/Гомель/квартиры_продажа/'

    req = requests.get(main_url)
    soup = BeautifulSoup(req.text, 'lxml')
    pages = soup.find_all('li', class_='page-item')
    last = pages[-2].text
    last = int(last)
    # print(last)


    for i in range(1, last + 1):
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
            content = soup.find('div', id="one_ads_show")
            # Title
            title = content.find('h1').text
            title_ = title.replace('-ком.', '').replace('квартира ', '').replace('м²', '').replace('эт', '')
            pattern = "\w+"
            title_info =  re.findall(pattern, title_)
            # print(title_info)
            if len(title_info) == 5:
                if 'Студия' in title_info:
                    rooms = 'Студия'
                else:
                    rooms = int(title_info[0])
                    sq_live = int(title_info[1] + title_info[2])/10
                    height = int(title_info[3])
                    tall = int(title_info[4])
            elif len(title_info) == 4:
                if 'Студия' in title_info:
                    rooms = 'Студия'
                else:
                    rooms = int(title_info[0])
                    sq_live = int(title_info[1])
                    height = int(title_info[2])
                    tall = int(title_info[3])

            address = content.find('div', class_="address").text
            
            try:
                prices = content.find_all('div', class_="adsPrice")
                for pr in prices:
                    price = pr.find('div', class_='price').text
                    price = price.replace('             р.', '').strip().replace(' ', '.').replace(',', '')
                    price = float(price)
                    price_square = pr.find('div', class_='price_square').text
                    price_square = price_square.replace('  р./м²', '').replace(',', '.').replace(' ', '')
                    price_square = float(price_square)

            except:
                price = None
                price_square = None
            # propierties
            square = content.find('div', class_="square full").text
            # square_all
            # square_live
            # square_kitchen
            type_house = content.find('div', class_="type_house").text
            type_house = type_house.replace("Тип дома:", '')

            floor = content.find('div', class_="floor").text

            try:
                water = content.find('div', class_="water").text
                water = water.replace('\nВодоснабжение:', '').strip()
            except:
                water = None
            try:
                bathroom = content.find('div', class_="bathroom").text
                bathroom = bathroom.replace('\nСанузел:', '').strip()
            except:
                bathroom = None
            try:
                balcony = content.find('div', class_="balcony").text
                balcony = balcony.replace('\nБалкон: ', '').strip()
            except:
                balcony = None
            try:
                repair = content.find('div', class_="repair").text
                repair = repair.replace('Ремонт: ', '').strip()
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
                            'title': title,
                            'address': address,
                            'price': price,
                            'price_square': price_square,
                            'rooms': rooms,
                            'sq_live': sq_live,
                            'height': height,
                            'tall': tall,
                            'square': square.strip(),
                            'type_house': type_house.strip(),
                            'floor': floor,
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