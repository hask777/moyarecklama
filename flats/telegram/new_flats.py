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
        # print(new_flats)

    with open('flats/files/json/flats.json', 'r', encoding='utf-8') as f:
        flats = json.loads(f.read())
        # print(flats)

    api_new_flats = []
    for flat in flats:
        flat = flat
        if flat['id'] in [new_flat for new_flat in new_flats]:
            api_new_flats.append(flat)
    # print(api_new_flats)
    with open('flats/telegram/files/json/api_new_flats.json', 'w', encoding='utf-8') as f:
        json.dump(api_new_flats, f, ensure_ascii = False, indent =4, sort_keys=False)
           


get_new_flats()