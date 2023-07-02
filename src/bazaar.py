import requests
from requests.models import Response

JSON = requests.get("https://sky.shiiyu.moe/api/v2/bazaar").json()


def refresh() -> None:
    """refreshes the bazaar data"""
    global JSON
    c: Response = requests.get("https://sky.shiiyu.moe/api/v2/bazaar")
    JSON = c.json()


def recombobulater_price() -> float:
    """gets the price of a recombobulater

    Returns:
        str: the price
    """
    return float(JSON['RECOMBOBULATOR_3000']['buyPrice'])


def get_all_enchants() -> dict[str, str]:
    """gets all available skyblock enchants

    Returns:
        dict[str, str]: dict of enchant names and their bazaar prices
    """
    enchantments: dict[str, str] = {}
    for x in JSON:
        if x.startswith("ENCHANTMENT"):
            key = x[12:].strip()
            enchantments[key] = JSON[x]['buyPrice']
    return enchantments


def lower_base_enchants() -> list[str]:
    """all the enchant names

    Returns:
        list[str]: the names
    """
    enc = get_all_enchants()
    out: set[str] = set()
    for x in enc:
        top: str = " ".join(x.split("_")[:-1])
        if x.startswith("ULTIMATE"):
            top = top[9:]
        out.add(top.lower())
    return list(out)
