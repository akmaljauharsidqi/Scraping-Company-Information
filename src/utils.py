import requests, pandas as pd
from .soup import Soup
from .models import Company
import datetime

def get_html(url : str):
    r = requests.get(url)
    return Soup(r.text)

def save_to_xlsx(companies : list[Company], filename : str):
    date = datetime.datetime.now().strftime("%d_%B_%Y")
    df = pd.DataFrame(companies)
    df.to_excel(f"{date}-{filename}")