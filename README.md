# skyblock sniper

a small fancy api reader
made this cause im tired of current ah flippers
will expand on this later and probably rewrite it all as it was written in an hour

# current functionalities

## item

- parse item data
- gauge item price
- infer base price with data from current bazaar data
- parse reforges and other modifiers
- infer item rarity
- parse all custom enchants

## bazaar

- parse bazaar data
- get current enchant prices since script has been ran or since the last time refresh was called

## auction

- parse auction data
- build a base price index

## utils

- roman to int
- parse all the current 5678 crafting recipes in game and put them in data.json (currently 8mbs)

all tools havent been integrated together yet

## todo

sort out item names and make them more standardised
