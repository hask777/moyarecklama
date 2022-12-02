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

    for i in range(1,66):
        url = f"https://moyareklama.by/Гомель/квартиры_продажа/все/8/{i}/"
        data = requests.get(url)
        print(url)

        soup = BeautifulSoup(data.text, 'lxml')
        # print(soup.prettify)

        items = soup.find_all('div', class_="one_advert_list")
        
        num = 0
             
        for item in items:
           
            link = main_url + item.find('div', class_="title").find('a').get('href')
            data = requests.get(link)
            soup = BeautifulSoup(data.text, 'lxml')
            images = []

            content = soup.find('div', class_="adsContent")
            try:
                photos_bl = content.find('div', class_='photo_block_ad')
                if photos_bl == None:
                    # photos = photos_bl.find_all('div', class_='photo_preview')
                    
                    # for image in photos:
                    #     style = image.get('style')
                    #     pattern = "\w+"
                    #     img_url =  re.findall(pattern, style)
                    #     image = 'https://media1.moyareklama.by/i/p/'+ img_url[8] +'/'+ img_url[9] +'/'+ img_url[10] +'.jpg'
                    #     images.append(image)
                    print('False')
                    
                else:
                    num = num + 1
                    print(num)
                    
                    
            except:
                continue    
                    
            
#             app_dict ={
#                                 'number': num,
#                                 'link': link,
#                                 'images': images,
#                                 # 'count': counter(count)
#                         }

# #             # app_arr.append([link, item_id, title, address, price, company_name, company_link])
#             app_arr.append(app_dict)

#         print(len(app_arr))

#     with open(f'files/json/flats.json', 'w', encoding='utf-8') as f:
#             json.dump(app_arr, f, ensure_ascii = False, indent =4, sort_keys=False)

#     print("JSON File write!")

#     df = pd.read_json('files/json/flats.json')
#     df.to_csv('files/csv/flats.csv')

#     print('CSV File write!')

#     # df = pd.DataFrame(app_arr)
#     # df.to_csv('files/csv/flats.csv')
       
get_appartments_single()         