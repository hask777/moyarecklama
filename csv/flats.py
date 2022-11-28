import requests
from bs4 import BeautifulSoup
import html5lib
import json
import pandas as pd
import os.path

url = "https://moyareklama.by/Гомель/новостройки/"
data = requests.get(url)

path = os.path.exists('html/realt.html')

if path != True:
    with open("html/realt.html", "w", encoding="utf-8") as f:
        f.write(data.text)
else:
    print("this file allready exists!")

with open("html/realt.html", 'r', encoding='utf-8') as f:
    page = f.read()
# print(data)

soup = BeautifulSoup(page, 'html5lib')
items = soup.find_all('div', class_="one_complex_list")

main_url = 'https://www.moyareklama.by/'

app_dict = {}
app_arr = []

for item in items:
    pass