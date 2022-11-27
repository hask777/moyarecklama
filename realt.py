import requests
from bs4 import BeautifulSoup
import html5lib
import json

url = "https://moyareklama.by/Гомель/новостройки/"
req = requests.get(url)
data = req.text
# print(data)

soup = BeautifulSoup(data, 'html5lib')
items = soup.find_all('div', class_="one_complex_list")

main_url = 'https://www.moyareklama.by/'

app_dict = {}
app_arr = []

for item in items:
    title = item.find('div', class_="adv-list-content").text
    complex_link = main_url + item.find_all('a')[0].get("href")
    address = item.find('div', class_='adv-list-content').text
    status = item.find('div', class_='adv-list-content text').text

    links = item.find_all('a')

    lines = item.find_all('div', class_="apartment_line")
    prices = item.find_all('div', class_="apartment_price")
 
    developer = item.find('div', class_='adv-list-content developer').text
    
    app_dict = {
        'title': title,
        'complex': complex_link,
        'address': address,
        'status': status,
        'links': [main_url + link.get('href') for link in links],
        'lines': [l.text for l in lines],
        'prices': [p.text for p in prices],
        'developer': developer
    }

    app_arr.append(app_dict)

with open('json/new.json', 'w', encoding='utf-8') as f:
    json.dump(app_arr, f, ensure_ascii = False, indent =4, sort_keys=False)

