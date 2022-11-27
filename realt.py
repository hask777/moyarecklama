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
    link3 = main_url + item.find_all('a')[3].get('href')
        
    lines = item.find_all('div', class_="apartment_line")
    # for l in lines:
    #     line = l.text # line = l.find_all('div', class_='apartment_line')

    #     print(line)

    developer = item.find('div', class_='adv-list-content developer').text
    
    app_dict = {
        'title': title,
        'complex': complex_link,
        'address': address,
        'status': status,
        'complex_link': link3,
        'line': [l.text for l in lines],
        # 'price': price.text,
        'developer': developer
    }

    app_arr.append(app_dict)

with open('json/new.json', 'w', encoding='utf-8') as f:
    json.dump(app_arr, f, ensure_ascii = False, indent =4, sort_keys=False)

