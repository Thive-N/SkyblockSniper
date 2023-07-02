import requests
import bazaar
import utils
import item


BASEPRICEINDEX: dict[str, str] = {}
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
    for page in range(total_pages):
        print(f"page {page}/{total_pages}")
        resp = request_page(page)
        for auction in resp['auctions']:
            if auction['bin']:
                if auction['item_name'] not in BASEPRICEINDEX:
                    BASEPRICEINDEX[auction['item_name']
                                   ] = auction['starting_bid']
