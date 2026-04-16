import json
import os,sys
import math
from parsers import to_serializable
from pokemon_data import accepted_classes,accepted_ACs,accepted_freqs,accepted_types

with open("data/reduxData_last.json", "r") as f:
    data = json.load(f)


with open("output/initials/moves.json","r") as f:
    moves = json.load(f)
for rmove in data["moves"]:
    if rmove["name"] != "-":
        already_exist = list(filter(lambda x: x["move"].lower() == rmove["name"].lower(), moves))
        if len(already_exist) == 0:
            #   < ---- Type ---- >
            types = []
            if len(rmove["types"]) == 1:
                types = data["typeT"][rmove["types"][0]]
            elif len(rmove["types"]) > 1:
                for typem in rmove["types"]:
                    types.append(data["typeT"][typem])
            #   < ---- Frequency ---- >
            freq = "TBD"
            #   < ---- AC ---- >
            AC = "TBD"
            #   < ---- Damage Base + Roll ---- >
            damage_base = -1
            roll = "TBD"
            #   < ---- classe ---- > (split)
            classe = data["splitT"][rmove["split"]]
            #   < ---- Range ---- > (target ?)
            range = "TBD"
            #   < ---- Effect ---- > (desc ?)
            effect = rmove["desc"]
            #   < ---- Blessing ---- >
            blessing = ""
            #   < ---- Special Effect ---- >
            special_effect = ""
            #   < ---- Contest Type ---- >
            contest_type = ""
            #   < ---- Contest Effect ---- >
            contest_effect = ""
            move_to_add = {"move":rmove["name"],"type":types,"frequency":freq,"AC":AC,"roll":roll,"damage_base":damage_base,
                           "classe":classe,"range":range,"effect":effect,"blessing":blessing,"special_effect":special_effect,
                           "contest_type":contest_type,"contest_effect":contest_effect,"extra_lines":[],"id":rmove["id"]}
            moves.append(move_to_add)
        else:
            found_move = already_exist[0]
            found_move["id"] = rmove["id"]

final_moves = sorted(moves, key = lambda x: x["move"])


with open("output/redux/moves.json", "w", encoding="utf-8") as f_jsonmove:
    json.dump(
        to_serializable(final_moves),
        f_jsonmove,
        indent=4,  # pretty print
        ensure_ascii=False
    )