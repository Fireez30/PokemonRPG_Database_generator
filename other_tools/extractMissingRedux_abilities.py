import json
import re

with open("../data/reduxData.json", "r") as f:
    data = json.load(f)

with open("../output/initials/abilities.json", "r") as f:
    old_abilities = json.load(f)
#explore_json(data)
#print("abilities before : "+str(len(abilities)))
abilities = []
redux_abilities = []
for ability in data["abilities"]:
    if ability["name"] != "-------":
        redux_abilities.append({"name":ability["name"],"effect":ability["desc"],"id":ability["id"],"update":"TBD"})

for rability in redux_abilities:
    already_exist = list(filter(lambda x:x["name"].lower() == rability["name"].lower(), old_abilities))
    if len(already_exist) == 0:
        abilities.append(rability)

final_abilities = sorted(abilities, key = lambda x: x["name"])

def split_trigger_and_effect(effect_text):
    cleaned = " ".join(effect_text.split())
    trigger_match = re.search(r"\btrigger\s*:\s*", cleaned, re.IGNORECASE)
    if not trigger_match:
        return None, cleaned

    before_trigger = cleaned[:trigger_match.start()].strip(" -–—;,.")
    after_trigger = cleaned[trigger_match.end():].strip()

    effect_match = re.search(r"\beffect\s*:\s*", after_trigger, re.IGNORECASE)
    if effect_match:
        trigger = after_trigger[:effect_match.start()].strip(" -–—;,.")
        effect_part = after_trigger[effect_match.end():].strip()
        merged_effect = " ".join(part for part in [before_trigger, effect_part] if part)
        return trigger if trigger else None, merged_effect

    split_sentence = re.search(r"(?<=[.!?])\s+", after_trigger)
    if split_sentence:
        trigger = after_trigger[:split_sentence.start()].strip(" -–—;,.")
        remaining = after_trigger[split_sentence.end():].strip()
        merged_effect = " ".join(part for part in [before_trigger, remaining] if part)
        return trigger if trigger else None, merged_effect

    return after_trigger if after_trigger else None, before_trigger if before_trigger else cleaned

with open("../output/redux/missing_abilities.md", "w", encoding="utf-8") as f_md:
    for ability in final_abilities:
        trigger, effect = split_trigger_and_effect(ability.get("effect", ""))

        f_md.write(f"## {ability['name']}\n")
        if trigger:
            f_md.write(f"Trigger: {trigger}\n")
        f_md.write(f"Effet: {effect}\n\n")
