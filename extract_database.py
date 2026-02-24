import fitz
from pokemon_data import *
import re

stop_read = False
def should_skip_line(line,page_number):
    return line.strip() == "" or "Unofficial Gen 7" in line or line.strip() == page_number

def extract_two_columns_text(pdf_path, page_number=0):
    global stop_read
    doc = fitz.open(pdf_path)
    if page_number >= doc.page_count:
        stop_read = True
        return None
    page = doc[page_number]

    blocks = page.get_text("blocks")

    page_width = page.rect.width
    mid_x = page_width / 2.25

    left_column = []
    right_column = []

    for block in blocks:
        x0, y0, x1, y1, text, *_ = block

        if not should_skip_line(text,page_number):
            #print(text)
            if x0 < mid_x:
                left_column.append((y0, text))
            else:
                right_column.append((y0, text))

    left_column.sort(key=lambda x: x[0])
    right_column.sort(key=lambda x: x[0])

    left_text = "\n".join([text for _, text in left_column])
    right_text = "\n".join([text for _, text in right_column])

    final_text = left_text + "\n\n" + right_text
    final_text = final_text.replace("HP: \n","HP:")
    final_text = final_text.replace("Attack: \n","Attack:")
    final_text = final_text.replace("Defense: \n","Defense:")
    final_text = final_text.replace("Special Defense: \n","Special Defense:")
    final_text = final_text.replace("Speed: \n","Speed:")
    return final_text

def UNUSED_parse_extracted_text_gen7(text):
    name = ""
    hp = -1
    attack = -1
    defense = -1
    spattack = -1
    spdefense = -1
    speed = -1
    poketype = ""
    evolutions = []
    base_abilities = []
    advanced_abilities = []
    high_abilities = []
    height = ""
    weight = ""
    gender_ratio_m = -1
    gender_ratio_f = -1
    egg_group = ""
    average_hatch_rate = -1
    diet = ""
    habitat = ""
    capabilities = []
    skills = []
    moves = []
    tm_moves = []
    tutor_moves = []
    egg_moves  = []

    not_treated = []
    current_status = "name"
    capabilities_aggr = ""
    skills_aggr = ""
    tm_moves_aggr = ""
    tutor_moves_aggr = ""
    egg_moves_aggr = ""
    previous_line = ""
    for line in text.split("\n"):
        if line.strip() == "":
            previous_line = line
            continue
        if line.strip().isdigit():
            not_treated.append(line)
            continue
        if line.strip().lower()=="base stats:":
            current_status = "base_stats"
            previous_line = line
            continue
        if line.strip().lower() == "basic information" or line.strip().lower() == "basic lnformation":
            current_status = "basic_information"
            previous_line = line
            continue
        if line.strip().lower().startswith("evolution:"):
            current_status = "evolution"
            previous_line = line
            continue
        if line.strip().lower().startswith("size lnformation") or line.strip().lower().startswith("size information"):
            current_status = "size"
            previous_line = line
            continue
        if line.strip().lower().startswith("breeding lnformation") or line.strip().lower().startswith("breeding information"):
            current_status = "breeding"
            previous_line = line
            continue
        if line.strip().lower().startswith("capability list"):
            current_status = "capabilities"
            previous_line = line
            continue
        if line.strip().lower().startswith("skill list"):
            current_status = "skills"
            previous_line = line
            continue
        if line.strip().lower().startswith("move list"):
            current_status = "moves"
            previous_line = line
            continue
        if line.strip().lower().startswith("tm move list") or line.strip().lower().startswith("tm/hm move list"):
            current_status = "tm_moves"
            previous_line = line
            continue
        if line.strip().lower().startswith("tutor move list"):
            current_status = "tutor_moves"
            previous_line = line
            continue
        if line.strip().lower().startswith("egg move list"):
            current_status = "egg_moves"
            previous_line = line
            continue
        if current_status == "name" and line.strip() != "":
            name = line.strip().lower()
        if current_status == "base_stats":
            if ':' in line:
                # cleaned = re.sub(r'[^0-9]', '', line.split(':')[1])
                cleaned = line.split(':')[1].replace("l", "1").replace(" ","")
                cleaned = re.sub(r'[^0-9]', '', cleaned)
                #cleaned = line.split(':')[1]
                if cleaned.strip() == "" or not cleaned.strip().isdigit():
                    previous_line = line
                    continue
                if line.strip().lower().startswith("hp:"):
                    if cleaned == "":
                        hp = -1
                    else :
                        hp=int(cleaned)
                if line.strip().lower().startswith("attack:"):
                    if cleaned == "":
                        attack = -1
                    else:
                        attack=int(cleaned)
                if line.strip().lower().startswith("defense:"):
                    if cleaned == "":
                        defense = -1
                    else:
                        defense=int(cleaned)
                if line.strip().lower().startswith("special attack:"):
                    if cleaned == "":
                        spattack = -1
                    else:
                        spattack=int(cleaned)
                if line.strip().lower().startswith("special defense:"):
                    if cleaned == "":
                        spdefense = -1
                    else:
                        spdefense=int(cleaned)
                if line.strip().lower().startswith("speed:"):
                    if cleaned == "":
                        speed = -1
                    else:
                        speed=int(cleaned)


        if current_status == "basic_information":
            if line.strip().lower().startswith("type:"):
                splitted = line.split(':')[1].strip()
                if '/' in splitted:
                    poketype = [s.strip() for s in splitted.split('/')]
                else :
                    poketype = splitted.strip()
            if line.strip().lower().startswith("basic ability") and ":" in line.strip().lower():
                ability = line.split(':')[1].strip()
                base_abilities.append(ability)
            if line.strip().lower().startswith("adv ability") and ":" in line.strip().lower():
                ability = line.split(':')[1].strip()
                advanced_abilities.append(ability)
            if line.strip().lower().startswith("high ability") and ":" in line.strip().lower():
                ability = line.split(':')[1].strip()
                high_abilities.append(ability)


        if current_status == "evolution":
            if line[0].isdigit() and "-" in line:
                toparse = line.strip().split("-")[1].strip()
                if toparse != "":
                    evolutions.append(toparse)


        if current_status == "size":
            if line.strip().lower().startswith("height:"):
                height = line.strip().split(":")[1].strip()
            if line.strip().lower().startswith("weight:"):
                weight = line.strip().split(":")[1].strip()

        if current_status == "breeding":
            if line.strip().lower().startswith("gender ratio:") or line.strip().lower().startswith("information gender ratio:"):
                cleaned_line = line.replace("Egg","")
                if cleaned_line.split(':')[1].lower().strip() == "no gender" or cleaned_line.split(':')[1].lower().strip() == "hermaphrodite" or cleaned_line.split(':')[1].lower().strip() == "genderless" or cleaned_line.split(':')[1].lower().strip() == "gender unknown" or cleaned_line.split(':')[1].lower().strip() == "unknown":
                    gender_ratio_f = -1
                    gender_ratio_m = -1
                else:
                    splitted = cleaned_line.split(':')[1].split('/')
                    if len(splitted) == 1 or (len(splitted) == 2 and splitted[1].strip()) == "":
                        gender_ratio_m = splitted[0].split("%")[0].strip()
                        gender_ratio_f = 100 - float(gender_ratio_m)
                    elif len(splitted) == 2:
                        gender_ratio_m = splitted[0].split("%")[0].strip()
                        gender_ratio_f = splitted[1].split("%")[0].strip()
            if line.strip().lower().startswith("egg group:") or (line.strip().lower().startswith("group:") and previous_line.strip().lower().endswith("egg")):
                egg_group = line.split(':')[1].strip()
            if line.strip().lower().startswith("diet:"):
                diet = line.split(':')[1].strip()
            if line.strip().lower().startswith("habitat:"):
                habitat = line.split(':')[1].strip()


        if current_status == "capabilities":
            if line.strip() != "":
                capabilities_aggr += line.strip() + " "


        if current_status == "skills":
            if line.strip() != "":
                skills_aggr += line.strip() + " "


        if current_status == "moves":
            print(line)
            if line.strip().lower().startswith("level up move list") or line.strip() == "":
                previous_line = line
                continue
            if line.strip()[0].isdigit() and "-" in line:
                found_line = line.strip().replace(" - ",":").replace(" -",':').replace("- ",':')
                levelstr = ""
                for i in range(0,len(found_line)):
                    if found_line[i].isdigit():
                        levelstr += found_line[i]
                    else:
                        break
                level = int(levelstr)
                found_line = found_line.replace(levelstr,"").strip()
                char_split = ':'
                if '-' in found_line and not ':' in found_line:
                    char_split = '-'
                splitted = found_line.split(char_split)
                print("name : "+splitted[0])
                moves.append(Move(splitted[0],level,splitted[1]))
            elif "-" not in line and line.strip()[0].isdigit():
                levelstr = ""
                for i in range(0, len(line)):
                    if line[i].isdigit():
                        levelstr += line[i]
                    else:
                        break
                level = int(levelstr)
                found_line = line.replace(levelstr, "").strip()
                moves.append(Move(found_line, level, ""))
            elif line.strip().startswith("Evo") and "-" in line:
                found_line = line.strip().replace(" - ", ":").replace(" -",':').replace("- ",':')
                found_line = found_line.replace("Evo ","").strip()
                char_split = ':'
                if '-' in found_line and not ':' in found_line:
                    char_split = '-'
                splitted = found_line.split(char_split)
                moves.append(Move(splitted[0],0,splitted[1]))
            elif line.strip().startswith("Evo") and "-" not in line:
                found_line = line.replace("Evo ", "").strip()
                moves.append(Move(found_line, 0, ""))

        if current_status == "tm_moves":
            if line.strip() != "":
                tm_moves_aggr += line.strip() + " "


        if current_status == "tutor_moves":
            if line.strip() != "":
                tutor_moves_aggr += line.strip() + " "


        if current_status == "egg_moves":
            if line.strip() != "":
                egg_moves_aggr += line.strip() + " "
        previous_line = line

    in_parenthesis = False
    out_capabilities = ""
    for s in capabilities_aggr:
        if s == '(' or s == '[':
            in_parenthesis = True
        if s == ')' or s == ']':
            in_parenthesis = False
        if not in_parenthesis and s == ',':
            out_capabilities += ";"
        else:
            out_capabilities += s

    for cap in out_capabilities.split(';'):
        trimmed_cap = cap.strip()
        m = re.search(r"\d", trimmed_cap) #  iterator of digits
        if m:
            index_split = int(m.start())
            name_cap = trimmed_cap[:index_split].strip()
            val = trimmed_cap[index_split:].strip()
            capabilities.append(Capability(name=name_cap,value=val))
        else:
            capabilities.append(Capability(name=trimmed_cap,value=""))

    in_parenthesis = False
    out_skills = ""
    for s in skills_aggr:
        if s == '(' or s == '[':
            in_parenthesis = True
        if s == ')' or s == ']':
            in_parenthesis = False
        if not in_parenthesis and s == ',':
            out_skills += ";"
        else:
            out_skills += s

    for cap in out_skills.split(';'):
        trimmed_cap = cap.strip()
        m = re.search(r"\d", trimmed_cap)  # iterator of digits
        if m:
            index_split = int(m.start())
            name_cap = trimmed_cap[:index_split].strip()
            val = trimmed_cap[index_split:].strip()
            skills.append(Skill(name=name_cap, roll=val))
        else:
            skills.append(Skill(name=trimmed_cap, roll=""))

    if tm_moves_aggr.strip() != "":
        in_parenthesis = False
        out_tm_moves = ""
        for s in tm_moves_aggr:
            if s == '(' or s == '[':
                in_parenthesis = True
            if s == ')' or s == ']':
                in_parenthesis = False
            if not in_parenthesis and s == ',':
                out_tm_moves += ";"
            else:
                out_tm_moves += s

        for cap in out_tm_moves.split(';'):
            tm_moves.append(cap.strip())

    if egg_moves_aggr.strip() != "":
        in_parenthesis = False
        out_egg_moves = ""
        for s in egg_moves_aggr:
            if s == '(' or s == '[':
                in_parenthesis = True
            if s == ')' or s == ']':
                in_parenthesis = False
            if not in_parenthesis and s == ',':
                out_egg_moves += ";"
            else:
                out_egg_moves += s

        for cap in out_egg_moves.split(';'):
            egg_moves.append(cap.strip())

    if tutor_moves_aggr.strip() != "":
        in_parenthesis = False
        out_tutor_moves = ""
        for s in tutor_moves_aggr:
            if s == '(' or s == '[':
                in_parenthesis = True
            if s == ')' or s == ']':
                in_parenthesis = False
            if not in_parenthesis and s == ',':
                out_tutor_moves += ";"
            else:
                out_tutor_moves += s

        for cap in out_tutor_moves.split(';'):
            tutor_moves.append(cap.strip())
    if hp == -1 and len(not_treated) > 0:
        hp = int(not_treated.pop(0).strip())
    if defense == -1 and len(not_treated) > 0:
        defense = int(not_treated.pop(0).strip())
    if attack == -1 and len(not_treated) > 0:
        attack = int(not_treated.pop(0).strip())
    if spattack == -1 and len(not_treated) > 0:
        spattack = int(not_treated.pop(0).strip())
    if spdefense == -1 and len(not_treated) > 0:
        spdefense = int(not_treated.pop(0).strip())
    if speed == -1 and len(not_treated) > 0:
        speed = int(not_treated.pop(0).strip())
    print(name)
    print(hp)
    print(attack)
    print(defense)
    print(spattack)
    print(spdefense)
    print(speed)
    print(poketype)
    print(evolutions)
    print(base_abilities)
    print(advanced_abilities)
    print(high_abilities)
    print(height)
    print(weight)
    print(gender_ratio_m)
    print(gender_ratio_f)
    print(egg_group)
    print(diet)
    print(habitat)
    print(capabilities)
    print(skills)
    print(moves)
    print(tm_moves)
    print(tutor_moves)
    print(egg_moves)
    return Pokemon(name,hp,attack,defense,spattack,spdefense,speed,poketype,base_abilities,advanced_abilities,high_abilities,evolutions,height,weight,gender_ratio_m,gender_ratio_f,egg_group,average_hatch_rate,diet,habitat,capabilities,skills,moves,tm_moves,tutor_moves,egg_moves)

def parse_extracted_text_gen8(text):
    name = ""
    hp = -1
    attack = -1
    defense = -1
    spattack = -1
    spdefense = -1
    speed = -1
    poketype = ""
    evolutions = []
    base_abilities = []
    advanced_abilities = []
    high_abilities = []
    height = ""
    weight = ""
    gender_ratio_m = -1
    gender_ratio_f = -1
    egg_group = ""
    average_hatch_rate = -1
    diet = ""
    habitat = ""
    capabilities = []
    skills = []
    moves = []
    tm_moves = []
    tutor_moves = []
    egg_moves  = []

    not_treated = []
    current_status = "name"
    capabilities_aggr = ""
    skills_aggr = ""
    tm_moves_aggr = ""
    tutor_moves_aggr = ""
    egg_moves_aggr = ""
    previous_line = ""
    for line in text.split("\n"):
        print(line)
        if line.strip() == "":
            previous_line = line
            continue
        if line.strip().isdigit():
            not_treated.append(line)
            continue
        if line.strip().lower()=="base stats" or line.strip().lower() == "base stats:":
            current_status = "base_stats"
            previous_line = line
            continue
        if line.strip().lower() == "basic information" or line.strip().lower() == "basic lnformation":
            current_status = "basic_information"
            previous_line = line
            continue
        if line.strip().lower().startswith("evolution:"):
            current_status = "evolution"
            previous_line = line
            continue
        if line.strip().lower().startswith("size lnformation") or line.strip().lower().startswith("size information"):
            current_status = "size"
            previous_line = line
            continue
        if line.strip().lower().startswith("breeding lnformation") or line.strip().lower().startswith("breeding information"):
            current_status = "breeding"
            previous_line = line
            continue
        if line.strip().lower().startswith("capability list"):
            current_status = "capabilities"
            previous_line = line
            continue
        if line.strip().lower().startswith("skill list"):
            current_status = "skills"
            previous_line = line
            continue
        if line.strip().lower().startswith("move list"):
            current_status = "moves"
            previous_line = line
            continue
        if line.strip().lower().startswith("tm move list") or line.strip().lower().startswith("tm/hm move list"):
            current_status = "tm_moves"
            previous_line = line
            continue
        if line.strip().lower().startswith("tutor move list"):
            current_status = "tutor_moves"
            previous_line = line
            continue
        if line.strip().lower().startswith("egg move list"):
            current_status = "egg_moves"
            previous_line = line
            continue
        if current_status == "name" and line.strip() != "":
            name = line.strip().lower()
        if current_status == "base_stats":
            if ':' in line:
                # cleaned = re.sub(r'[^0-9]', '', line.split(':')[1])
                cleaned = line.split(':')[1].replace("l", "1").replace(" ","")
                cleaned = re.sub(r'[^0-9]', '', cleaned)
                #cleaned = line.split(':')[1]
                if cleaned.strip() == "" or not cleaned.strip().isdigit():
                    previous_line = line
                    continue
                if line.strip().lower().startswith("hp:"):
                    if cleaned == "":
                        hp = -1
                    else :
                        hp=int(cleaned)
                if line.strip().lower().startswith("attack:"):
                    if cleaned == "":
                        attack = -1
                    else:
                        attack=int(cleaned)
                if line.strip().lower().startswith("defense:"):
                    if cleaned == "":
                        defense = -1
                    else:
                        defense=int(cleaned)
                if line.strip().lower().startswith("special attack:"):
                    if cleaned == "":
                        spattack = -1
                    else:
                        spattack=int(cleaned)
                if line.strip().lower().startswith("special defense:"):
                    if cleaned == "":
                        spdefense = -1
                    else:
                        spdefense=int(cleaned)
                if line.strip().lower().startswith("speed:"):
                    if cleaned == "":
                        speed = -1
                    else:
                        speed=int(cleaned)


        if current_status == "basic_information":
            if line.strip().lower().startswith("type:"):
                splitted = line.split(':')[1].strip()
                if '/' in splitted:
                    poketype = [s.strip() for s in splitted.split('/')]
                else :
                    poketype = splitted.strip()
            if line.strip().lower().startswith("basic ability") and ":" in line.strip().lower():
                ability = line.split(':')[1].strip()
                base_abilities.append(ability)
            if (line.strip().lower().startswith("adv ability") or line.strip().lower().startswith("advanced ability")) and ":" in line.strip().lower():
                ability = line.split(':')[1].strip()
                advanced_abilities.append(ability)
            if line.strip().lower().startswith("high ability") and ":" in line.strip().lower():
                ability = line.split(':')[1].strip()
                high_abilities.append(ability)


        if current_status == "evolution":
            if line[0].isdigit() and "-" in line:
                toparse = line.strip().split("-")[1].strip()
                if toparse != "":
                    evolutions.append(toparse)


        if current_status == "size":
            if line.strip().lower().startswith("height:"):
                height = line.strip().split(":")[1].strip()
            if line.strip().lower().startswith("weight:"):
                weight = line.strip().split(":")[1].strip()

        if current_status == "breeding":
            if line.strip().lower().startswith("gender ratio:") or line.strip().lower().startswith("information gender ratio:"):
                cleaned_line = line.replace("Egg","")
                if cleaned_line.split(':')[1].lower().strip() == "no gender" or cleaned_line.split(':')[1].lower().strip() == "hermaphrodite" or cleaned_line.split(':')[1].lower().strip() == "genderless" or cleaned_line.split(':')[1].lower().strip() == "gender unknown" or cleaned_line.split(':')[1].lower().strip() == "unknown":
                    gender_ratio_f = -1
                    gender_ratio_m = -1
                else:
                    splitted = cleaned_line.split(':')[1].split('/')
                    if len(splitted) == 1 or (len(splitted) == 2 and splitted[1].strip()) == "":
                        gender_ratio_m = splitted[0].split("%")[0].strip()
                        gender_ratio_f = 100 - float(gender_ratio_m)
                    elif len(splitted) == 2:
                        gender_ratio_m = splitted[0].split("%")[0].strip()
                        gender_ratio_f = splitted[1].split("%")[0].strip()
            if line.strip().lower().startswith("egg group:") or (line.strip().lower().startswith("group:") and previous_line.strip().lower().endswith("egg")):
                egg_group = line.split(':')[1].strip()
                diet = line.split(':')[1].strip()
            if line.strip().lower().startswith("average hatch rate:"):
                cleaned = re.sub(r'[^0-9]', '', line.split(':')[1].strip())
                if cleaned != "" and cleaned.isdigit():
                    average_hatch_rate = int(cleaned)
            if line.strip().lower().startswith("diet:"):
                diet = line.split(':')[1].strip()
            if line.strip().lower().startswith("habitat:"):
                habitat = line.split(':')[1].strip()


        if current_status == "capabilities":
            if line.strip() != "":
                capabilities_aggr += line.strip() + " "


        if current_status == "skills":
            if line.strip() != "":
                skills_aggr += line.strip() + " "


        if current_status == "moves":
            print(line)
            if line.strip().lower().startswith("level up move list") or line.strip() == "":
                previous_line = line
                continue
            if line.strip()[0].isdigit() and "-" in line:
                found_line = line.strip().replace(" - ",":").replace(" -",':').replace("- ",':')
                levelstr = ""
                for i in range(0,len(found_line)):
                    if found_line[i].isdigit():
                        levelstr += found_line[i]
                    else:
                        break
                level = int(levelstr)
                found_line = found_line.replace(levelstr,"").strip()
                char_split = ':'
                if '-' in found_line and not ':' in found_line:
                    char_split = '-'
                splitted = found_line.split(char_split)
                print("name : "+splitted[0])
                moves.append(Move(splitted[0],level,splitted[1]))
            elif "-" not in line and line.strip()[0].isdigit():
                levelstr = ""
                for i in range(0, len(line)):
                    if line[i].isdigit():
                        levelstr += line[i]
                    else:
                        break
                level = int(levelstr)
                found_line = line.replace(levelstr, "").strip()
                moves.append(Move(found_line, level, ""))
            elif line.strip().startswith("Evo") and "-" in line:
                found_line = line.strip().replace(" - ", ":").replace(" -",':').replace("- ",':')
                found_line = found_line.replace("Evo ","").strip()
                char_split = ':'
                if '-' in found_line and not ':' in found_line:
                    char_split = '-'
                splitted = found_line.split(char_split)
                moves.append(Move(splitted[0],0,splitted[1]))
            elif line.strip().startswith("Evo") and "-" not in line:
                found_line = line.replace("Evo ", "").strip()
                moves.append(Move(found_line, 0, ""))

        if current_status == "tm_moves":
            if line.strip() != "":
                tm_moves_aggr += line.strip() + " "


        if current_status == "tutor_moves":
            if line.strip() != "":
                tutor_moves_aggr += line.strip() + " "


        if current_status == "egg_moves":
            if line.strip() != "":
                egg_moves_aggr += line.strip() + " "
        previous_line = line

    in_parenthesis = False
    out_capabilities = ""
    for s in capabilities_aggr:
        if s == '(' or s == '[':
            in_parenthesis = True
        if s == ')' or s == ']':
            in_parenthesis = False
        if not in_parenthesis and s == ',':
            out_capabilities += ";"
        else:
            out_capabilities += s

    for cap in out_capabilities.split(';'):
        trimmed_cap = cap.strip()
        m = re.search(r"\d", trimmed_cap) #  iterator of digits
        if m:
            index_split = int(m.start())
            name_cap = trimmed_cap[:index_split].strip()
            val = trimmed_cap[index_split:].strip()
            capabilities.append(Capability(name=name_cap,value=val))
        else:
            capabilities.append(Capability(name=trimmed_cap,value=""))

    in_parenthesis = False
    out_skills = ""
    for s in skills_aggr:
        if s == '(' or s == '[':
            in_parenthesis = True
        if s == ')' or s == ']':
            in_parenthesis = False
        if not in_parenthesis and s == ',':
            out_skills += ";"
        else:
            out_skills += s

    for cap in out_skills.split(';'):
        trimmed_cap = cap.strip()
        m = re.search(r"\d", trimmed_cap)  # iterator of digits
        if m:
            index_split = int(m.start())
            name_cap = trimmed_cap[:index_split].strip()
            val = trimmed_cap[index_split:].strip()
            skills.append(Skill(name=name_cap, roll=val))
        else:
            skills.append(Skill(name=trimmed_cap, roll=""))

    if tm_moves_aggr.strip() != "":
        in_parenthesis = False
        out_tm_moves = ""
        for s in tm_moves_aggr:
            if s == '(' or s == '[':
                in_parenthesis = True
            if s == ')' or s == ']':
                in_parenthesis = False
            if not in_parenthesis and s == ',':
                out_tm_moves += ";"
            else:
                out_tm_moves += s

        for cap in out_tm_moves.split(';'):
            tm_moves.append(cap.strip())

    if egg_moves_aggr.strip() != "":
        in_parenthesis = False
        out_egg_moves = ""
        for s in egg_moves_aggr:
            if s == '(' or s == '[':
                in_parenthesis = True
            if s == ')' or s == ']':
                in_parenthesis = False
            if not in_parenthesis and s == ',':
                out_egg_moves += ";"
            else:
                out_egg_moves += s

        for cap in out_egg_moves.split(';'):
            egg_moves.append(cap.strip())

    if tutor_moves_aggr.strip() != "":
        in_parenthesis = False
        out_tutor_moves = ""
        for s in tutor_moves_aggr:
            if s == '(' or s == '[':
                in_parenthesis = True
            if s == ')' or s == ']':
                in_parenthesis = False
            if not in_parenthesis and s == ',':
                out_tutor_moves += ";"
            else:
                out_tutor_moves += s

        for cap in out_tutor_moves.split(';'):
            tutor_moves.append(cap.strip())
    if hp == -1 and len(not_treated) > 0:
        hp = int(not_treated.pop(0).strip())
    if defense == -1 and len(not_treated) > 0:
        defense = int(not_treated.pop(0).strip())
    if attack == -1 and len(not_treated) > 0:
        attack = int(not_treated.pop(0).strip())
    if spattack == -1 and len(not_treated) > 0:
        spattack = int(not_treated.pop(0).strip())
    if spdefense == -1 and len(not_treated) > 0:
        spdefense = int(not_treated.pop(0).strip())
    if speed == -1 and len(not_treated) > 0:
        speed = int(not_treated.pop(0).strip())
    print(name)
    print(hp)
    print(attack)
    print(defense)
    print(spattack)
    print(spdefense)
    print(speed)
    print(poketype)
    print(evolutions)
    print(base_abilities)
    print(advanced_abilities)
    print(high_abilities)
    print(height)
    print(weight)
    print(gender_ratio_m)
    print(gender_ratio_f)
    print(egg_group)
    print(diet)
    print(habitat)
    print(capabilities)
    print(skills)
    print(moves)
    print(tm_moves)
    print(tutor_moves)
    print(egg_moves)
    return Pokemon(name,hp,attack,defense,spattack,spdefense,speed,poketype,base_abilities,advanced_abilities,high_abilities,evolutions,height,weight,gender_ratio_m,gender_ratio_f,egg_group,average_hatch_rate,diet,habitat,capabilities,skills,moves,tm_moves,tutor_moves,egg_moves)


def parse_extracted_text_gen9(text):
    name = ""
    hp = -1
    attack = -1
    defense = -1
    spattack = -1
    spdefense = -1
    speed = -1
    poketype = ""
    evolutions = []
    base_abilities = []
    advanced_abilities = []
    high_abilities = []
    height = ""
    weight = ""
    gender_ratio_m = -1
    gender_ratio_f = -1
    egg_group = ""
    average_hatch_rate = -1
    diet = ""
    habitat = ""
    capabilities = []
    skills = []
    moves = []
    tm_moves = []
    tutor_moves = []
    egg_moves  = []

    not_treated = []
    current_status = "name"
    capabilities_aggr = ""
    skills_aggr = ""
    tm_moves_aggr = ""
    tutor_moves_aggr = ""
    egg_moves_aggr = ""
    previous_line = ""
    for line in text.split("\n"):
        print(line)
        if line.strip() == "":
            previous_line = line
            continue
        if line.strip().isdigit():
            not_treated.append(line)
            continue
        if line.strip().lower()=="base stats" or line.strip().lower() == "base stats:":
            current_status = "base_stats"
            previous_line = line
            continue
        if line.strip().lower() == "basic information" or line.strip().lower() == "basic lnformation":
            current_status = "basic_information"
            previous_line = line
            continue
        if line.strip().lower().startswith("evolution:"):
            current_status = "evolution"
            previous_line = line
            continue
        if line.strip().lower().startswith("size lnformation") or line.strip().lower().startswith("size information"):
            current_status = "size"
            previous_line = line
            continue
        if line.strip().lower().startswith("breeding lnformation") or line.strip().lower().startswith("breeding information"):
            current_status = "breeding"
            previous_line = line
            continue
        if line.strip().lower().startswith("capability list"):
            current_status = "capabilities"
            previous_line = line
            continue
        if line.strip().lower().startswith("skill list"):
            current_status = "skills"
            previous_line = line
            continue
        if line.strip().lower().startswith("move list"):
            current_status = "moves"
            previous_line = line
            continue
        if line.strip().lower().startswith("tm move list") or line.strip().lower().startswith("tm/hm move list"):
            current_status = "tm_moves"
            previous_line = line
            continue
        if line.strip().lower().startswith("tutor move list"):
            current_status = "tutor_moves"
            previous_line = line
            continue
        if line.strip().lower().startswith("egg move list"):
            current_status = "egg_moves"
            previous_line = line
            continue
        if current_status == "name" and line.strip() != "":
            name = line.strip().lower()
        if current_status == "base_stats":
            # Update this to aggr all lines with digits.
            # format is the following :
            # line 1 : HP SPATK
            # line 2 : ATK SPDEF TOTAL
            #line 3 : DEF SPD
            # split everything after the line parsing
            if ':' in line:
                # cleaned = re.sub(r'[^0-9]', '', line.split(':')[1])
                cleaned = line.split(':')[1].replace("l", "1").replace(" ","")
                cleaned = re.sub(r'[^0-9]', '', cleaned)
                #cleaned = line.split(':')[1]
                if cleaned.strip() == "" or not cleaned.strip().isdigit():
                    previous_line = line
                    continue
                if line.strip().lower().startswith("hp:"):
                    if cleaned == "":
                        hp = -1
                    else :
                        hp=int(cleaned)
                if line.strip().lower().startswith("attack:"):
                    if cleaned == "":
                        attack = -1
                    else:
                        attack=int(cleaned)
                if line.strip().lower().startswith("defense:"):
                    if cleaned == "":
                        defense = -1
                    else:
                        defense=int(cleaned)
                if line.strip().lower().startswith("special attack:"):
                    if cleaned == "":
                        spattack = -1
                    else:
                        spattack=int(cleaned)
                if line.strip().lower().startswith("special defense:"):
                    if cleaned == "":
                        spdefense = -1
                    else:
                        spdefense=int(cleaned)
                if line.strip().lower().startswith("speed:"):
                    if cleaned == "":
                        speed = -1
                    else:
                        speed=int(cleaned)


        if current_status == "basic_information":
            if line.strip().lower().startswith("type:"):
                splitted = line.split(':')[1].strip()
                if '/' in splitted:
                    poketype = [s.strip() for s in splitted.split('/')]
                else :
                    poketype = splitted.strip()
            if line.strip().lower().startswith("basic ability") and ":" in line.strip().lower():
                ability = line.split(':')[1].strip()
                base_abilities.append(ability)
            if (line.strip().lower().startswith("adv ability") or line.strip().lower().startswith("advanced ability")) and ":" in line.strip().lower():
                ability = line.split(':')[1].strip()
                advanced_abilities.append(ability)
            if line.strip().lower().startswith("high ability") and ":" in line.strip().lower():
                ability = line.split(':')[1].strip()
                high_abilities.append(ability)


        if current_status == "evolution":
            if line[0].isdigit() and "-" in line:
                toparse = line.strip().split("-")[1].strip()
                if toparse != "":
                    evolutions.append(toparse)


        if current_status == "size":
            if line.strip().lower().startswith("height:"):
                height = line.strip().split(":")[1].strip()
            if line.strip().lower().startswith("weight:"):
                weight = line.strip().split(":")[1].strip()

        if current_status == "breeding":
            if line.strip().lower().startswith("gender ratio:") or line.strip().lower().startswith("information gender ratio:"):
                cleaned_line = line.replace("Egg","")
                if cleaned_line.split(':')[1].lower().strip() == "no gender" or cleaned_line.split(':')[1].lower().strip() == "hermaphrodite" or cleaned_line.split(':')[1].lower().strip() == "genderless" or cleaned_line.split(':')[1].lower().strip() == "gender unknown" or cleaned_line.split(':')[1].lower().strip() == "unknown":
                    gender_ratio_f = -1
                    gender_ratio_m = -1
                else:
                    splitted = cleaned_line.split(':')[1].split('/')
                    if len(splitted) == 1 or (len(splitted) == 2 and splitted[1].strip()) == "":
                        gender_ratio_m = splitted[0].split("%")[0].strip()
                        gender_ratio_f = 100 - float(gender_ratio_m)
                    elif len(splitted) == 2:
                        gender_ratio_m = splitted[0].split("%")[0].strip()
                        gender_ratio_f = splitted[1].split("%")[0].strip()
            if line.strip().lower().startswith("egg group:") or (line.strip().lower().startswith("group:") and previous_line.strip().lower().endswith("egg")):
                egg_group = line.split(':')[1].strip()
                diet = line.split(':')[1].strip()
            if line.strip().lower().startswith("average hatch rate:"):
                cleaned = re.sub(r'[^0-9]', '', line.split(':')[1].strip())
                if cleaned != "" and cleaned.isdigit():
                    average_hatch_rate = int(cleaned)
            if line.strip().lower().startswith("diet:"):
                diet = line.split(':')[1].strip()
            if line.strip().lower().startswith("habitat:"):
                habitat = line.split(':')[1].strip()


        if current_status == "capabilities":
            if line.strip() != "":
                capabilities_aggr += line.strip() + " "


        if current_status == "skills":
            if line.strip() != "":
                skills_aggr += line.strip() + " "


        if current_status == "moves":
            print(line)
            # first, replace all moves with a dash (u-turn, double-edge, all-out pummeling, baby-doll eyes, freeze-dry, all G-Max moves, lock-on, mud-slap, multi-attack, never-ending nightmare, power-up punch, savage spin-out, self-destruct, soft-boiled, soul-stealing 7-star strike, topsy-turvy, trick-or-treat, V-create, wake-up slap, will-o-wisp, x-scissor) , by the same with space
            # than, parsing is easier, split on ("-") , and than trim
            if line.strip().lower().startswith("level up move list") or line.strip() == "":
                previous_line = line
                continue
            if line.strip()[0].isdigit() and "-" in line:
                found_line = line.strip().replace(" - ",":").replace(" -",':').replace("- ",':')
                levelstr = ""
                for i in range(0,len(found_line)):
                    if found_line[i].isdigit():
                        levelstr += found_line[i]
                    else:
                        break
                level = int(levelstr)
                found_line = found_line.replace(levelstr,"").strip()
                char_split = ':'
                if '-' in found_line and not ':' in found_line:
                    char_split = '-'
                splitted = found_line.split(char_split)
                print("name : "+splitted[0])
                moves.append(Move(splitted[0],level,splitted[1]))
            elif "-" not in line and line.strip()[0].isdigit():
                levelstr = ""
                for i in range(0, len(line)):
                    if line[i].isdigit():
                        levelstr += line[i]
                    else:
                        break
                level = int(levelstr)
                found_line = line.replace(levelstr, "").strip()
                moves.append(Move(found_line, level, ""))
            elif line.strip().startswith("Evo") and "-" in line:
                found_line = line.strip().replace(" - ", ":").replace(" -",':').replace("- ",':')
                found_line = found_line.replace("Evo ","").strip()
                char_split = ':'
                if '-' in found_line and not ':' in found_line:
                    char_split = '-'
                splitted = found_line.split(char_split)
                moves.append(Move(splitted[0],0,splitted[1]))
            elif line.strip().startswith("Evo") and "-" not in line:
                found_line = line.replace("Evo ", "").strip()
                moves.append(Move(found_line, 0, ""))

        if current_status == "tm_moves":
            if line.strip() != "":
                tm_moves_aggr += line.strip() + " "


        if current_status == "tutor_moves":
            if line.strip() != "":
                tutor_moves_aggr += line.strip() + " "


        if current_status == "egg_moves":
            if line.strip() != "":
                egg_moves_aggr += line.strip() + " "
        previous_line = line

    in_parenthesis = False
    out_capabilities = ""
    for s in capabilities_aggr:
        if s == '(' or s == '[':
            in_parenthesis = True
        if s == ')' or s == ']':
            in_parenthesis = False
        if not in_parenthesis and s == ',':
            out_capabilities += ";"
        else:
            out_capabilities += s

    for cap in out_capabilities.split(';'):
        trimmed_cap = cap.strip()
        m = re.search(r"\d", trimmed_cap) #  iterator of digits
        if m:
            index_split = int(m.start())
            name_cap = trimmed_cap[:index_split].strip()
            val = trimmed_cap[index_split:].strip()
            capabilities.append(Capability(name=name_cap,value=val))
        else:
            capabilities.append(Capability(name=trimmed_cap,value=""))

    in_parenthesis = False
    out_skills = ""
    for s in skills_aggr:
        if s == '(' or s == '[':
            in_parenthesis = True
        if s == ')' or s == ']':
            in_parenthesis = False
        if not in_parenthesis and s == ',':
            out_skills += ";"
        else:
            out_skills += s

    for cap in out_skills.split(';'):
        trimmed_cap = cap.strip()
        m = re.search(r"\d", trimmed_cap)  # iterator of digits
        if m:
            index_split = int(m.start())
            name_cap = trimmed_cap[:index_split].strip()
            val = trimmed_cap[index_split:].strip()
            skills.append(Skill(name=name_cap, roll=val))
        else:
            skills.append(Skill(name=trimmed_cap, roll=""))

    if tm_moves_aggr.strip() != "":
        in_parenthesis = False
        out_tm_moves = ""
        for s in tm_moves_aggr:
            if s == '(' or s == '[':
                in_parenthesis = True
            if s == ')' or s == ']':
                in_parenthesis = False
            if not in_parenthesis and s == ',':
                out_tm_moves += ";"
            else:
                out_tm_moves += s

        for cap in out_tm_moves.split(';'):
            tm_moves.append(cap.strip())

    if egg_moves_aggr.strip() != "":
        in_parenthesis = False
        out_egg_moves = ""
        for s in egg_moves_aggr:
            if s == '(' or s == '[':
                in_parenthesis = True
            if s == ')' or s == ']':
                in_parenthesis = False
            if not in_parenthesis and s == ',':
                out_egg_moves += ";"
            else:
                out_egg_moves += s

        for cap in out_egg_moves.split(';'):
            egg_moves.append(cap.strip())

    if tutor_moves_aggr.strip() != "":
        in_parenthesis = False
        out_tutor_moves = ""
        for s in tutor_moves_aggr:
            if s == '(' or s == '[':
                in_parenthesis = True
            if s == ')' or s == ']':
                in_parenthesis = False
            if not in_parenthesis and s == ',':
                out_tutor_moves += ";"
            else:
                out_tutor_moves += s

        for cap in out_tutor_moves.split(';'):
            tutor_moves.append(cap.strip())
    if hp == -1 and len(not_treated) > 0:
        hp = int(not_treated.pop(0).strip())
    if defense == -1 and len(not_treated) > 0:
        defense = int(not_treated.pop(0).strip())
    if attack == -1 and len(not_treated) > 0:
        attack = int(not_treated.pop(0).strip())
    if spattack == -1 and len(not_treated) > 0:
        spattack = int(not_treated.pop(0).strip())
    if spdefense == -1 and len(not_treated) > 0:
        spdefense = int(not_treated.pop(0).strip())
    if speed == -1 and len(not_treated) > 0:
        speed = int(not_treated.pop(0).strip())
    print(name)
    print(hp)
    print(attack)
    print(defense)
    print(spattack)
    print(spdefense)
    print(speed)
    print(poketype)
    print(evolutions)
    print(base_abilities)
    print(advanced_abilities)
    print(high_abilities)
    print(height)
    print(weight)
    print(gender_ratio_m)
    print(gender_ratio_f)
    print(egg_group)
    print(diet)
    print(habitat)
    print(capabilities)
    print(skills)
    print(moves)
    print(tm_moves)
    print(tutor_moves)
    print(egg_moves)
    return Pokemon(name,hp,attack,defense,spattack,spdefense,speed,poketype,base_abilities,advanced_abilities,high_abilities,evolutions,height,weight,gender_ratio_m,gender_ratio_f,egg_group,average_hatch_rate,diet,habitat,capabilities,skills,moves,tm_moves,tutor_moves,egg_moves)

if __name__ == "__main__":
    skip_pages_to = 14
    to_skip = [865,866,1015,1016,1017,987]
    stop_at = 1353
    range_gen_7_1 = range(13,1015)
    range_gen_8 = range(1018,1129)
    range_gen_9 = range(1132,1149)
    range_gen_7_2 = range(1153,1352)
    input_pdf = "data/PokedexDocumentation.pdf"
    output_json = "database.json"
    pokemons = []
    """for index in range_gen_7_1:
        if index not in to_skip:
            text = extract_two_columns_text(input_pdf, page_number=index)
            print(text)
            if not stop_read and text is not None:
                pokemons.append(parse_extracted_text_gen8(text))
    for index in range_gen_7_2:
        if index not in to_skip:
            text = extract_two_columns_text(input_pdf, page_number=index)
            print(text)
            if not stop_read and text is not None:
                pokemons.append(parse_extracted_text_gen8(text))
    for index in range_gen_8:
        if index not in to_skip:
            text = extract_two_columns_text(input_pdf, page_number=index)
            print(text)
            if not stop_read and text is not None:
                pokemons.append(parse_extracted_text_gen8(text))"""
    """for index in range_gen_9:
        if index not in to_skip:
            text = extract_two_columns_text(input_pdf, page_number=index)
            print(text)
            if not stop_read and text is not None:
                pokemons.append(parse_extracted_text_gen9(text))"""

    text = extract_two_columns_text(input_pdf, page_number=1132)
    if not stop_read and text is not None:
        pokemons.append(parse_extracted_text_gen9(text))