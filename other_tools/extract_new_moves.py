import json
import pandas as pd
import math
from pokemon_data import FullMove,ROLL_TO_DAMAGE_BASE
from parsers import to_serializable
input_csv = "../input_pdf/Move base+ New Redux + PTE séparés - moves.csv"

df = pd.read_csv(input_csv)
key_name = "Absorb_pte"
key_frequency = "At-Will"
key_ac = "3"
key_types = "Grass"
key_roll = "1d8+6"
key_class = "Spec"
key_range = "4, 1 Target "
key_effect = "Drain."
output = []
to_skip = ["Celebrate"]
for index, row in df.iterrows():
    print(row)
    if not type(row[key_name]) == float:
        if row[key_name].strip() is not None and row[key_name].strip() != "" and row[key_name] not in to_skip:
            print(row[key_name])
            move_name = row[key_name].strip().replace("_pte","")
            move_frequency = row[key_frequency].strip()
            move_ac = row[key_ac].strip()
            if "/" in row[key_types]:
                move_types = row[key_types].strip().split("/")
            else:
                move_types = [row[key_types].strip()]
            move_roll = ""
            move_damage_base = -1
            if not type(row[key_roll]) == float:
                move_roll = row[key_roll].strip()
                move_damage_base = ROLL_TO_DAMAGE_BASE()[move_roll]
            move_class = row[key_class].strip()
            if move_class == "Phys":
                move_class = "Physical"
            if move_class == "Spec":
                move_class = "Special"
            move_range = ""
            if not type(row[key_range]) == float:
                move_range = row[key_range].strip()
            move_effect = ""
            if not type(row[key_effect]) == float:
                move_effect = row[key_effect].strip()

            output.append(FullMove(name=move_name,types=move_types,frequency=move_frequency,AC=move_ac,damage_base=move_damage_base,roll=move_roll,m_class=move_class,range=move_range,effect=move_effect))
print(output)
"""
with open("../output/finals/corrected_moves.json", "w", encoding="utf-8") as f_json:
    json.dump(
        to_serializable(output),
        f_json,
        indent=2,  # pretty print
        ensure_ascii=False
    )
"""