import json


def load_pokemon(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

if __name__ == "__main__":
    pokemons = load_pokemon("data/final_pokemons.json")
    moves = load_pokemon("data/final_moves.json")
    egg_moves = []
    final_str = ""
    for poke in pokemons:
        if len(poke["egg_moves"]) > 0:
            for move_name in poke["egg_moves"]:
                to_str = move_name
                corresponding_moves = [move for move in moves if move["move"] == move_name]
                if len(corresponding_moves) > 0:
                    found_move = corresponding_moves[0]
                    to_str += " : "
                    if type(found_move["type"]) == str:
                        to_str += found_move["type"]
                    else:
                        for typem in found_move["type"]:
                            to_str += typem + ","
                        to_str = to_str[:-1]
                    if not to_str in egg_moves:
                        egg_moves.append(to_str)

    for egg in egg_moves:
        final_str += egg+"\n"

    f = open("all_egg_moves.txt","w+")
    f.write(final_str)
    f.close()
