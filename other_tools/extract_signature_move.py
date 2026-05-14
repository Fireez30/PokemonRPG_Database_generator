from parsers import remove_html_tags
import re
from pokemon_data import FullMove

def parse_full_moves(filepath):
    pattern = r"Damage Base ([1-9]\d?):\s*(.*)"
    moves = {}
    f = open(filepath)
    lines = f.readlines()
    f.close()
    started_parsing = False
    cleaned_lines = []
    removed_lines = []
    current_str = ""
    for line in lines:
        if "Moves:" in line or "moves :" in line or "Moves :" in line or "moves:" in line:
            continue
        cleaned_line = line.replace(": ", ":").replace("Damase", "Damage").replace(" :", ":").replace("::",
                                                                                                      ":").replace(
            "\n</p>", "</p>").replace("Base Base", "Base")
        cleaned_line = cleaned_line.replace("Damage Base 9: 10:", "Damage Base 10:").replace("Damage Base: 2d10+10",
                                                                                             "Damage Base 9: 2d10+10").replace(
            "Damase Base 9: 10:", "Damase Base 10:").replace("Damase Base: 2d10+10", "Damase Base 9: 2d10+10")
        if remove_html_tags(cleaned_line.strip()).startswith("Move:"):
            cleaned_lines.append("----")
        elif "Move:" in remove_html_tags(cleaned_line.strip()) and not remove_html_tags(
                cleaned_line.strip()).startswith("Move"):
            splitted_line = remove_html_tags(cleaned_line.strip()).split("Move:")
            cleaned_lines.append(splitted_line[0])
            cleaned_lines.append("----")
            cleaned_lines.append("Move:" + splitted_line[1])
            started_parsing = True
        if (cleaned_line.strip().startswith("<p>") or cleaned_line.strip().startswith(
                "<p ") or cleaned_line.strip().startswith(
                "<h3")) and cleaned_line.strip() != "" and not started_parsing:
            current_str += cleaned_line.strip()
            started_parsing = True
        elif "/p>" in cleaned_line.strip() or "/h3>" in cleaned_line.strip() or (
                (cleaned_line.strip().startswith("<p>") or cleaned_line.strip().startswith("<p ")) and started_parsing):
            if current_str != "":
                current_str += cleaned_line.strip()
                non_html_line = remove_html_tags(current_str).strip()
                if "Frequency:" in non_html_line and not non_html_line.startswith("Frequency"):
                    splitted_line = non_html_line.split("Frequency:")
                    cleaned_lines.append(splitted_line[0])
                    cleaned_lines.append("Frequency:" + splitted_line[1])
                elif "Move:" in non_html_line and not non_html_line.startswith("Move"):
                    splitted_line = non_html_line.split("Move:")
                    cleaned_lines.append(splitted_line[0])
                    cleaned_lines.append("----")
                    cleaned_lines.append("Move:" + splitted_line[1])
                    started_parsing = True
                elif "Range:" in non_html_line and not non_html_line.startswith("Range"):
                    splitted_line = non_html_line.split("Range:")
                    if splitted_line[0].strip() != "":
                        cleaned_lines.append(splitted_line[0].strip())
                    cleaned_lines.append("Range :" + splitted_line[1])

                elif "Class:" in non_html_line and not non_html_line.startswith("Class"):
                    splitted_line = non_html_line.split("Class:")
                    if splitted_line[0].strip() != "":
                        cleaned_lines.append(splitted_line[0].strip())
                    cleaned_lines.append("Class:" + splitted_line[1])
                elif "Contest Effect:" in non_html_line and not non_html_line.startswith("Contest Effect"):
                    splitted_line = non_html_line.split("Contest Effect:")
                    if splitted_line[0].strip() != "":
                        cleaned_lines.append(splitted_line[0].strip())
                    cleaned_lines.append("Contest Effect:" + splitted_line[1])
                elif "Contest Effect :" in non_html_line and not non_html_line.startswith("Contest Effect"):
                    splitted_line = non_html_line.split("Contest Effect :")
                    if splitted_line[0].strip() != "":
                        cleaned_lines.append(splitted_line[0].strip())
                    cleaned_lines.append("Contest Effect:" + splitted_line[1])
                elif "Effect:" in non_html_line and not non_html_line.startswith(
                        "Effect") and not non_html_line.startswith("Contest Effect:"):
                    splitted_line = non_html_line.split("Effect:")
                    if splitted_line[0].strip() != "":
                        cleaned_lines.append(splitted_line[0].strip())
                    cleaned_lines.append("Effect:" + splitted_line[1])
                elif "AC:" in non_html_line and not non_html_line.startswith("AC"):
                    splitted_line = non_html_line.split("AC:")
                    if splitted_line[0].strip() != "":
                        cleaned_lines.append(splitted_line[0].strip())
                    cleaned_lines.append("AC:" + splitted_line[1])
                elif "Contest Type:" in non_html_line and not non_html_line.startswith("Contest Type"):
                    splitted_line = non_html_line.split("Contest Type:")
                    if splitted_line[0].strip() != "":
                        cleaned_lines.append(splitted_line[0].strip())
                    cleaned_lines.append("Contest Type:" + splitted_line[1])
                elif "Type:" in non_html_line and not non_html_line.startswith("Type") and not non_html_line.startswith(
                        "Contest Type:"):
                    splitted_line = non_html_line.split("Type:")
                    if splitted_line[0].strip() != "":
                        cleaned_lines.append(splitted_line[0].strip())
                    cleaned_lines.append("Type :" + splitted_line[1])
                elif re.match(pattern, non_html_line) and not non_html_line.startswith("Damage Base"):
                    matches = re.findall(pattern, non_html_line)
                    for number, description in matches:
                        cleaned_lines.append("Damage Base:" + str(number))
                        cleaned_lines.append("Roll:" + description.strip())
                    splitted_line = non_html_line.split("Damage Base")
                    class_line = non_html_line[0]
                    if class_line.strip() != "":
                        cleaned_lines.append(class_line.strip().replace("\n", ""))
                else:
                    if non_html_line.strip() != "":
                        if non_html_line.startswith("Damage Base"):
                            matches = re.findall(pattern, non_html_line)
                            for number, description in matches:
                                cleaned_lines.append("Damage Base:" + str(number))
                                cleaned_lines.append("Roll:" + description.strip())
                        else:
                            cleaned_lines.append(non_html_line.strip())
            current_str = ""
            started_parsing = False
        elif started_parsing:
            current_str += cleaned_line.strip()
        else:
            removed_lines.append(remove_html_tags(cleaned_line.strip()))

    # for cleaned_line in cleaned_lines:
    #    #print(cleaned_line)
    parsing_move = False
    bypass_current_move = False
    move_name = ""
    move_type = ""
    move_frequency = ""
    move_ac = ""
    move_damage_base = ""
    move_roll = ""
    move_classe = ""
    move_range = ""
    move_effect = ""
    move_blessing = ""
    move_special_effect = ""
    move_contest_type = ""
    move_contest_effect = ""
    move_extra_lines = []
    for cleaned_line in cleaned_lines:
        split_line = cleaned_line.split(":")
        # #print(split_line)
        if len(split_line) == 1:
            if cleaned_line.strip().startswith("----"):
                # #print("found move to store : "+move_name)
                if not bypass_current_move and move_name.strip() != "":
                    moves[move_name]=FullMove(
                             name=move_name,
                             types=[t.strip() for t in move_type.split("/") if t.strip()] if move_type else ["Normal"],
                             frequency=move_frequency,
                             AC=move_ac,
                             damage_base=int(move_damage_base) if move_damage_base.strip().lstrip('-').isdigit() else -1,
                             roll=move_roll,
                             m_class=move_classe if move_classe else "Status",
                             range=move_range,
                             effect=move_effect,
                             blessing=move_blessing if move_blessing else None,
                             special_effect=move_special_effect if move_special_effect else None,
                             contest_types=move_contest_type if move_contest_type else None,
                             contest_effect=move_contest_effect if move_contest_effect else None,
                             extra_lines=move_extra_lines)
                move_name = ""
                move_type = ""
                move_frequency = ""
                move_ac = ""
                move_roll = ""
                move_damage_base = ""
                move_classe = ""
                move_range = ""
                move_effect = ""
                move_blessing = ""
                move_special_effect = ""
                move_contest_type = ""
                move_contest_effect = ""
                move_extra_lines = []
                parsing_move = True
                bypass_current_move = False
        elif len(split_line) == 2 or (len(split_line) == 3 and split_line[-1] == ""):
            if cleaned_line.strip().startswith("Move:"):  # first time we find a move
                move_name = cleaned_line.strip().replace("Move:", "").strip()
                # #print("found move : " + move_name)
                if move_name == "":
                    bypass_current_move = True
            elif cleaned_line.strip().startswith("Type:"):
                move_type = cleaned_line.strip().replace("Type:", "").strip()
            elif cleaned_line.strip().startswith("Damage Base:"):
                move_damage_base = cleaned_line.strip().replace("Damage Base:", "").strip()
            elif cleaned_line.strip().startswith("Roll:"):
                move_roll = cleaned_line.strip().replace("Roll:", "").strip()
            elif cleaned_line.strip().startswith("Frequency:"):
                move_frequency = cleaned_line.strip().replace("Frequency:", "").strip()
            elif cleaned_line.strip().startswith("AC:"):
                move_ac = cleaned_line.strip().replace("AC:", "").strip()
            elif cleaned_line.strip().startswith("Class:"):
                move_classe = cleaned_line.strip().replace("Class:", "").strip()
            elif cleaned_line.strip().startswith("Range:"):
                move_range = cleaned_line.strip().replace("Range:", "").strip()
            elif cleaned_line.strip().startswith("Effect:"):
                move_effect = cleaned_line.strip().replace("Effect:", "").strip()
            elif cleaned_line.strip().startswith("Special:"):
                move_special_effect = cleaned_line.strip().replace("Special:", "").strip()
            elif cleaned_line.strip().startswith("Contest Type:"):
                move_contest_type = cleaned_line.strip().replace("Contest Type:", "").strip()
            elif cleaned_line.strip().startswith("Contest Effect:"):
                move_contest_effect = cleaned_line.strip().replace("Contest Effect:", "").strip()
            elif cleaned_line.strip().startswith("Contest Type:"):
                move_contest_type = cleaned_line.strip().replace("Contest Type:", "").strip()
            elif cleaned_line.strip().startswith("Contest Effect:"):
                move_contest_effect = cleaned_line.strip().replace("Contest Effect:", "").strip()
            else:
                # #print("found line that doesn't match anything ! ")
                # #print(cleaned_line.strip())
                move_extra_lines.append(cleaned_line.strip())
        if len(split_line) > 2:
            if split_line[0] == "Effect":
                move_effect = ""
                for line_split_instance in split_line:
                    move_effect += line_split_instance + ":"
            if split_line[0] == "Range":
                move_range = ""
                for line_split_instance in split_line:
                    move_range += line_split_instance + " "
            elif split_line[0] == "Contest Effect":
                move_effect = ""
                for line_split_instance in split_line:
                    move_contest_effect += line_split_instance + ":"
            elif split_line[0].isdigit():
                for line_split_instance in split_line:
                    move_effect += line_split_instance + ":"
            elif split_line[0] in ["Spring Form", "Summer Form", "Autumn Form", "Winter Form"]:
                for line_split_instance in split_line:
                    move_effect += line_split_instance + ":"
            elif split_line[0] == "Damage Base 9" and split_line[1] == "10":
                move_roll = "3d8+10 / 24"
                move_damage_base = "10"
            elif split_line[1] == "SpecialDamage Base" and split_line[2] == "2d10+10 / 21":
                move_roll = "2d10+10 / 21"
                move_damage_base = "9"
                move_classe = "Special"
    return moves

def save_move(param_current_move_name, param_current_move_type,param_current_move_frequency,param_current_move_AC, param_current_move_DB, param_current_move_roll,param_current_move_class,param_current_move_range,param_current_move_effect):
    print("Saving : ")
    print(param_current_move_name)
    print(param_current_move_type)
    print(param_current_move_frequency)
    print(param_current_move_AC)
    print(param_current_move_DB)
    print(param_current_move_roll)
    print(param_current_move_class)
    print(param_current_move_range)
    print(param_current_move_effect)
    if "status" in param_current_move_class.lower():
        param_current_move_DB = None
        param_current_move_roll = None
    return FullMove(id=-1,name=param_current_move_name,types=param_current_move_type,frequency=param_current_move_frequency,AC=param_current_move_AC,damage_base=param_current_move_DB,roll=param_current_move_roll,m_class=param_current_move_class,range=param_current_move_range,effect=param_current_move_effect,extra_lines=[])
input_txt = "../input_pdf/Moves updates.txt"
f = open(input_txt, "r")
lines = f.readlines()
f.close()
last_line = ""
moves = []
previous_previous_line = ""
current_move_name = ""
current_move_type = []
current_move_frequency = ""
current_move_AC = ""
current_move_DB = ""
current_move_roll = ""
current_move_class = ""
current_move_range = ""
current_move_effect = ""
for raw_line in lines:
    line = raw_line.replace("\n","").strip("* ").strip("\n")
    if line:
        if line.lower().startswith("type:") or line.lower().startswith("type :"):
            if current_move_name != "":
                current_move_effect = current_move_effect.replace(previous_previous_line, "")
                current_move_effect = current_move_effect.replace(last_line, "")
                current_move_effect = current_move_effect.replace("Effect:", "")
                move = save_move(current_move_name,current_move_type,current_move_frequency,current_move_AC,current_move_DB,current_move_roll,current_move_class,current_move_range,current_move_effect)
                moves.append(move)
                print("last line : ")
                print(last_line)
                print("previous line : ")
                print(previous_previous_line)
                current_move_frequency = ""
                current_move_AC = ""
                current_move_DB = ""
                current_move_roll = ""
                current_move_class = ""
                current_move_range = ""
                current_move_effect = ""
            current_move_name = last_line.replace(":","").replace("(added)","").strip()
            current_move_types = line.split(":")[1].strip()
            if "," in current_move_types:
                current_move_type = [f.strip() for f in current_move_types.split(",")]
            elif "/" in current_move_types:
                current_move_type = [f.strip() for f in current_move_types.split("/")]
            else :
                current_move_type = [current_move_types]
        elif line.lower().startswith("frequency:") or line.lower().startswith("frequency :"):
            current_move_frequency = line.split(":")[1].strip()
        elif line.lower().startswith("ac:") or line.lower().startswith("ac :"):
            current_move_AC = line.split(":")[1].strip()
        elif line.lower().startswith("damage base") or line.lower().startswith(" damage base"):
            splitted = line.split(":")
            current_move_roll = splitted[1].split("/")[0].strip()
            current_move_DB = splitted[0].replace("Damage Base ","")
        elif line.lower().startswith("class:") or line.lower().startswith("class :"):
            current_move_class = line.split(":")[1].strip()
        elif line.lower().startswith("range:") or line.lower().startswith("range :"):
            current_move_range = line.split(":")[1].strip()
        else:
            current_move_effect += line.strip()

        previous_previous_line = last_line
        last_line = line
move = save_move(current_move_name, current_move_type, current_move_frequency, current_move_AC, current_move_DB,
                 current_move_roll, current_move_class, current_move_range, current_move_effect)
moves.append(move)

csv_file = "output_signature_moves.csv"
csv = "Move,Freq,AC,Type,Roll,Dmg. Type,Range,Special Effect"
for m in moves:
    csv += "\n" + m.to_csv()
f = open(csv_file, "w+")
f.write(csv)
f.close()