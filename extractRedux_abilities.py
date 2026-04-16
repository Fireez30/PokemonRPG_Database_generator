import json
import os,sys
import math
from parsers import to_serializable
from pokemon_data import accepted_classes,accepted_ACs,accepted_freqs,accepted_types

with open("data/reduxData_last.json", "r") as f:
    data = json.load(f)

with open("output/initials/abilities.json","r") as f:
    abilities = json.load(f)
#explore_json(data)
#print("abilities before : "+str(len(abilities)))

redux_abilities = []
for ability in data["abilities"]:
    if ability["name"] != "-------":
        redux_abilities.append({"name":ability["name"],"effect":ability["desc"],"id":ability["id"],"update":"TBD"})

for rability in redux_abilities:
    already_exist = list(filter(lambda x:x["name"].lower() == rability["name"].lower(), abilities))
    if len(already_exist) == 0:
        abilities.append(rability)
    else:
        found_move = already_exist[0]
        found_move["id"] = rability["id"]

final_abilities = sorted(abilities, key = lambda x: x["name"])

with open("output/redux/abilities.json", "w", encoding="utf-8") as f_json:
    json.dump(
        to_serializable(final_abilities),
        f_json,
        indent=4,  # pretty print
        ensure_ascii=False
    )