import requests
import bazaar
import utils
import item
import tqdm
import json
from typing import Union
import log

# {
# "item_name": {
# current_price: int,
# count: int,
# }
# }

BASEPRICEINDEX: dict[str, dict[str, Union[int, float]]] = {}
LAST_UPDATED = 0


def request_page(page: int) -> dict:
    """requests a page of auctions

    Args:
        page (int): the page to request

    Returns:
        dict: the json response
    """
    c = requests.get(f"https://api.hypixel.net/skyblock/auctions?page={page}")
    return c.json()


def last_updated() -> int:
    """gets the last time the bazaar was updated

    Returns:
        int: the last time the bazaar was updated
    """
    c = requests.get("https://api.hypixel.net/skyblock/auctions?page=0")
    resp = c.json()
    return resp['lastUpdated']


def get_total_pages() -> int:
    """gets the total number of auction pages

    Returns:
        int: the total number of auction pages
    """
    c = requests.get("https://api.hypixel.net/skyblock/auctions?page=0")
    resp = c.json()
    return resp['totalPages']


def build_base_price_index() -> None:
    """builds the base price index"""
    global BASEPRICEINDEX
    total_pages = get_total_pages()

    log.iprint("Building base price index")
    current_page = tqdm.tqdm(
        range(total_pages), position=0)
    current_processing = tqdm.tqdm(position=1, bar_format='{desc}')
    for page in current_page:
        resp = request_page(page)
        for auction in resp['auctions']:
            current_processing.set_description_str(
                f"processing {auction['uuid']}")

            i = item.Item(auction)
            name = i.get_clean_name()
            price = i.clean_item_price()
            if name not in BASEPRICEINDEX:
                BASEPRICEINDEX[name] = {
                    "current_price": price,
                    "count": 1
                }
                continue
            else:
                BASEPRICEINDEX[name]['current_price'] += price
                BASEPRICEINDEX[name]['count'] += 1
    current_page.close()
    current_processing.close()
    log.iprint("Finished building base price index")
    calculate_average_prices()


def calculate_average_prices() -> None:
    """calculates the average prices"""
    global BASEPRICEINDEX
    log.iprint("Calculating average prices")
    for item in tqdm.tqdm(BASEPRICEINDEX):
        BASEPRICEINDEX[item]['current_price'] /= BASEPRICEINDEX[item]['count']


def save_base_price_index() -> None:
    """saves the base price index"""
    global BASEPRICEINDEX
    with open("./base_price_index.json", "w", encoding='utf8') as f:
        json.dump(BASEPRICEINDEX, f)


def load_base_price_index() -> None:
    """loads the base price index"""
    global BASEPRICEINDEX
    with open("./base_price_index.json", "r", encoding='utf8') as f:
        BASEPRICEINDEX = json.load(f)


if __name__ == "__main__":
    load_base_price_index()
    calculate_average_prices()
    save_base_price_index()
