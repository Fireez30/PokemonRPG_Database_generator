import json
from pokemon_data import Ability
with open("../data/reduxData_last.json", "r") as f:
    data = json.load(f)

with open("../output/finals/abilities.json", "r") as f:
    last_abilities = json.load(f)

final_abilities = []
redux_abilities = []

for ability in data["abilities"]:
    if ability["name"] != "-------":
        redux_abilities.append({"name":ability["name"],"effect":ability["desc"],"id":ability["id"],"update":"TBD"})

for rability in redux_abilities:
    already_exist = list(filter(lambda x:x["name"].lower() == rability["name"].lower(), last_abilities))
    if len(already_exist) == 0:
        final_abilities.append(Ability(rability["name"], rability["effect"],(rability["id"] if "id" in rability else -1)))

final_abilities = sorted(final_abilities, key = lambda x: x.name)

csv = "Name,Effect"
for abili in final_abilities:
    if abili is not None and abili != "":
        csv += "\n" + abili.name + ",\"" + abili.effect + "\""
f = open("../output/finals/new_redux_abilities.csv", "w+")
f.write(csv)
f.close()