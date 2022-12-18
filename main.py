import requests
from bs4 import BeautifulSoup
import lxml
import csv
import json
import pandas as pd
import os.path
import time
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root():
    with open('flats/telegram/files/json/api_new_flats.json', 'r', encoding='utf-8') as f:
        new_flats = json.loads(f.read())
    return {'flats': new_flats}