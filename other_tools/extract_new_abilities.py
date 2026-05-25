import json
import pandas as pd
import math
from pokemon_data import Ability
from parsers import to_serializable
input_csv = "../input_pdf/Abilities PTU + PTE + Redux - abilities.csv"

df = pd.read_csv(input_csv)
output = []
for index, row in df.iterrows():
    print(row)
    if not type(row["Unnamed: 0"]) == float and not type(row["Unnamed: 1"]) == float:
        if row["Unnamed: 0"].strip() is not None and row["Unnamed: 0"].strip() != "":
            print(row["Unnamed: 0"])
            ab_name = row["Unnamed: 0"].strip().replace("_pte","")
            ab_effect = row["Unnamed: 1"].strip()
            output.append(Ability(name=ab_name,effect=ab_effect))
with open("../output/finals/corrected_abilities.json", "w", encoding="utf-8") as f_json:
    json.dump(
        to_serializable(output),
        f_json,
        indent=2,  # pretty print
        ensure_ascii=False
    )