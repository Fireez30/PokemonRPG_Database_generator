import json


def load_pokemon(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

if __name__ == "__main__":
    pokemons = load_pokemon("../output/finals/pokemons.json")
    moves = load_pokemon("../output/finals/moves.json")
    tutor_moves = []
    final_str = ""
    for poke in pokemons:
        if len(poke["tutor_moves"]) > 0:
            for move_name in poke["tutor_moves"]:
                to_str = move_name
                corresponding_moves = [move for move in moves if move["name"] == move_name]
                if len(corresponding_moves) > 0:
                    found_move = corresponding_moves[0]
                    to_str += " : "
                    types_val = found_move["types"]
                    if isinstance(types_val, list):
                        to_str += ",".join(types_val)
                    else:
                        to_str += str(types_val)
                if not to_str in tutor_moves:
                    tutor_moves.append(to_str)

    for tutor in tutor_moves:
        final_str += tutor+"\n"

    f = open("all_tutor_moves.txt","w+")
    f.write(final_str)
    f.close()