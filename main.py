import requests
from bs4 import BeautifulSoup

url = "https://moyareklama.by/Гомель/новостройки/"
req = requests.get(url)
data = req.text
# print(data)

soup = BeautifulSoup(data, 'html.parser')
items = soup .find_all('div', class_="one_complex_list")
print(items)
