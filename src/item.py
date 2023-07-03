import bazaar
import utils

TOP_REFORGES: list[str] = [
    ' ✦', ' ✪', 'Ambered ', 'Ancient ', 'Auspicious ', 'Awkward ', 'Bizarre ', 'Blessed ', 'Bloody ', 'Bountiful ', 'Bulky ', 'Candied ', 'Clean ', 'Cubic ',
    'Deadly ', 'Demonic ', 'Dirty ', 'Empowered ', 'Epic ', 'Fabled ', 'Fair ', 'Fast ', 'Fierce ', 'Fine ', 'Fleet ', 'Forceful ', 'Fruitful ', 'Gentle ',
    'Giant ', 'Gilded ', 'Godly ', 'Grand ', 'Hasty ', 'Headstrong ', 'Heated ', 'Heavy ', 'Heroic ', 'Hurtful ', 'Itchy ', 'Jaded ', "Jerry's ", 'Keen ',
    'Legendary ', 'Light ', 'Loving ', 'Lucky ', 'Magnetic ', 'Mithraic ', 'Moil ', 'Mythic ', 'Neat ', 'Necrotic ', 'Odd ', 'Ominous ', 'Perfect ', 'Pleasant ',
    'Precise ', 'Pretty ', 'Pure ', 'Rapid ', 'Refined ', 'Reinforced ', 'Renowned ', 'Rich ', 'Ridiculous ', 'Shaded ', 'Sharp ', 'Shiny ', 'Silky ', 'Simple ',
    'Smart ', 'Spicy ', 'Spiked ', 'Spiritual ', 'Stellar ', 'Stiff ', 'Strange ', 'Strong ', 'Submerged ', 'Superior ', 'Suspicious ', 'Sweet ', 'Titanic ',
    'Toil ', 'Undead ', 'Unpleasant ', 'Unreal ', 'Vivid ', 'Warped ', 'Warped ', 'Wise ', 'Withered ', 'Zealous ', '⚚ ', '✪'
]

ENCHANTS: list[str] = bazaar.lower_base_enchants()

BAZAAR_PRICES: dict[str, str] = bazaar.get_all_enchants()


class Item:
    def __init__(self, raw) -> None:
        self.item: str = raw
        self.uuid: str = raw['uuid']
        self.name: str = raw['item_name']
        self.lore: str = raw['item_lore']
        self.reforges: dict[str, str] = self.get_reforges()

    def is_recombobulated(self) -> bool:
        """Checks if the item is recombobulated
        Returns:
            bool: True if recombobulated, False if not
        """
        return "§d§l§ka" in self.lore

    def get_reforges(self) -> dict[str, str]:
        """Gets the reforges of the item
        Returns:
            dict[str, str]: dict of reforges and their levels
        """
        end = {}
        for x in self.lore.split("\n"):
            for enchant in ENCHANTS:
                if enchant in x.lower() and len(x[2:].split(" ")) == 2:
                    s = x[2:]
                    if s.startswith("§d§l"):
                        s = s[4:]
                    s.split(" ")
                    try:
                        end[s[0]] = utils.roman_to_integer(s[1])
                    except:
                        pass
        return end

    def get_reforge_price(self) -> float:
        """Sum of all the reforges' prices according to the bazaar

        Returns:
            float: the end sum
        """
        price: float = 0
        for reforge in self.reforges:
            thing = reforge.upper().replace(" ", "_") + \
                "_" + str(self.reforges[reforge])
            if "cultivating" in thing.lower():
                continue
            price += BAZAAR_PRICES[thing]
        return price

    def clean_item_price(self) -> float:
        """Gets the price of the item without reforges or recombobulater

        Returns:
            float: the price
        """
        cur = 0
        if self.item['bin']:
            cur = self.item['starting_bid']
        else:
            pass

        if self.is_recombobulated():
            cur -= bazaar.recombobulater_price()
        cur -= self.get_reforge_price()
        return cur

    def get_clean_name(self) -> str:
        """Gets the name of the item without reforges

        Returns:
            str: the name
        """
        for reforge in TOP_REFORGES:
            if reforge in self.name:
                return self.name.replace(reforge, "")
        return self.name

    def __str__(self) -> str:
        """returns the name of the item

        Returns:
            str: the name of the item
        """
        return self.name

    def __eq__(self, other: object) -> bool:
        return self.__hash__() == other.__hash__()

    def __ne__(self, other) -> bool:
        return not self.__eq__(other)

    def __hash__(self) -> str:
        return self.uuid


if __name__ == "__main__":
    test = {'uuid': '69c4110f8a9041fbb0a23133c6e61a08', 'auctioneer': '2d3e8491b06a4e129dbe79268bb6a943', 'profile_id': '6183f4739afd470d992a32b108431aed', 'coop': ['2d3e8491b06a4e129dbe79268bb6a943'], 'start': 1688410965138, 'end': 1688583765138,
            'item_name': 'Dwarf Turtle Shelmet',
            'item_lore': "§8Consumed on use\n\n§7§7Pet items can boost pets in\n§7various ways but pets can only\n§7hold 1 item at a time so choose\n§7wisely!\n\n§7§7Makes the pet's owner immune\n§7to knockback.\n\n§7§eRight click on your summoned\n§epet to give it this item!\n\n§9§lRARE PET ITEM", 'extra': 'Dwarf Turtle Shelmet Skull Item', 'category': 'misc', 'tier': 'RARE', 'starting_bid': 1000000,
            'item_bytes': 'H4sIAAAAAAAAAE1SzW7aQBAe8tMCh6ZqK/XSwyaK1BONsQ3ElXJAwSmOMCFgoHCJ1vaAF9Y28q6TOO/Q5+DaZ8iDVV3Sqqq0l9nvb2Z2qwAVKLEqAJT2YI+FpR8lOLxM80SWqrAv6XIfKl0W4hWnS6FYv6pQHa1zzm8eEszKsOeEcNpoaOehHvg1bJq0ZtTrWPMbZr3W0qxmS/NNS6eh0g2ydIOZZCgqUJb4KPMMxUt0GQ4nlOcIP7G41ubfIy38fs2Dwmmq2htp/MZZbVpOMin8S6fpxArvtpu9wvqP25B02uAz4zqaJ7e5H0+0njHk2B3Wg3h831/NtP5qbc7jSdSfTlauPivm8a0x/+YYMy/iqtbm3tq8mdqP/SdbdztuffZ0zeYdV99p3achm3lX0Xw1Nl1vbDhJ3VrcXlyo7qvwOmRiw2lRgYNemmFZXb6Bd8/b88s0EXmMIUkTkgtU98fP25Y6A5SESYwFCWhC/DQVkmxQCsKSF8o9zViaC/JAC0H8/C+446YJL+BEUaKUh6T+4kKoJJRIFiMRKQkiZYdQVZwHJpAXxyr35E+uS9coiIxwZ/hZkHT3ioTFcZ4gvFUEmZJ1kgZrnwbrL/90OGTLSJKAs2C9m6VI84yoyeI0wRA+KYKyI0q7ZPeoWlIJTLy0tst+/7y1nrd82B7aZGB7xPFstwwHfRojfFRY54FmC+LlmeRIRhHyGKXa6pH9KDPaljJjagMoyrv/CR860/bw6s4bD72efTfq2j3X9pRbnivw1Dcsii0Ma9ai5ddMI2zWLHMR1hq0buiWcY66EZShsluVkDTewFHzTLfOdIMYX3WTDFyAPXjVoTFdIuwD/AYWnBBzIAMAAA==', 'claimed': False, 'claimed_bidders': [], 'highest_bid_amount': 0, 'last_updated': 1688410965138, 'bin': True, 'bids': [], 'item_uuid': 'b39ae7ed9f7b43d694fd5a132938e23c'}
    test2 = {'uuid': 'e44cac6073924c55ad41f7a3ada3ec5a', 'auctioneer': '921549aea0ca4170b51a36140e63b07b', 'profile_id': 'cb864fe100114e9ba279886bf2a3afa4', 'coop': ['921549aea0ca4170b51a36140e63b07b', '7179a4be56aa46d1837b03220ab84cb7'], 'start': 1688411326526, 'end': 1689620926526,
             'item_name': 'Ancient Final Destination Leggings',
             'item_lore': '§7Strength: §c+35 §9(+35)\n§7Crit Chance: §c+15% §9(+15%)\n§7Crit Damage: §c+32% §9(+32%)\n§7Health: §a+282 §e(+40) §9(+7)\n§7Defense: §a+147 §e(+20) §9(+7)\n§7Intelligence: §a+125 §9(+25)\n§7Health Regen: §a+10\n\n§9§d§lWisdom V\n§9Ferocious Mana V\n§9Growth V\n§9Protection V\n§9Rejuvenate V\n§9Thorns III\n\n§6Full Set Bonus: Vivacious Darkness\n§7§7Costs §32⸎ Soulflow §7per 5s\n§7in combat while §asneaking§7:\n§3⁍ §c+30❁ Strength\n§3⁍ §e+20⚔ Bonus Attack Speed\n§3⁍ §f+10✦ Speed\n§3⁍ §7Multiply §b✎ Intelligence §7by §b1.25x\n§3⁍ §c+200⫽ Ferocity §7against Endermen\n§3⁍ §a+100% §7damage against Endermen\n\n§6Piece Bonus: Enderman Bulwark\n§7Kill Endermen to accumulate\n§7defense against them.\n§7Piece Bonus: §a+310❈\n§7Next Upgrade: §a+335❈ §8(§a10,937§7/§c25,000§8)\n\n§9Ancient Bonus\n§7Grants §a+1 §9☠ Crit Damage\n§9§7per §cCatacombs §7level.\n\n§d§l§ka§r §d§l§d§lMYTHIC LEGGINGS §d§l§ka', 'extra': 'Ancient Final Destination Leggings Leather Leggings §d§lWisdom Thorns Ferocious Mana Rejuvenate Protection Growth', 'category': 'armor', 'tier': 'MYTHIC', 'starting_bid': 17900000,
             'item_bytes': 'H4sIAAAAAAAAAGVUz28aRxR+mDjBpK1TVeqPqKqmrVOZ+EeWBYzh5oDBqDaNguOqJzTsPpYpywzanTX2MbdemlMPVZVIPZVD/4H20At/Cn9I0zfsQqmKLO/Me9/M++Z930wWYAtSIgsAqQ3YEG5qPwWbNRVJncpCWnNvC+6gdAZgfim4/0L2AuRD3vMxlYatM+Fiw+deSNm/s3DPFeHY57e06FwFmKHoDnw6m5Y7OkDp6UGVzabOXqFEn8oufXPwOWVrgdCsNuDSwRiQLz2KETRYg9T5iHsJpGAnEBrk4EuCnCH34wp8zz626Yu7e0UrF8PKOdghUB37KEOMUfliOUbZayhTrSU1+r7wMGFEUDvhbBPnj1bV2HMkUAKx6LjvE2g2dWdT/1sRumrEruADCjUwUI5QUcguuOQUvE/BZqAmtMUVbNPkWaA0OloomQSe4/fRNUqukQLvUuByoAIZslarRXUezaZHjcj3WQc1e6pkFFbZlbjmcZE6D4YSwxC+IqameyrUIZEs2PM/XrGOivy+ryYUKI8xYKUQvqChkMxRox7XbDIQPpozhZK0FtKjbBU+ofXzlz/G3bfmb16ypaqm/UkKqZfzX36KKbETrbkzZJ0xogsfrkB96tX89W9JvLSKly8iX4uxf0vj3vz1K7aug8n3Fpn8oV26gcM1OrZlzX//i8Vd1gZU5h4XMtTsVLoYjFDC4xXeSGUZ95TdhaHY/7AAlD16JpDKJs2Nc1yyp5E/ofbCZ7T+a0EKLFcxrRh3nGgU+SQafGz2j922KqAHODqEh5T5z96GUoFa8uYHqFKujTeavRh7AXcT9xUKJUrS8HiXpnlrv1Iwsj6hs9ulfcuyKJMj1g/IJifSESgTUyyEbQZcLuSngxsTz3/+la3dJ3PWSmIF2rDGSTPygVlQ9vEa/UPauRibejYd8tnU4OKZ+X/x3eVZq8bOT5vNVrvZYf8i07DpKF8F8DZ6m4E7bT5CY1x3SbEhJPdZHUNNg4X1z9HzyG8hZGH79EYHnBwUiF6kMUzDdsCJ9W03iltj3hx6gx4MlO6OleZadR3zcFE4m4YskljdIQlEuMd/ZiAzUq7oCwzgHo/rZ8yDBw8brfbJebd+2rmkwWXrm3Z3eZQsvGPePuoeyasNA+PPEanbnSxuN5XaTMNdvbiZNEmn4b3+8qp3iQCPEdlgdZmTwHh13ZM9vMVjYCZArYoiYrZz3M8fVxCtgyIvVw6KWLAOKtwpHhSLaJeP8q5bcngGtogStZCPxrBtP7Hpr8DsqlViJxcAG3A3UZl+/wC+q9ju7gUAAA==', 'claimed': False, 'claimed_bidders': [], 'highest_bid_amount': 0, 'last_updated': 1688411326526, 'bin': True, 'bids': [], 'item_uuid': '8f189ee04a794e309ac444e2761dd5ca'}
    print(ENCHANTS)
    print(BAZAAR_PRICES)
    item = Item(test)
    print(item.get_reforge_price())
