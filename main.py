import requests
from bs4 import BeautifulSoup
import lxml
import csv
import json
import pandas as pd
import os.path
import time

# functions
from flats.flats import get_appartments

if __name__ == '__main__':
    while True:
        get_appartments()
        time.sleep(10)