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
import asyncio
import aiohttp

app_arr = []
app_dict = {}
posts_ids = []
new_flats_list = []
last_new_flats = [] 

start_time = time.time()

main_url = 'https://www.moyareklama.by/Гомель/квартиры_продажа/'

async def get_page_data(session, page):
    url = f"https://moyareklama.by/Гомель/квартиры_продажа/все/8/{page}"

    async with session.get(url=url) as response:
        data = await response.text()
        print(url)
        soup = BeautifulSoup(data, 'lxml')
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
            try:
                address = item.find('div', class_="address").text
            except:
                address = None
            # area
            if address is not None:
                try:
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
                except:
                    area = None

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
                        # 'area': area,
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

    with open('flats/async/files/json/new_flats.json',  'w', encoding='utf-8') as f:
        json.dump(new_flats_list, f, ensure_ascii = False, indent =4, sort_keys=False)

async def gather_data():
    main_url = 'https://www.moyareklama.by/Гомель/квартиры_продажа/'
    async with aiohttp.ClientSession() as session:
        response = await session.get(url=main_url)
        soup = BeautifulSoup(await response.text(), 'lxml')
        pages = int(soup.find_all('li', class_='page-item')[-2].text)
        items_count = soup.find('div', class_="current").text
        print(f"{items_count}страниц: {pages}")

        tasks = []

        for page in range(1, pages + 1):
            task = asyncio.create_task(get_page_data(session, page))
            tasks.append(task)

        await asyncio.gather(*tasks)
            

def main():
    
    asyncio.run(gather_data())
    # current_time = datetime.datetime.now().strftime('%d_%m_%Y_%H_%M')
    finish_time = time.time() - start_time
    
    print(finish_time)

if __name__ == '__main__':
    main()