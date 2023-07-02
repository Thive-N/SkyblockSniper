import bazaar
import utils

TOP_REFORGES = [' ✦', ' ✪', 'Ambered ', 'Ancient ', 'Auspicious ', 'Awkward ', 'Bizarre ', 'Blessed ', 'Bloody ', 'Bountiful ', 'Bulky ', 'Candied ', 'Clean ', 'Cubic ', 'Deadly ', 'Demonic ', 'Dirty ', 'Empowered ', 'Epic ', 'Fabled ', 'Fair ', 'Fast ', 'Fierce ', 'Fine ', 'Fleet ', 'Forceful ', 'Fruitful ', 'Gentle ', 'Giant ', 'Gilded ', 'Godly ', 'Grand ', 'Hasty ', 'Headstrong ', 'Heated ', 'Heavy ', 'Heroic ', 'Hurtful ', 'Itchy ', 'Jaded ', "Jerry's ", 'Keen ', 'Legendary ', 'Light ', 'Loving ', 'Lucky ', 'Magnetic ',
                'Mithraic ', 'Moil ', 'Mythic ', 'Neat ', 'Necrotic ', 'Odd ', 'Ominous ', 'Perfect ', 'Pleasant ', 'Precise ', 'Pretty ', 'Pure ', 'Rapid ', 'Refined ', 'Reinforced ', 'Renowned ', 'Rich ', 'Ridiculous ', 'Shaded ', 'Sharp ', 'Shiny ', 'Silky ', 'Simple ', 'Smart ', 'Spicy ', 'Spiked ', 'Spiritual ', 'Stellar ', 'Stiff ', 'Strange ', 'Strong ', 'Submerged ', 'Superior ', 'Suspicious ', 'Sweet ', 'Titanic ', 'Toil ', 'Undead ', 'Unpleasant ', 'Unreal ', 'Vivid ', 'Warped ', 'Warped ', 'Wise ', 'Withered ', 'Zealous ', '⚚ ', '✪']

ENCHANTS = bazaar.lower_base_enchants()

BAZAAR_PRICES = bazaar.get_all_enchants()


class Item:
    def __init__(self, raw) -> None:
        self.item = raw
        self.uuid = raw['uuid']
        self.name = raw['item_name']
        self.lore = raw['item_lore']
        self.refo = self.get_reforges()

    def is_recombobulated(self):
        return "§d§l§ka" in self.lore

    def get_reforges(self) -> dict[str, str]:
        end = {}
        for x in self.lore.split("\n"):
            for enchant in ENCHANTS:
                if enchant in x.lower() and len(x[2:].split(" ")) == 2:
                    s = x[2:].split(" ")
                    end[s[0]] = utils.roman_to_integer(s[1])

        return end

    def get_reforge_price(self) -> float:
        price: float = 0
        for reforge in self.refo:
            thing = reforge.upper().replace(" ", "_") + \
                "_" + str(self.refo[reforge])
            price += BAZAAR_PRICES[thing]
        return price

    def clean_item_price(self) -> float:
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
        for reforge in TOP_REFORGES:
            if reforge in self.name:
                return self.name.replace(reforge, "")
        return self.name

    def __str__(self) -> str:
        return self.name

    def __eq__(self, other):
        return other and self.a == other.a and self.b == other.b

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return self.uuid
