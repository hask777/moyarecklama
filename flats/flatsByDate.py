import requests
from bs4 import BeautifulSoup
import lxml
import csv
import json
import pandas as pd
import os.path
import time
import datetime
from datetime import date
from datetime import timedelta
from tqdm import tqdm

today = date.today()
yesterday = today - timedelta(days = 2)
yesterday = yesterday.strftime('%d.%m.%Y')
print(str(yesterday))

current_date = datetime.datetime.now().strftime('%d_%m_%Y')
# print(current_date)

def get_new_flats_dates():



    current_date = datetime.datetime.now().strftime('%d_%m_%Y')
    # Grab all old ids
    with open(f'flats/files/json/flats.json', 'r', encoding='utf-8') as f:
        last_flats = json.loads(f.read())

    new_flats_list = []

    for new_flat in last_flats:
        # print(new_flat['date'])    
        if new_flat['date'] == yesterday:    
            new_flats_list.append(new_flat['date'])
    
            with open(f'flats/files/json/new_flats_date.json', 'w', encoding='utf-8') as f:          
                json.dump(new_flats_list, f, ensure_ascii = False, indent =4, sort_keys=False)

    print(new_flats_list) 
    print("JSON File write!")

    # df = pd.read_json(f'flats/files/json/flats_time.json')
    # df.to_csv('flats/files/csv/flatsByDate.csv')

    print('CSV File write!')
       
get_new_flats_dates()         