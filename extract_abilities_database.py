from parsers import parse_full_abilities,to_serializable
import json
def export_abilities(abilities):
    """
    csv = "Name,Effect"
    for abili in abilities:
        if abili is not None and abili != "":
            csv += "\n"+abilities[abili].name+",\""+abilities[abili].effect+"\""
    f = open(output_csv,"w+")
    f.write(csv)
    f.close()
    """
    with open("output/initials/abilities.json", "w", encoding="utf-8") as f_json:
        json.dump(
            to_serializable(list(abilities.values())),
            f_json,
            indent=2,  # pretty print
            ensure_ascii=False
        )

if __name__ == "__main__":
    input_pdf = "input_pdf/Abilities.pdf"
    abilities = parse_full_abilities(input_pdf)
    export_abilities(abilities)