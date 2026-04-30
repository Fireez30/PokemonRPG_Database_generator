import json
import os,sys

json_pokes = "/home/benjamin/Projects/Others/FaeresDevWebsite/faeresdev-site/src/data/pokemon.json"

with open(json_pokes, "r") as f:
    data = json.load(f)

list_pokes = ""

for poke in data:
    list_pokes += poke["name"] + "\n" + "\n"
    list_pokes += "level up moves: " + "\n" + "\n"
    list_pokes += "ct / egg moves: " + "\n" + "\n"

f = open("list_pokemons.txt","w+")
f.write(list_pokes)
f.close()