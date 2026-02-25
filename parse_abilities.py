from parsers import parse_full_abilities

def export_abilities(abilities,output_csv):
    csv = "Name,Effect"
    for abili in abilities:
        if abili is not None and abili != "":
            csv += "\n"+abilities[abili].name+",\""+abilities[abili].effect+"\""
    f = open(output_csv,"w+")
    f.write(csv)
    f.close()

if __name__ == "__main__":
    input_pdf = "data/Abilities.pdf"
    output_csv = "abilities.csv"
    abilities = parse_full_abilities(input_pdf)
    for ability in abilities:
        if ability == "Trinity":
            print(abilities[ability].name)
            print(abilities[ability].effect)
            print(" ------ ")
    export_abilities(abilities,output_csv)