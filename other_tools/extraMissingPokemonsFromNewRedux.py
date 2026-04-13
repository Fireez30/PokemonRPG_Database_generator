import json
import os,sys
import math
from parsers import to_serializable
from pokemon_data import accepted_classes,accepted_ACs,accepted_freqs,accepted_types


with open("../data/reduxData_last.json", "r") as f:
    data = json.load(f)

with open("../output/finals/abilities.json","r") as f:
    final_abilities = json.load(f)

with open("../output/finals/moves.json","r") as f:
    final_moves = json.load(f)
new_pokemons = []
redux_mons = []
with open("../output/initials/pokemons.json","r") as f:
    pokemons = json.load(f)
for mon in data["species"]:
    if mon["name"] != "??????????":
        #   < ---- Name ---- >
        pokemon_name = mon["name"].strip()
        #   < ---- Stats ---- >
        stat_hp = round(float(mon["stats"]["base"][0])/10)
        stat_atk = round(float(mon["stats"]["base"][1])/10)
        stat_def = round(float(mon["stats"]["base"][2])/10)
        stat_spatk = round(float(mon["stats"]["base"][3])/10)
        stat_spdef = round(float(mon["stats"]["base"][4])/10)
        stat_speed = round(float(mon["stats"]["base"][5])/10)
        #   < ---- Type ---- >
        types = []
        if len(mon["stats"]["types"]) == 1:
                types = data["typeT"][mon["stats"]["types"][0]]
        elif len(mon["stats"]["types"]) > 1:
            for typem in mon["stats"]["types"]:
                if not data["typeT"][typem] in types:
                    types.append(data["typeT"][typem])
        #   < ---- Abilities ---- >
        base_abilities = []
        adv_abilities = []
        high_abilities = []
        if "inns" in mon["stats"].keys():
            inns_ids = mon["stats"]["inns"]
            #print(inns_ids)
            for id_i in inns_ids:
                exist = list(filter(lambda x:"id" in x.keys() and x["id"] == int(id_i), final_abilities))
                if len(exist) > 0:
                    if len(base_abilities) < 2:
                        base_abilities.append(exist[0]["name"])
                    elif len(adv_abilities) < 3:
                        adv_abilities.append(exist[0]["name"])
                    else:
                        high_abilities.append(exist[0]["name"])
        if "abis" in mon["stats"].keys():
            inns_ids = mon["stats"]["abis"]
            for id_i in inns_ids:
                exist = list(filter(lambda x:"id" in x.keys() and x["id"] == int(id_i), final_abilities))
                if len(exist) > 0:
                    if len(base_abilities) < 2:
                        base_abilities.append(exist[0]["name"])
                    elif len(adv_abilities) < 3:
                        adv_abilities.append(exist[0]["name"])
                    else:
                        high_abilities.append(exist[0]["name"])
        #   < ---- Evolutions ---- >
        evolutions = []
        evolutions.append("TBD")
        to_work = []
        """
        found_evos = [x for x in mon["evolutions"] if x["kd"] == 0]
        for evo in found_evos:
            pokeexist = list(filter(lambda x: x["id"] == evo["in"], data["species"]))
            if len(pokeexist) > 0:
                name_to_add = pokeexist[0]["name"]+" Minimum "+str(evo["rs"])
                if name_to_add not in evolutions:
                    evolutions.append(name_to_add)
                    to_work.append(pokeexist[0]["id"])

        for idmon in to_work:
            pokeobj = list(filter(lambda x: x["id"] == idmon, data["species"]))
            if len(pokeobj) > 0:
                found_evos = [x for x in pokeobj[0]["evolutions"] if x["kd"] == 0]
                for evo in found_evos:
                    pokeexist = list(filter(lambda x: x["id"] == evo["in"], data["species"]))
                    if len(pokeexist) > 0:
                        name_to_add = pokeexist[0]["name"] + " Minimum " + str(evo["rs"])
                        if name_to_add not in evolutions:
                            evolutions.append(name_to_add)
        """
        # for poke , evolutions. Get all with kd = 0

        #   < ---- TM Moves ---- >
        tm_moves = []
        if len(mon["TMHMMoves"]) > 0:
            for id_tm in mon["TMHMMoves"]:
                move_exist = list(filter(lambda x: "id" in x.keys() and x["id"] == id_tm, final_moves))
                if len(move_exist) > 0:
                    tm_moves.append(str(move_exist[0]["move"].capitalize()))
        #   < ---- Tutor Moves ---- >
        tutor = []
        if len(mon["tutor"]) > 0:
            for id_tm in mon["tutor"]:
                move_exist = list(filter(lambda x: "id" in x.keys() and x["id"] == id_tm, final_moves))
                if len(move_exist) > 0:
                    tutor.append(str(move_exist[0]["move"].capitalize()))
        #   < ---- Tutor Moves ---- >
        egg_moves = []
        if len(mon["eggMoves"]) > 0:
            for id_tm in mon["eggMoves"]:
                move_exist = list(filter(lambda x: "id" in x.keys() and x["id"] == id_tm, final_moves))
                if len(move_exist) > 0:
                    egg_moves.append(str(move_exist[0]["move"].capitalize()))

        height = ""
        weight = ""
        gender_ratio_m = ""
        gender_ratio_f = ""
        egg_group = ""
        average_hatch_rate = -1
        diet = ""
        habitat = ""
        capabilities = []
        skills = []
        #   < ---- extracted from normal ---- >
        matching_poke_name = pokemon_name.strip().lower().replace("redux_", "").replace("redux", "").replace("alola_",
                                                                                                             "").replace(
            "alola", "").replace("hisuian_", "").replace("hisuian", "").replace("therian_", "").replace("therian",
                                                                                                        "").strip()
        found_matchings = list(filter(lambda x: x["name"] == matching_poke_name, pokemons))
        if len(found_matchings) == 0:
            matching_poke_name = \
            pokemon_name.strip().lower().replace("redux_", "").replace("redux", "").replace("alola_", "").replace(
                "alola", "").replace("hisuian_", "").replace("hisuian", "").replace("therian_", "").replace("therian",
                                                                                                            "").strip().split(
                " ")[0]
            found_matchings = list(filter(lambda x: x["name"] == matching_poke_name, pokemons))
        if len(found_matchings) > 0:
            pokeobj = found_matchings[0]
            height = pokeobj["height"]
            weight = pokeobj["weight"]
            gender_ratio_m = pokeobj["gender_ratio_m"]
            gender_ratio_f = pokeobj["gender_ratio_f"]
            egg_group = pokeobj["egg_group"]
            average_hatch_rate = pokeobj["average_hatch_rate"]
            diet = pokeobj["diet"]
            habitat = pokeobj["habitat"]
            capabilities = pokeobj["capabilities"]
            skills = pokeobj["skills"]
        #   < ---- Moves ---- >
        pokemoves = []
        for move_oj in mon["levelUpMoves"]:
            move_id = move_oj["id"]
            move_level = move_oj["lv"]
            move_exist = list(filter(lambda x: "id" in x.keys() and x["id"] == move_id, final_moves))
            if len(move_exist) > 0:
                pokemoves.append({"name": move_exist[0]["move"], "level": move_level, "type": move_exist[0]["type"]})
        uncorrect_types = False
        for ptype in types:
            if ptype not in accepted_types:
                uncorrect_types = True

        pokemon_to_add = {
            "name": pokemon_name.lower(),
            "stat_hp": stat_hp,
            "stat_atk": stat_atk,
            "stat_def": stat_def,
            "stat_sp_atk": stat_spatk,
            "stat_sp_def": stat_spdef,
            "stat_spd": stat_speed,
            "pokemon_types": types,
            "base_abilities":base_abilities,
            "advanced_abilities": adv_abilities,
            "high_abilities": high_abilities,
            "evolutions": evolutions,
            "height": height,
            "weight": weight,
            "gender_ratio_m": gender_ratio_m,
            "gender_ratio_f": gender_ratio_f,
            "egg_group": egg_group,
            "average_hatch_rate": average_hatch_rate,
            "diet": diet,
            "habitat": habitat,
            "capabilities": capabilities,
            "skills": skills,
            "moves": pokemoves,
            "tm_moves": tm_moves,
            "tutor_moves": tutor,
            "egg_moves": egg_moves,
            "mega_evolution": None
        }
        redux_mons.append(pokemon_to_add)
for rmon in redux_mons:
    mon_name = rmon["name"]
    mon_name = mon_name.replace("galarian","galar")
    mon_name = mon_name.replace("alolan","alola")
    mon_name = mon_name.replace("corvisquir","corvisquire")
    if not mon_name.lower().startswith("nidoran") and not mon_name.lower().startswith("zygarde") and not mon_name.lower().startswith("sirfetch") and not mon_name.lower().startswith("farfetch") and not mon_name.lower().startswith("tauros paldean combat breed") and not mon_name.lower().startswith("arceus"):
        already_exist = list(filter(lambda x:x["name"].lower() == mon_name.lower(), pokemons))
        if len(already_exist) == 0:
            if not ("mega " in mon_name.lower() or " mega" in mon_name.lower() or " redux" in mon_name.lower() or "redux " in mon_name.lower()):
                print("added : "+mon_name)
            new_pokemons.append(rmon)

#final_pokemons = sorted(pokemons, key = lambda x: x["name"])
final_pokemons = new_pokemons

with open("../output/finals/pokemons_redux_new.json", "w", encoding="utf-8") as f:
    json.dump(
        to_serializable(final_pokemons),
        f,
        indent=4,  # pretty print
        ensure_ascii=False
    )