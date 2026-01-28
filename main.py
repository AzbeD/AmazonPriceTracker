import requests
import os
import json
from dotenv import load_dotenv
from urllib.parse import urlparse, parse_qs
import datetime

def main():
    url = "https://www.amazon.de/-/en/Sennheiser-Momentum-Wireless-Cancelling-Headphones-black/dp/B0B6GHW1SX/ref=sr_1_4?sr=8-4"
    asin = getAsin(url)
    product, price = extractPrice(asin)
    product_short = " ".join(product.split()[:4])
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("CenaIzdelka.txt", "a") as text_file:
         text_file.write(f"{now} Izdelek: {product_short}; cena: {price}$\n")

def extractPrice(asin):
    load_dotenv()
    SERPAPI_API_KEY = os.getenv('SERPAPI_API_KEY')

    params = {
        "api_key": SERPAPI_API_KEY,
        "engine": "amazon_product",
        "asin": asin,
        "amazon_domain": "amazon.de"
    }

    search = requests.get("https://serpapi.com/search", params=params)
    response = search.json()

    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(response,f, ensure_ascii=False, indent=4)
    
    product_results = response.get("product_results", {})
    title = product_results.get("title")
    price = product_results.get("extracted_price")

    if not price:
        price = product_results.get("price")

    return title, price

def getAsin(url):
    asin = url.split('/dp/')[1].split('/')[0]
    return asin

main()
