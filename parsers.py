import fitz
from pokemon_data import *
import re

stop_read = False

from dataclasses import asdict, is_dataclass
def to_serializable(obj):
    if is_dataclass(obj):
        return asdict(obj)
    elif isinstance(obj, list):
        return [to_serializable(item) for item in obj]
    elif hasattr(obj, "__dict__"):
        return {
            key: to_serializable(value)
            for key, value in obj.__dict__.items()
        }
    else:
        return obj

def should_skip_line(line,page_number):
    return line.strip() == "" or "Unofficial Gen 7" in line or line.strip() == page_number
def remove_html_tags(text):
    clean = re.compile('<.*?>')
    return re.sub(clean, '', text)
def replace_dash_in_move_names(text):
    output = text
    mapping = {"Topsy-Turvy":"Topsy&Turvy","Will-O-Wisp":"Will&O&Wisp","X-Scissor":"X&Scissor","Mud-Slap":"Mud&Slap","Multi-Attack":"Multi&Attack","Never-Ending Nightmare":"Never&Ending Nightmare","Double-Edge":"Double&Edge","All-Out Pummeling":"All&Out Pummeling","Baby-Doll Eyes":"Baby&Doll Eyes","Freeze-Dry":"Freeze&Dry","G-Max":"G&Max","Lock-On":"Lock&On","U-turn":"U&turn","Wake-Up Slap":"Wake&Up Slap","V-create":"V&create","Trick-or-Treat":"Trick&or&Treat","Power-Up Punch":"Power&Up Punch","Savage Spin-Out":"Savage Spin&Out","Self-Destruct":"Self&Destruct","Soft-Boiled":"Soft&Boiled","Soul-Stealing 7-Star Strike":"Soul&Stealing 7&Star Strike"}
    for k, v in mapping.items():
        output = output.replace(k, v)
    return output

def is_bold_span(span):
    # Most reliable check
    if "bold" in span["font"].lower():
        return True

    # Backup: flags bitmask (bold is bit 2^4 = 16)
    if span["flags"] & 16:
        return True

    return False
def first_line_is_bold(block):
    if block["type"] != 0:  # not text
        return False

    if not block["lines"]:
        return False

    first_line = block["lines"][0]
    spans = first_line["spans"]

    if not spans:
        return False

    bold_spans = sum(is_bold_span(span) for span in spans)

    # You can tune this rule:
    # - all spans bold
    # - or majority bold
    return bold_spans >= len(spans) / 2

def extract_one_column_text(pdf_path):
    global stop_read
    doc = fitz.open(pdf_path)
    sections = []
    current_section = []

    for page in doc:
        data = page.get_text("dict")

        for block in data["blocks"]:
            if block["type"] != 0:
                continue

            block_text = ""
            for line in block["lines"]:
                for span in line["spans"]:
                    block_text += span["text"]
                block_text += "\n"

            block_text = block_text.strip()
            if not block_text:
                continue

            if first_line_is_bold(block):
                # Start new section
                if current_section:
                    sections.append("\n".join(current_section))
                current_section = [block_text]
            else:
                current_section.append(block_text)

    if current_section:
        sections.append("\n".join(current_section))

    return sections

def extract_two_columns_text(pdf_path, page_number=0):
    global stop_read
    doc = fitz.open(pdf_path)
    if page_number >= doc.page_count:
        stop_read = True
        return None
    page = doc[page_number]

    #blocks = page.get_text("blocks")
    width2 = page.rect.width / 2  # half of the page width
    left = page.rect + (0, 0, -width2, 0)  # the left half page
    right = page.rect + (width2, 0, 0, 0)  # the right half page
    # now extract the 2 halves spearately:
    lblocks = page.get_text("blocks", clip=left, sort=True)
    rblocks = page.get_text("blocks", clip=right, sort=True)
    blocks = lblocks + rblocks
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

def UNUSED_parse_extracted_text_gen7(input_pdf,index):
    text = extract_two_columns_text(input_pdf, page_number=index)
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

def parse_extracted_text_gen8(input_pdf,index):
    text = extract_two_columns_text(input_pdf, page_number=index)
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
    mega_evolution = False
    mega_evolution_type_aggr = ""
    mega_evolution_stats_aggr = ""
    mega_evolution_ability_aggr = ""
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
        if line.strip().lower() == "mega evolution" or line.strip().lower() == "mega evolution:":
            mega_evolution = True
            current_status = "mega_evolution_nothing"
            previous_line = line
            continue
        if "mega_evolution" in current_status and line.strip().lower().startswith("type:"):
            current_status = "mega_evolution_type"
            mega_evolution_type_aggr = line.split(':')[1].strip()
            previous_line = line
            continue
        if "mega_evolution" in current_status and line.strip().lower().startswith("ability:"):
            current_status = "mega_evolution_ability"
            previous_line = line
            mega_evolution_ability_aggr = line.split(':')[1].strip()
            continue
        if "mega_evolution" in current_status and line.strip().lower().startswith("stats:"):
            current_status = "mega_evolution_stats"
            mega_evolution_stats_aggr = line.split(':')[1].strip()
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


        if current_status == "mega_evolution_type":
            if line.strip() != "":
                mega_evolution_type_aggr += line.strip() + " "
        if current_status == "mega_evolution_ability":
            if line.strip() != "":
                mega_evolution_ability_aggr += line.strip() + " "

        if current_status == "mega_evolution_stats":
            if line.strip() != "":
                mega_evolution_stats_aggr += line.strip() + " "

        if current_status == "skills":
            if line.strip() != "":
                skills_aggr += line.strip() + " "


        if current_status == "moves":
            print(line)
            if line.strip().lower().startswith("level up move list") or line.strip() == "":
                previous_line = line
                continue
            replaced_move = replace_dash_in_move_names(line)
            if replaced_move.strip()[0].isdigit() and "-" in replaced_move:
                found_line = replaced_move.strip().replace(" - ",":").replace(" -",':').replace("- ",':')
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
                moves.append(Move(splitted[0].replace("&","-"),level,splitted[1]))
            elif "-" not in replaced_move and replaced_move.strip()[0].isdigit():
                levelstr = ""
                for i in range(0, len(replaced_move)):
                    if replaced_move[i].isdigit():
                        levelstr += replaced_move[i]
                    else:
                        break
                level = int(levelstr)
                found_line = replaced_move.replace(levelstr, "").strip()
                moves.append(Move(found_line.replace("&","-"), level, ""))
            elif replaced_move.strip().startswith("Evo") and "-" in replaced_move:
                found_line = replaced_move.strip().replace(" - ", ":").replace(" -",':').replace("- ",':')
                found_line = found_line.replace("Evo ","").strip()
                char_split = ':'
                if '-' in found_line and not ':' in found_line:
                    char_split = '-'
                splitted = found_line.split(char_split)
                moves.append(Move(splitted[0].replace("&","-"),0,splitted[1]))
            elif replaced_move.strip().startswith("Evo") and "-" not in replaced_move:
                found_line = replaced_move.replace("Evo ", "").strip()
                moves.append(Move(found_line.replace("&","-"), 0, ""))

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

    print(mega_evolution_type_aggr)
    mega_evolution_types = []
    if "," in mega_evolution_type_aggr:
        mega_evolution_types = mega_evolution_type_aggr.split(',')
    else :
        mega_evolution_types = [mega_evolution_type_aggr]

    print(mega_evolution_ability_aggr)
    print(mega_evolution_stats_aggr)
    mega_evolution_obj = MegaEvolution(mega_evolution_types, mega_evolution_ability_aggr, mega_evolution_stats_aggr)
    print("name: "+name)
    print("hp: "+str(hp))
    print("attack: "+str(attack))
    print("defense: "+str(defense))
    print("spattack: "+str(spattack))
    print("spdefense: "+str(spdefense))
    print("speed: "+str(speed))
    print("Types : ")
    print(poketype)
    print("Evolutions : ")
    print(evolutions)
    print("Base abilities : ")
    print(base_abilities)
    print("Advanced abilities : ")
    print(advanced_abilities)
    print("High abilities : ")
    print(high_abilities)
    print("Height : ")
    print(height)
    print("Weigth : ")
    print(weight)
    print("Gender ratio M : ")
    print(gender_ratio_m)
    print("Gender ratio F : ")
    print(gender_ratio_f)
    print("Egg group : ")
    print(egg_group)
    print("Diet : ")
    print(diet)
    print("Habitat : ")
    print(habitat)
    print("Capabilities : ")
    print(capabilities)
    print("Skills : ")
    print(skills)
    print("Moves : ")
    print(moves)
    print("TM Moves : ")
    print(tm_moves)
    print("Tutor moves : ")
    print(tutor_moves)
    print("Egg moves : ")
    print(egg_moves)
    return Pokemon(name,hp,attack,defense,spattack,spdefense,speed,poketype,base_abilities,advanced_abilities,high_abilities,evolutions,height,weight,gender_ratio_m,gender_ratio_f,egg_group,average_hatch_rate,diet,habitat,capabilities,skills,moves,tm_moves,tutor_moves,egg_moves,mega_evolution,mega_evolution_obj)


def parse_extracted_text_gen9(input_pdf,index):
    text = extract_two_columns_text(input_pdf, page_number=index)
    name = ""
    stats_aggr = ""
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
    mega_evolution = False
    mega_evolution_type_aggr = ""
    mega_evolution_stats_aggr = ""
    mega_evolution_ability_aggr = ""
    text = text.replace(": \n",":")
    for line in text.split("\n"):
        print(line)
        if line.strip() == "":
            previous_line = line
            continue
        if current_status != "base_stats" and line.strip().isdigit():
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
        if line.strip().lower() == "mega evolution" or line.strip().lower() == "mega evolution:":
            mega_evolution = True
            current_status = "mega_evolution_nothing"
            previous_line = line
            continue
        if "mega_evolution" in current_status and line.strip().lower().startswith("type:"):
            current_status = "mega_evolution_type"
            mega_evolution_type_aggr = line.split(':')[1].strip()
            previous_line = line
            continue
        if "mega_evolution" in current_status and line.strip().lower().startswith("ability:"):
            current_status = "mega_evolution_ability"
            previous_line = line
            mega_evolution_ability_aggr = line.split(':')[1].strip()
            continue
        if "mega_evolution" in current_status and line.strip().lower().startswith("stats:"):
            current_status = "mega_evolution_stats"
            mega_evolution_stats_aggr = line.split(':')[1].strip()
            previous_line = line
            continue
        if line.strip().lower().startswith("evolution"):
            current_status = "evolution"
            previous_line = line
            continue
        if line.strip().lower().startswith("other lnformation") or line.strip().lower().startswith("other information"):
            current_status = "other"
            previous_line = line
            continue
        if line.strip().lower().startswith("capabilities"):
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
        if line.strip().lower().startswith("tm move list") or line.strip().lower().startswith("tm/hm move list") or line.strip().lower().startswith("tm/tutor moves"):
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
            if line.strip().isdigit():
                stats_aggr += line.strip()+","
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


        if current_status == "other":
            if line.strip().lower().startswith("height:"):
                height = line.strip().split(":")[1].strip()
            if line.strip().lower().startswith("size:"):
                height = line.strip().split(":")[1].strip()
            if line.strip().lower().startswith("weight:"):
                weight = line.strip().split(":")[1].strip()
            if "lbs" in line and "kg" in line:
                weight = line.strip()
            if line.strip().startswith("(") and line.strip().endswith(")"):
                if "Weight" in line:
                    weight += " "+line.strip()
                else:
                    height += " "+line.strip()
            if line.strip().lower().startswith("genders:"):
                if line.split(':')[1].lower().strip() == "no gender" or line.split(':')[1].lower().strip() == "hermaphrodite" or line.split(':')[1].lower().strip() == "genderless" or line.split(':')[1].lower().strip() == "gender unknown" or line.split(':')[1].lower().strip() == "unknown":
                    gender_ratio_f = -1
                    gender_ratio_m = -1
                elif "male" in line.strip().lower():
                    cleaned = re.sub(r'[^0-9]', '', line.split(':')[1].strip().split(".")[0])
                    gender_ratio_m = float(cleaned)
                    gender_ratio_f = 100 - float(gender_ratio_m)
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


        if current_status == "mega_evolution_ability":
            if line.strip() != "":
                mega_evolution_ability_aggr += line.strip() + " "

        if current_status == "mega_evolution_stats":
            if line.strip() != "":
                mega_evolution_stats_aggr += line.strip() + " "

        if current_status == "mega_evolution_type":
            if line.strip() != "":
                mega_evolution_type_aggr += line.strip() + " "
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
            replaced_move = replace_dash_in_move_names(line)
            if replaced_move.count('-') == 2:
                splited = replaced_move.split("-")
                if splited[0].lower().startswith("evo"):
                    splited[0] = 0
                moves.append(Move(splited[1].strip().replace("&","-"),int(splited[0]),splited[2].strip()))
            elif replaced_move.strip()[0].isdigit() and "-" in replaced_move:
                found_line = replaced_move.strip().replace(" - ",":").replace(" -",':').replace("- ",':')
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
                moves.append(Move(splitted[0].replace("&","-"),level,splitted[1]))
            elif "-" not in replaced_move and replaced_move.strip()[0].isdigit():
                levelstr = ""
                for i in range(0, len(replaced_move)):
                    if replaced_move[i].isdigit():
                        levelstr += replaced_move[i]
                    else:
                        break
                level = int(levelstr)
                found_line = replaced_move.replace(levelstr, "").strip()
                moves.append(Move(found_line.replace("&","-"), level, ""))
            elif replaced_move.strip().startswith("Evo") and "-" in replaced_move:
                found_line = replaced_move.strip().replace(" - ", ":").replace(" -",':').replace("- ",':')
                found_line = found_line.replace("Evo ","").strip()
                char_split = ':'
                if '-' in found_line and not ':' in found_line:
                    char_split = '-'
                splitted = found_line.split(char_split)
                moves.append(Move(splitted[0].replace("&","-"),0,splitted[1]))
            elif replaced_move.strip().startswith("Evo") and "-" not in replaced_move:
                found_line = replaced_move.replace("Evo ", "").strip()
                moves.append(Move(found_line.replace("&","-"), 0, ""))

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

    split_stat = stats_aggr[:len(stats_aggr)-1].split(",")
    if len(split_stat) == 7:
        hp = split_stat[0]
        spattack = split_stat[1]
        attack = split_stat[2]
        spdefense = split_stat[3]
        defense = split_stat[5]
        speed = split_stat[6]
    else:
        for stat in split_stat:
            if stat != "":
                if hp == -1:
                    hp = int(stat)
                elif spattack == -1:
                    spattack = int(stat)
                elif attack == -1:
                    attack = int(stat)
                elif spdefense == -1:
                    spdefense = int(stat)
                elif defense == -1:
                    defense = int(stat)
                elif speed == -1:
                    speed = int(stat)
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

    print(mega_evolution_type_aggr)
    mega_evolution_types = []
    if "," in mega_evolution_type_aggr:
        mega_evolution_types = mega_evolution_type_aggr.split(',')
    else :
        mega_evolution_types = [mega_evolution_type_aggr]

    print(mega_evolution_ability_aggr)
    print(mega_evolution_stats_aggr)
    mega_evolution_obj = MegaEvolution(mega_evolution_types, mega_evolution_ability_aggr, mega_evolution_stats_aggr)
    print("name: "+name)
    print("hp: "+str(hp))
    print("attack: "+str(attack))
    print("defense: "+str(defense))
    print("spattack: "+str(spattack))
    print("spdefense: "+str(spdefense))
    print("speed: "+str(speed))
    print("Types : ")
    print(poketype)
    print("Evolutions : ")
    print(evolutions)
    print("Base abilities : ")
    print(base_abilities)
    print("Advanced abilities : ")
    print(advanced_abilities)
    print("High abilities : ")
    print(high_abilities)
    print("Height : ")
    print(height)
    print("Weigth : ")
    print(weight)
    print("Gender ratio M : ")
    print(gender_ratio_m)
    print("Gender ratio F : ")
    print(gender_ratio_f)
    print("Egg group : ")
    print(egg_group)
    print("Diet : ")
    print(diet)
    print("Habitat : ")
    print(habitat)
    print("Capabilities : ")
    print(capabilities)
    print("Skills : ")
    print(skills)
    print("Moves : ")
    print(moves)
    print("TM Moves : ")
    print(tm_moves)
    print("Tutor moves : ")
    print(tutor_moves)
    print("Egg moves : ")
    print(egg_moves)
    return Pokemon(name,hp,attack,defense,spattack,spdefense,speed,poketype,base_abilities,advanced_abilities,high_abilities,evolutions,height,weight,gender_ratio_m,gender_ratio_f,egg_group,average_hatch_rate,diet,habitat,capabilities,skills,moves,tm_moves,tutor_moves,egg_moves,mega_evolution,mega_evolution_obj)
def sections_to_text(all_sections):
    extracted = []

    for section in all_sections:
        # Sort blocks top-to-bottom inside section
        sorted_blocks = sorted(section, key=lambda b: (b[1], b[0]))

        text = "\n".join(
            block[4].strip()
            for block in sorted_blocks
            if block[4].strip()
        )

        extracted.append(text)

    return extracted
def parse_full_abilities(filepath="data/Abilities.pdf"):
    all_sections = extract_one_column_text(filepath)
    abilities = {}
    #section_texts = sections_to_text(all_sections)
    for section in all_sections:
        name = ""
        effect = ""
        lines = section.split("\n")
        index = 0
        for line in lines:
            if "Abilities" in line or "Ability list " in line or " / 110" in line or "2024-08-13" in line or "DocumentationJDR.md" in line:
                continue
            if index == 0:
                name = line.replace("Ability:","").strip()
            else:
                effect += line+"\n"
            index += 1
        effect = effect[:-1]
        abilities[name]=Ability(name=name,effect=effect.replace('"',"'").replace("\n"," "))
    return abilities

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
    #    print(cleaned_line)
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
        # print(split_line)
        if len(split_line) == 1:
            if cleaned_line.strip().startswith("----"):
                # print("found move to store : "+move_name)
                if not bypass_current_move and move_name.strip() != "":
                    moves[move_name]=FullMove(move_name, move_type, move_frequency, move_ac, move_damage_base, move_roll, move_classe,
                             move_range,
                             move_effect, move_blessing, move_special_effect, move_contest_type, move_contest_effect,
                             move_extra_lines)
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
                # print("found move : " + move_name)
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
                # print("found line that doesn't match anything ! ")
                # print(cleaned_line.strip())
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