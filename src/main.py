import auctions
import utils
import item
import os
import json
import requests
import math

if __name__ == "__main__":
    utils.create_crafting_index()
    auctions.build_base_price_index()
