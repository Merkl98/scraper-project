import requests
from bs4 import BeautifulSoup
import pandas as pd
import re

from collections import namedtuple 
from typing import List, Dict, Optional

AUCTION_PAGE_URL = "https://urbanauctions.ca/"
WAREHOUSE_URL = "https://www.skatewarehouse.com/Clearance_Skateboard_Clothing/catpage-SALEAPPAREL.html"

def main() -> None:
    url = WAREHOUSE_URL
    df = pd.DataFrame()

#think tree: need to loop each category section with nested loops for headers - items.

    response = get_web_data(url)
    soup = BeautifulSoup(response.text, "html.parser")
    containers = soup.find_all("a", class_="cattable-wrap-cell-info")

    df = load_pandas(containers, df)
    df = price_ascending(df)
    print_csv(df)

def get_web_data(url):
    response = requests.get(url)
    response.raise_for_status()
    return response

def load_pandas(items, data):
    clothes = []
    for container in items:
        name = container.find("div", class_="cattable-wrap-cell-info-name").text.strip()
        link = container["href"]
        price = container.find("div", class_="cattable-wrap-cell-info-price").find("span").text.strip().replace("$","")
        price = float(price)
        item = {"Name": name, "Link": link, "Price": price}
        clothes.append(item)
    data = pd.DataFrame(clothes)
    return data

def print_csv(data):
    data.to_csv("clearance_findings.csv", index=False)

def price_ascending(data):
    data = data.sort_values("Price")
    print(data)
    return data


if __name__ == "__main__":
    main()