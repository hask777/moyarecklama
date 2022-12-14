import requests
from bs4 import BeautifulSoup
import lxml
import json
import pandas as pd
import os.path


url = "https://moyareklama.by/Гомель/новостройки/"
data = requests.get(url)

path = os.path.exists('files/html/realt.html')

if path != True:
    with open("files/html/realt.html", "w", encoding="utf-8") as f:
        f.write(data.text)
else:
    print("this file allready exists!")

with open("files/html/realt.html", 'r', encoding='utf-8') as f:
    page = f.read()
# print(data)

soup = BeautifulSoup(page, 'lxml')
items = soup.find_all('div', class_="one_complex_list")

main_url = 'https://www.moyareklama.by/'

app_dict = {}
app_arr = []

for item in items:
    item_id = item.get('id')
    title = item.find('div', class_="adv-list-title").text
    # title = title.replace(" ", "")
    address = item.find('div', class_='adv-list-content').text

    if 'Железнодорожный' in address:
        category = 'Железнодорожный'
    if 'Центральный' in address:
        category = 'Центральный'
    if 'Советский' in address:
        category = 'Советский'
    if 'Новобелицкий' in address:
        category = 'Новобелицкий'
    if 'Гомельский' in address:
        category = 'Гомельский'

    status = item.find('div', class_='adv-list-content text').text
    # status = status.replace(" ", "")

    links = item.find_all('a')
    lines = item.find_all('div', class_='apartment_line')
    prices = item.find_all('div', class_='apartment_price')
    developer = item.find('div', class_='adv-list-content developer').text
    image = item.find('div', class_="image").get('style')
    image = image.replace('background-image: url', '').replace('\'', '').replace('(', '').replace(')', '')
    
    print(image)

    app_dict = {
        'id': item_id,
        'title': title,
        'category': category,
        'address': address,
        'status': status,
        'links': [main_url + l.get('href') for l in links],
        'lines': [l.text for l in lines],
        'prices': [p.text for p in prices],
        'developer': developer,
        'image': image
    }

    app_arr.append(app_dict)

with open('files/json/new.json', 'w', encoding='utf-8') as f:
    json.dump(app_arr, f, ensure_ascii = False, indent =4, sort_keys=False)

df = pd.read_json('files/json/new.json')
df.to_csv('files/csv/new.csv')