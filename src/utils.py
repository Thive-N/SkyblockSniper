import git
import log
import os
import shutil
import json
import tqdm

roman = {
    "M": 1000,
    "CM": 900,
    "D": 500,
    "CD": 400,
    "C": 100,
    "XC": 90,
    "L": 50,
    "XL": 40,
    "X": 10,
    "IX": 9,
    "V": 5,
    "IV": 4,
    "I": 1}


def roman_to_integer(str) -> int:
    """Converts a roman numeral to an integer.

    Args:
        str (str): the roman numeral to convert

    Returns:
        int: the integer
    """
    i = 0
    num = 0
    while i < len(str):
        if i + 1 < len(str) and str[i:i + 2] in roman:
            num += roman[str[i:i + 2]]
            i += 2
        else:
            num += roman[str[i]]
            i += 1
    return num


def create_crafting_index() -> None:
    """Creates a crafting index for the bazaar.

    Returns:
        None
    """
    updated = False
    if os.path.exists("./.metadata"):
        repo = git.Repo("./.metadata")
        if repo.is_dirty():
            log.iprint("Changes detected, refreshing repo...")
            repo.remotes.origin.pull()
            updated = True

    else:
        log.iprint("Cloning repo...")
        git.Repo.clone_from(
            "https://github.com/NotEnoughUpdates/NotEnoughUpdates-REPO.git", "./.metadata")
        log.iprint("cloned repo")
        updated = True

    if not updated:
        log.iprint("repo up to date, skipping...")

    log.iprint("creating index...")
    single_dump = {}
    item_jsons = [d for d in os.listdir(
        "./.metadata/items") if d.endswith(".json")]
    file_log = tqdm.tqdm(total=0, position=1,
                         bar_format='{desc}')
    for item_json in (progress_bar := tqdm.tqdm(item_jsons, position=0)):
        file_log.set_description_str(f"processing {item_json}")
        item_str = item_json.replace(".json", "")
        with open(f"./.metadata/items/{item_json}", "r", encoding='utf8') as f:
            item = json.load(f)
            single_dump[item_str] = item

    with open("./data.json", "w", encoding='utf8') as f:
        json.dump(single_dump, f)


if __name__ == "__main__":
    create_crafting_index()
