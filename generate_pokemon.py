import datetime
from pokemon_data import Pokemon
from parsers import parse_full_moves,parse_full_abilities
import json
from random import randint

import math

if __name__ == "__main__":
    roll_to_stat = {
        1: "HP",
        2: "ATK",
        3: "DEF",
        4: "SPATK",
        5: "SPDEF",
        6: "SPD"
    }

    NATURE_MATRIX = {
        "HP": {
            "ATK": "Cuddly (+HP/-ATK)",
            "DEF": "Distracted (+HP/-DEF)",
            "SPATK": "Proud (+HP/-SPATK)",
            "SPDEF": "Decisive (+HP/-SPDEF)",
            "SPD": "Patient (+HP/-SPD)",
            "HP": "Neutral (+HP/-HP)",
        },

        "ATK": {
            "HP": "Desperate (+ATK/-HP)",
            "DEF": "Lonely (+ATK/-DEF)",
            "SPATK": "Adamant (+ATK/-SPATK)",
            "SPDEF": "Naughty (+ATK/-SPDEF)",
            "SPD": "Brave (+ATK/-SPD)",
            "ATK": "Neutral (+ATK/-ATK)",
        },

        "DEF": {
            "HP": "Stark (+DEF/-HP)",
            "ATK": "Bold (+DEF/-ATK)",
            "SPATK": "Impish (+DEF/-SPATK)",
            "SPDEF": "Lax (+DEF/-SPDEF)",
            "SPD": "Relaxed (+DEF/-SPD)",
            "DEF": "Neutral (+DEF/-DEF)",
        },

        "SPATK": {
            "HP": "Curious (+SPATK/-HP)",
            "ATK": "Modest (+SPATK/-ATK)",
            "DEF": "Mild (+SPATK/-DEF)",
            "SPDEF": "Rash (+SPATK/-SPDEF)",
            "SPD": "Quiet (+SPATK/-SPD)",
            "SPATK": "Neutral (+SPATK/-SPATK)",
        },

        "SPDEF": {
            "HP": "Dreamy (+SPDEF/-HP)",
            "ATK": "Calm (+SPDEF/-ATK)",
            "DEF": "Gentle (+SPDEF/-DEF)",
            "SPATK": "Careful (+SPDEF/-SPATK)",
            "SPD": "Sassy (+SPDEF/-SPD)",
            "SPDEF": "Neutral (+SPDEF/-SPDEF)",
        },

        "SPD": {
            "HP": "Skittish (+SPD/-HP)",
            "ATK": "Timid (+SPD/-ATK)",
            "DEF": "Hasty (+SPD/-DEF)",
            "SPATK": "Jolly (+SPD/-SPATK)",
            "SPDEF": "Naive (+SPD/-SPDEF)",
            "SPD": "Neutral (+SPD/-SPD)",
        },
    }
    input_jsons = "data/pokemon.json"
    with open(input_jsons, "r", encoding="utf-8") as f:
        raw_data = json.load(f)
    pokemons = [Pokemon.from_dict(p) for p in raw_data]
    moves_by_name = parse_full_moves("data/Moves.html")
    abilities_by_name = parse_full_abilities("data/Abilities.pdf")

    pokemon_to_find = input("Please enter the name of the pokemon : ")

    found=False
    pokemon = None

    for pokemon_temp in pokemons:
        if pokemon_temp.name == pokemon_to_find.lower():
            found = True
            pokemon = pokemon_temp

    if not found or pokemon is None:
        print("Pokemon not found, here is a list of pokemon by name :")
        for pokemon_t in pokemons:
            print(pokemon_t.name)
        exit()


    level = -1
    while level <= 0 :
        level = int(input("Please input the level of the pokemon : "))
    pokemon_rarity = ""
    while pokemon_rarity not in ["Normal","Shiny","Platine"]:
        pokemon_rarity = input("Please input the pokemon rarity (Normal, Shiny or Platine) : ")
    pokemon_card = ""
    while pokemon_card not in ["None","Normal","Shiny","Platine"]:
        pokemon_card = input("Please input the pokemon card (None, Normal, Shiny or Platine) : ")
    gender = ""
    if pokemon.gender_ratio_f == -1 or pokemon.gender_ratio_m == -1:
        print("Gender is not determined by a roll")
        gender = "Unknown"
    else:
        print("Rolling gender using pokemon ratios ... ")
        male_max_roll = float(pokemon.gender_ratio_m)
        is_male = randint(0, 100) <= male_max_roll
        gender = "Male" if is_male else "Female"
    print(f"Your pokemon gender is {gender}")

    print("Choosing pokemon nature : \n\n")
    print("Here are the pokemon stats: ")
    print(f" hp = {pokemon.stat_hp}")
    print(f" attack = {pokemon.stat_atk}")
    print(f" defense = {pokemon.stat_def}")
    print(f" sp attack = {pokemon.stat_sp_atk}")
    print(f" sp defense = {pokemon.stat_sp_def}")
    print(f" speed = {pokemon.stat_spd}")
    bool_choosing_nature = False
    choosing_nature = ""
    while choosing_nature != "y" and choosing_nature != "n":
        choosing_nature = input("Do you want to choose the nature yourself ? Y / N , if N , 3 natures will be randomly rolled, and you will pick. : ")
        if choosing_nature != "y" and choosing_nature != "n":
            print("Please input y or n")
    bool_choosing_nature = (choosing_nature.strip().lower() == "y")
    if bool_choosing_nature:
        chosen_nature = ""
        while chosen_nature == "":
            final_buffed_stat = input("Please enter the chosen nature buffed stat in [HP, ATK, DEF, SPDEF, SPATK , SPD] : ")
            final_lowered_stat = input("Please enter the chosen nature lowered stat in [HP, ATK, DEF, SPDEF, SPATK , SPD] : ")
            if final_buffed_stat in NATURE_MATRIX:
                if final_lowered_stat in NATURE_MATRIX[final_buffed_stat]:
                    chosen_nature = NATURE_MATRIX[final_buffed_stat][final_lowered_stat]
        print(" You chose "+chosen_nature)
    else:
        print("Rolling the 3 choices for for nature : ")
        bonus_choice_1 = roll_to_stat[randint(1,6)]
        malus_choice_1 = roll_to_stat[randint(1,6)]
        bonus_choice_2 = roll_to_stat[randint(1,6)]
        malus_choice_2 = roll_to_stat[randint(1,6)]
        bonus_choice_3 = roll_to_stat[randint(1,6)]
        malus_choice_3 = roll_to_stat[randint(1,6)]
        nature_choice_1 = NATURE_MATRIX[bonus_choice_1][malus_choice_1]
        nature_choice_2 = NATURE_MATRIX[bonus_choice_2][malus_choice_2]
        nature_choice_3 = NATURE_MATRIX[bonus_choice_3][malus_choice_3]
        final_buffed_stat = ""
        final_lowered_stat = ""
        chosen_nature = ""
        print("Rolled nature 1 : "+nature_choice_1)
        print("Rolled nature 2 : "+nature_choice_2)
        print("Rolled nature 3 : "+nature_choice_3)
        choice = ""
        while choice not in ["1","2","3"]:
            choice = input("Choose your nature 1 , 2 or 3 : ")
        if choice == "1":
            print("you chose nature : "+nature_choice_1)
            final_buffed_stat = bonus_choice_1
            final_lowered_stat = malus_choice_1
            chosen_nature = nature_choice_1
        if choice == "2":
            print("you chose nature : "+nature_choice_2)
            final_buffed_stat = bonus_choice_2
            final_lowered_stat = malus_choice_2
            chosen_nature = nature_choice_2
        if choice == "3":
            print("you chose nature : "+nature_choice_3)
            final_buffed_stat = bonus_choice_3
            final_lowered_stat = malus_choice_3
            chosen_nature = nature_choice_3
    type_str = ""
    for typep in pokemon.pokemon_types:
        type_str += typep+","
    type_str = type_str[:-1]
    final_str = f"# {pokemon.name}\n"
    final_str+= f"\n"
    final_str+= f"Card: {pokemon_card}\n"
    final_str+= f"Gender: {gender}\n"
    final_str+= f"Item: \n"
    final_str+= f"Nature: {chosen_nature}\n"
    final_str+= f"Level: {level}\n"
    final_str+= f"Rarity: {pokemon_rarity}\n"
    final_str+= f"Type: {type_str}\n"
    final_str+= f"Weight: {pokemon.weight}\n"
    final_str+= f"\n"
    final_str+= f"## **Abilities**\n"
    final_str+= f"\n"

    print("Rolling pokemon abilities ")
    final_str+= f"| **Ability** | **Effect** |\n"
    final_str+= f"| ---------------- | ------------------ |\n"
    ability_choice=randint(0,len(pokemon.base_abilities)-1)
    print("Rolled basic ability : "+pokemon.base_abilities[ability_choice])
    final_str+= f"| {pokemon.base_abilities[ability_choice]} | {abilities_by_name[pokemon.base_abilities[ability_choice]].effect if pokemon.base_abilities[ability_choice] in abilities_by_name else ""} |\n"
    if level >= 20  and len(pokemon.advanced_abilities) > 0:
        print("Rolling advanced ability")
        advanced_ability_choice = randint(0,len(pokemon.advanced_abilities)-1)
        print("Rolled advanced ability : "+pokemon.advanced_abilities[advanced_ability_choice])
        final_str += f"| {pokemon.advanced_abilities[advanced_ability_choice]} | {abilities_by_name[pokemon.advanced_abilities[advanced_ability_choice]].effect if pokemon.advanced_abilities[advanced_ability_choice] in abilities_by_name else ""} |\n"
    if level >= 40 and len(pokemon.high_abilities) > 0:
        print("Rolling high ability")
        high_ability_choice = randint(0,len(pokemon.high_abilities)-1)
        print("Rolled high ability : "+pokemon.high_abilities[high_ability_choice])
        final_str += f"| {pokemon.high_abilities[high_ability_choice]} | {abilities_by_name[pokemon.high_abilities[high_ability_choice]].effect if pokemon.high_abilities[high_ability_choice] in abilities_by_name else ""} | \n"


    points_to_give = 10+level
    print("Here are the pokemon stats: ")
    print(f" hp = {pokemon.stat_hp}")
    print(f" attack = {pokemon.stat_atk}")
    print(f" defense = {pokemon.stat_def}")
    print(f" sp attack = {pokemon.stat_sp_atk}")
    print(f" sp defense = {pokemon.stat_sp_def}")
    print(f" speed = {pokemon.stat_spd}")
    point_in_hp = -1
    point_in_atk = -1
    point_in_def = -1
    point_in_spatk = -1
    point_in_spdef = -1
    point_in_speed = -1
    stop = False
    print("Give the pokemon point")
    while point_in_hp < 0 and point_in_hp <= points_to_give and not stop:
        point_in_hp = input("Please input the number of point in HP stat (max "+str(points_to_give)+"). If you want the code to automatically set points, enter 'default': ")
        if point_in_hp == "default":
            stop = True
            break
        point_in_hp = int(point_in_hp)
        if point_in_hp < 0:
            print("Please input a positive point number")
            point_in_hp = -1
        if point_in_hp > points_to_give:
            print("you can't give more point than you have ("+str(points_to_give)+")")
            point_in_hp = -1
    if not stop:
        points_to_give = points_to_give - point_in_hp

    while point_in_atk < 0 and point_in_atk <= points_to_give and not stop:
        point_in_atk = input("Please input the number of point in ATK stat (max "+str(points_to_give)+"). If you want the code to automatically set points, enter 'default': ")
        if point_in_atk == "default":
            stop = True
            break
        point_in_atk = int(point_in_atk)
        if point_in_atk < 0:
            print("Please input a positive point number")
            point_in_atk = -1
        if point_in_atk > points_to_give:
            print("you can't give more point than you have ("+str(points_to_give)+")")
            point_in_atk = -1
    if not stop:
        points_to_give = points_to_give - point_in_atk

    while point_in_def < 0 and point_in_def <= points_to_give and not stop:
        point_in_def = input("Please input the number of point in DEF stat (max "+str(points_to_give)+"). If you want the code to automatically set points, enter 'default': ")
        if point_in_def == "default":
            stop = True
            break
        point_in_def = int(point_in_def)
        if point_in_def < 0:
            print("Please input a positive point number")
            point_in_def = -1
        if point_in_def > points_to_give:
            print("you can't give more point than you have ("+str(points_to_give)+")")
            point_in_def = -1
    if not stop:
        points_to_give = points_to_give - point_in_def

    while point_in_spatk < 0 and point_in_spatk <= points_to_give and not stop:
        point_in_spatk = input("Please input the number of point in SP ATK stat (max "+str(points_to_give)+"). If you want the code to automatically set points, enter 'default' : ")
        if point_in_spatk == "default":
            stop = True
            break
        point_in_spatk = int(point_in_spatk)
        if point_in_spatk < 0:
            print("Please input a positive point number")
            point_in_spatk = -1
        if point_in_spatk > points_to_give:
            print("you can't give more point than you have ("+str(points_to_give)+")")
            point_in_spatk = -1
    if not stop:
        points_to_give = points_to_give - point_in_spatk


    while point_in_spdef < 0 and point_in_spdef <= points_to_give and not stop:
        point_in_spdef = input("Please input the number of point in SP DEF stat (max "+str(points_to_give)+"). If you want the code to automatically set points, enter 'default': ")
        if point_in_spdef == "default":
            stop = True
            break
        point_in_spdef = int(point_in_spdef)
        if point_in_spdef < 0:
            print("Please input a positive point number")
            point_in_spdef = -1
        if point_in_spdef > points_to_give:
            print("you can't give more point than you have ("+str(points_to_give)+")")
            point_in_spdef = -1
    if not stop:
        points_to_give = points_to_give - point_in_spdef

    while point_in_speed < 0 and point_in_speed <= points_to_give and not stop:
        point_in_speed = input("Please input the number of point in SPEED stat (max "+str(points_to_give)+"). If you want the code to automatically set points, enter 'default': ")
        if point_in_speed == "default":
            stop = True
            break
        point_in_speed = int(point_in_speed)
        if point_in_speed < 0:
            print("Please input a positive point number")
            point_in_speed = -1
        if point_in_speed > points_to_give:
            print("you can't give more point than you have ("+str(points_to_give)+")")
            point_in_speed = -1
    if not stop:
        points_to_give = points_to_give - point_in_speed

    if stop:
        points_to_give = 10 + level
        init_points_to_give = points_to_give
        sum_pokepoints = pokemon.stat_hp + pokemon.stat_atk + pokemon.stat_def + pokemon.stat_sp_atk + pokemon.stat_sp_def + pokemon.stat_spd
        print("Points to give = "+str(points_to_give))
        point_in_hp = -1
        point_in_atk = -1
        point_in_def = -1
        point_in_spatk = -1
        point_in_spdef = -1
        point_in_speed = -1
        hp_weight = float(pokemon.stat_hp) / float(sum_pokepoints)
        print("hp weight = ")
        print(hp_weight)
        atk_weight = float(pokemon.stat_atk) / float(sum_pokepoints)
        print("atk weight = ")
        print(atk_weight)
        def_weight = float(pokemon.stat_def) / float(sum_pokepoints)
        print("def weight = ")
        print(def_weight)
        spatk_weight = float(pokemon.stat_sp_atk) / float(sum_pokepoints)
        print("spatk weight = ")
        print(spatk_weight)
        spdef_weight = float(pokemon.stat_sp_def) / float(sum_pokepoints)
        print("spdef weight = ")
        print(spdef_weight)
        spd_weight = float(pokemon.stat_spd) / float(sum_pokepoints)
        print("spd weight = ")
        print(spd_weight)
        point_in_hp = int(init_points_to_give*hp_weight)
        print("Given "+str(point_in_hp)+" points in hp")
        points_to_give = points_to_give - point_in_hp
        point_in_atk = int(init_points_to_give * atk_weight)
        print("Given "+str(point_in_atk)+" points in atk")
        points_to_give = points_to_give - point_in_atk
        point_in_def = int(init_points_to_give * def_weight)
        print("Given "+str(point_in_def)+" points in def")
        points_to_give = points_to_give - point_in_def
        point_in_spatk = int(init_points_to_give * spatk_weight)
        print("Given "+str(point_in_spatk)+" points in sp atk")
        points_to_give = points_to_give - point_in_spatk
        point_in_spdef = int(init_points_to_give * spdef_weight)
        print("Given "+str(point_in_spdef)+" points in sp def")
        points_to_give = points_to_give - point_in_spdef
        point_in_speed = int(init_points_to_give * spd_weight)
        print("Given "+str(point_in_speed)+" points in sp speed")
        points_to_give = points_to_give - point_in_speed
        print("Remaining point : "+str(points_to_give))
        print("Those remaining points will be spread using weights")
        roll_for_hp = int(hp_weight*100)
        roll_for_atk = int(atk_weight*100)+roll_for_hp
        roll_for_def = int(def_weight*100)+roll_for_atk
        roll_for_spatk = int(spatk_weight*100)+roll_for_def
        roll_for_spdef = int(spdef_weight*100)+roll_for_spatk
        roll_for_speed = min(100,int(spd_weight*100)+roll_for_spdef)
        while points_to_give > 0:
            roll = randint(1,100)
            if roll < roll_for_hp:
                print("Added 1 remaining point to HP")
                point_in_hp += 1
                points_to_give -= 1
            elif roll < roll_for_atk:
                print("Added 1 remaining point to ATK")
                point_in_atk += 1
                points_to_give -= 1
            elif roll < roll_for_def:
                print("Added 1 remaining point to DEF")
                point_in_def += 1
                points_to_give -= 1
            elif roll < roll_for_spatk:
                print("Added 1 remaining point to SPATK")
                point_in_spatk += 1
                points_to_give -= 1
            elif roll < roll_for_spdef:
                print("Added 1 remaining point to SPDEF")
                point_in_spdef += 1
                points_to_give -= 1
            elif roll < roll_for_speed:
                print("Added 1 remaining point to SPD")
                point_in_spdef += 1
                points_to_give -= 1



    bonus_point_in_hp = 0
    bonus_point_in_atk = 0
    bonus_point_in_def = 0
    bonus_point_in_spatk = 0
    bonus_point_in_spdef = 0
    bonus_point_in_speed = 0
    bonus_point_to_nature_stat = 1
    if pokemon_card != "None":
        if pokemon_card == "Normal":
            bonus_point_in_hp += 1
            bonus_point_in_atk += 1
            bonus_point_in_def += 1
            bonus_point_in_spatk += 1
            bonus_point_in_spdef += 1
            bonus_point_in_speed += 1
            bonus_point_to_nature_stat += 1
        elif pokemon_card == "Shiny":
            bonus_point_in_hp += 2
            bonus_point_in_atk += 2
            bonus_point_in_def += 2
            bonus_point_in_spatk += 2
            bonus_point_in_spdef += 2
            bonus_point_in_speed += 2
            bonus_point_to_nature_stat += 1
        elif pokemon_card == "Platine":
            bonus_point_in_hp += 3
            bonus_point_in_atk += 3
            bonus_point_in_def += 3
            bonus_point_in_spatk += 3
            bonus_point_in_spdef += 3
            bonus_point_in_speed += 3
            bonus_point_to_nature_stat += 1
    if pokemon_rarity == "Shiny":
        bonus_point_in_hp += 2
        bonus_point_in_atk += 2
        bonus_point_in_def += 2
        bonus_point_in_spatk += 2
        bonus_point_in_spdef += 2
        bonus_point_in_speed += 2
    elif pokemon_rarity == "Platine":
        bonus_point_in_hp += 4
        bonus_point_in_atk += 4
        bonus_point_in_def += 4
        bonus_point_in_spatk += 4
        bonus_point_in_spdef += 4
        bonus_point_in_speed += 4

    if final_buffed_stat == "HP":
        bonus_point_in_hp += bonus_point_to_nature_stat
    if final_buffed_stat == "ATK":
        bonus_point_in_atk += bonus_point_to_nature_stat
    if final_buffed_stat == "DEF":
        bonus_point_in_def += bonus_point_to_nature_stat
    if final_buffed_stat == "SPATK":
        bonus_point_in_spatk += bonus_point_to_nature_stat
    if final_buffed_stat == "SPDEF":
        bonus_point_in_spdef += bonus_point_to_nature_stat
    if final_buffed_stat == "SPD":
        bonus_point_in_speed += bonus_point_to_nature_stat

    if final_lowered_stat == "HP":
        bonus_point_in_hp = bonus_point_in_hp-bonus_point_to_nature_stat
    if final_lowered_stat == "ATK":
        bonus_point_in_atk =bonus_point_in_atk-bonus_point_to_nature_stat
    if final_lowered_stat == "DEF":
        bonus_point_in_def = bonus_point_in_def - bonus_point_to_nature_stat
    if final_lowered_stat == "SPATK":
        bonus_point_in_spatk = bonus_point_in_spatk - bonus_point_to_nature_stat
    if final_lowered_stat == "SPDEF":
        bonus_point_in_spdef = bonus_point_in_spdef - bonus_point_to_nature_stat
    if final_lowered_stat == "SPD":
        bonus_point_in_speed = bonus_point_in_speed - bonus_point_to_nature_stat
    final_str += f"\n"
    final_str += f"\n"
    final_str += f"## **Capabilities**\n"
    final_str += f"\n"
    final_str+= f"| **Capability** | **Value** |\n"
    final_str+= f"| ---------------- | ------------------ |\n"
    for cat in pokemon.capabilities:
        if cat["name"] != "":
            final_str += f"| {cat["name"]} | {cat["value"]} | \n"
    final_str += f"\n"
    final_str += f"\n"
    final_str += f"## **Skills**\n"
    final_str += f"\n"
    final_str+= f"| **Skill** | **Roll** |\n"
    final_str+= f"| ---------------- | ------------------ |\n"
    for cat in pokemon.skills:
        if cat["name"] != "":
            final_str += f"| {cat["name"]} | {cat["roll"]} | \n"
    final_str += f"\n"
    final_str += f"\n"
    final_str += f"## **Stats**\n"
    final_str += f"\n"
    sum_hp = max(0,pokemon.stat_hp+bonus_point_in_hp+point_in_hp)
    sum_atk = max(0,pokemon.stat_atk+bonus_point_in_atk+point_in_atk)
    sum_def = max(0,pokemon.stat_def+bonus_point_in_def+point_in_def)
    sum_spatk = max(0,pokemon.stat_sp_atk+bonus_point_in_spatk+point_in_spatk)
    sum_spdef = max(0,pokemon.stat_sp_def+bonus_point_in_spdef+point_in_spdef)
    sum_speed = max(0,pokemon.stat_spd+bonus_point_in_speed+point_in_speed)
    hit_points = int(level+(3*(sum_hp))+10)
    final_str += f"| **Hit Points Max :{hit_points}**                           | **Hit Points: {hit_points}/{hit_points}** |\n"
    final_str += f"|------------------------------------------------------------|------------------------------------------|\n"
    final_str += f"| **Max HP**: {pokemon.stat_hp}+{bonus_point_in_hp}+{point_in_hp}={sum_hp}              | **Current HP**:{sum_hp}                  |\n".replace("+-","-")
    final_str += f"| **Max ATK**: {pokemon.stat_atk}+{bonus_point_in_atk}+{point_in_atk}={sum_atk}              | **Current ATK**:{sum_atk}                  |\n".replace("+-","-")
    final_str += f"| **Max DEF**: {pokemon.stat_def}+{bonus_point_in_def}+{point_in_def}={sum_def}              | **Current DEF**:{sum_def}                  |\n".replace("+-","-")
    final_str += f"| **Max SP.ATK**: {pokemon.stat_sp_atk}+{bonus_point_in_spatk}+{point_in_spatk}={sum_spatk}              | **Current SP.ATK**:{sum_spatk}                  |\n".replace("+-","-")
    final_str += f"| **Max SP.DEF**: {pokemon.stat_sp_def}+{bonus_point_in_spdef}+{point_in_spdef}={sum_spdef}              | **Current SP.DEF**:{sum_spdef}                  |\n".replace("+-","-")
    final_str += f"| **Max SPEED**: {pokemon.stat_spd}+{bonus_point_in_speed}+{point_in_speed}={sum_speed}              | **Current SPEED**:{sum_speed}                  |\n".replace("+-","-")
    final_str += f"\n"
    phy_evade = int(sum_def/10)
    spe_evade = int(sum_spdef/10)
    speed_evade = int(sum_speed/10)
    injuries = 0
    final_str += f"| **Derived stats** |                |\n"
    final_str += f"|-------------------|----------------|\n"
    final_str += f"| Phys Evade        | {phy_evade}    |\n"
    final_str += f"| Spec Evade        | {spe_evade}    |\n"
    final_str += f"| Speed Evade       | {speed_evade}  |\n"
    final_str += f"| Injuries          | {injuries}     |\n"
    final_str += f"\n"
    final_str += f"*Pokémon Hit Points = Pokémon Level + (HP x3) + 10*\n"
    final_str += f"\n"
    final_str += f"## **Moves** :\n"
    final_str += f"\n"
    final_str += f"| **Move**    | **Freq**         | **AC**    | **Type**    | **Roll**    | **Dmg. Type**      | **Range**    | **Special Effect** |\n"
    final_str += f"|-------------|------------------|-----------|-------------|-------------|--------------------|--------------|-------------------|\n"
    poke_moves = reversed(sorted(pokemon.moves, key=lambda item: item["level"]))
    filtered_moves = [m for m in poke_moves if int(m["level"]) <= level]
    #filtered_moves = filtered_moves[:6]
    print("here is the list of move available for the pokemon : ")
    for move in filtered_moves:
        if move["name"] in moves_by_name:
            print(f"| {move["name"]} | {moves_by_name[move["name"]].get_frequency()} | {moves_by_name[move["name"]].get_AC()} | {moves_by_name[move["name"]].get_type()} | {moves_by_name[move["name"]].get_roll()} | {moves_by_name[move["name"]].get_classe()} | {moves_by_name[move["name"]].get_range()} | {moves_by_name[move["name"]].get_effect()}     |")
    chosen_moves = []
    current_move = ""
    while current_move != "stop" and current_move != "default" and len(chosen_moves) < 6:
        current_move = input("Please input a move to add by name (case sensitive). If you want to stop, write stop. If you want the tool to fill automatically, input 'default' : ")
        if current_move != "stop" and current_move != "default":
            for move_f in filtered_moves:
                if move_f["name"] == current_move:
                    chosen_moves.append(move_f)
            current_move = ""
        if current_move == "default":
            chosen_moves = filtered_moves[:6]
            break
    print(chosen_moves)
    for move in chosen_moves:
        if move["name"] in moves_by_name:
            final_str += f"| {move["name"]} | {moves_by_name[move["name"]].get_frequency()} | {moves_by_name[move["name"]].get_AC()} | {moves_by_name[move["name"]].get_type()} | {moves_by_name[move["name"]].get_roll()} | {moves_by_name[move["name"]].get_classe()} | {moves_by_name[move["name"]].get_range()} | {moves_by_name[move["name"]].get_effect()}     |\n"
        else:
            final_str += f"| {move["name"]} |  |  |  |  |  |  |      |\n"

    egg_moves = []
    print("You will now choose egg moves. Here is the list of availables ones : ")
    for move in pokemon.egg_moves:
        print(move + " , ")
    current_egg_move = ""
    while current_egg_move != "stop" and len(egg_moves) < 3:
        current_egg_move = input("Please input the egg move name (case sensitive). If you want to stop, please enter 'stop'")
        if current_egg_move != "stop":
            for move_name in moves_by_name:
                if move_name == current_egg_move:
                    egg_moves.append(moves_by_name[move_name])
    final_str += f"\n"
    final_str += f"|               |   |   |   |   |   |   |   |\n"
    final_str += f"|---------------| - | - | - | - | - | - | - |\n"
    added_count=0
    for move in egg_moves:
        final_str += f"| {move.name} | {move.get_frequency()} | {move.get_AC()} | {move.get_type()} | {move.get_roll()} | {move.get_classe()} | {move.get_range()} | {move.get_effect()}     |\n"
        added_count += 1
    for i in range(added_count,3):
        final_str += f"|               |   |   |   |   |   |   |   |\n"
    final_str += f"\n"
    tutor_point_count = math.floor(level/5)
    final_str += f"Tutor points = {tutor_point_count}\n"
    final_str += f"\n"
    final_str += f"\n"
    final_str += f"## **Notes**\n"
    final_str += f"\n"
    final_str += f"egg move :todo\n"
    now = datetime.datetime.now()
    f = open(pokemon.name+"_"+str(now.strftime("%s"))+".md","w+")
    f.write(final_str)
    f.close()