# This is a sample Python script.
import argparse
import json
from parsers import parse_full_moves,to_serializable

parser = argparse.ArgumentParser(
                    prog='PTUMoveFormatter',
                    description='This program reads the HTML of pokemon PTU moves, and formats it to CSV. It can filter on the different values.')
parser.add_argument('html_file', help='Path to the HTML file containing the moves')
parser.add_argument('--type',required=False,default="None",help='Filter the move list by Type. Set to None or do not provide to get all types')
parser.add_argument('--frequency',required=False,default="None",help='Filter the move list by Frequency. Set to None or do not provide to get all frequencies')
parser.add_argument('--damage_base',required=False,default="None",help='Filter the move list by Damage Base. Set to None or do not provide to get all damage base')
parser.add_argument('--damage_type',required=False,default="None",help='Filter the move list by Damage Type. Set to None or do not provide to get all damage type')
parser.add_argument('-o','--output',required=True,default="output.csv",help='Path to a csv file that will be created with the moves')

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import re

def export_moves(moves,output_csv):
    csv = "Move,Freq,AC,Type,Roll,Dmg. Type,Range,Special Effect"
    print(csv.replace(",", " | "))
    for move in moves:
        csv += "\n"+moves[move].to_csv()
    f = open(output_csv,"w+")
    f.write(csv)
    f.close()

    with open("data/moves.json", "w", encoding="utf-8") as f_json:
        json.dump(
            to_serializable(list(moves.values())),
            f_json,
            indent=2,  # pretty print
            ensure_ascii=False
        )


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    args = parser.parse_args()
    filepath = args.html_file
    type_filter = args.type
    frequency_filter = args.frequency
    damage_base_filter = args.damage_base
    damage_type_filter = args.damage_type
    output = args.output
    moves =  parse_full_moves(filepath)

    final_moves = moves

    if type_filter != "None" and type_filter != "":
        moves = list(filter(lambda x: x.type.lower() == type_filter.lower(),moves))

    if frequency_filter != "None" and frequency_filter != "":
        moves = list(filter(lambda x: x.frequency.lower() == frequency_filter.lower(),moves))

    if damage_type_filter != "None" and damage_type_filter != "":
        moves = list(filter(lambda x: x.classe.lower() == damage_type_filter.lower(),moves))

    if damage_base_filter != "None" and damage_base_filter != "":
        moves = list(filter(lambda x: x.damage_base.lower() == damage_base_filter.lower(),moves))

    export_moves(moves,output)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
