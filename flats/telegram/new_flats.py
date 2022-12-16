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

def get_new_flats():
    with open('flats/files/json/new_flats.json', 'r') as f:
        new_flats = json.loads(f.read())
        print(new_flats)

    with open('flats/files/json/flats.json', 'r', encoding='utf-8') as f:
        flats = json.loads(f.read())
        print(flats)
    all_flats = [flat['id'] for flat in flats]

    for new_flat in new_flats:
        if new_flat in all_flats:
            print(f'https://www.moyareklama.by/Гомель/квартиры_продажа//single/ad/{new_flat}')

get_new_flats()