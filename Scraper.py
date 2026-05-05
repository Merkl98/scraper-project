# HTTP requests
import requests

# HTML parsing
from bs4 import BeautifulSoup

# data handling (useful later when saving results)
import pandas as pd

# regex for extracting numbers, prices, etc.
import re

from collections import namedtuple 

# optional typing (helps readability)
from typing import List, Dict, Optional

AUCTION_PAGE_URL = "https://urbanauctions.ca/"
WAREHOUSE_URL = "https://www.skatewarehouse.com/Clearance_Skateboard_Clothing/catpage-SALEAPPAREL.html"

def main() -> None:
    url = WAREHOUSE_URL
    df = pd.DataFrame

#think tree: need to loop each category section with nested loops for headers - items.


    response = get_web_data(url)
    soup = BeautifulSoup(response.text, "html.parser")
    containers = soup.find_all("a", class_="cattable-wrap-cell-info")
    articles = soup.find_all("div", class_="catheader")
    print(articles)

    df = load_pandas(containers, df, articles)
    print_csv(df)

def get_web_data(url):
    response = requests.get(url)
    response.raise_for_status()
    return response

def load_pandas(items, data, type):
    clothes = []
    article = type.find("h2").text.strip()
    for container in items:
        name = container.find("div", class_="cattable-wrap-cell-info-name").text.strip()
        link = container["href"]
        price = container.find("div", class_="cattable-wrap-cell-info-price").find("span").text.strip()
        item = {"Name": name, "Link": link, "Price": price, "Type": article}
        clothes.append(item)
    data = pd.DataFrame(clothes)
    return data

def print_csv(data):
    data.to_csv("clearance_findings.csv", index=False)


if __name__ == "__main__":
    main()