from parsers import parse_extracted_text_gen8,parse_extracted_text_gen9,to_serializable,parse_mega_evolutions
import json

if __name__ == "__main__":
    with open("data/db_pokedex.json", "r") as f:
        db_pokemons = json.load(f)
    db_pokemons_names = list(filter(lambda x: x["name"]["english"].lower(),db_pokemons))
    to_skip = [865,866,1015,1016,1017,987]
    stop_at = 1353
    range_gen_7_1 = range(14,1015)
    range_gen_8 = range(1018,1130)
    range_gen_9 = range(1132,1150)
    range_gen_7_2 = range(1153,1353)
    range_eevolution = range(0,10)
    range_megaevolution = range(8,115)
    input_pdf = "data/PokedexDocumentation.pdf"
    output_json = "data/pokemon.json"
    pokemons = []
    """
    for index in range_gen_7_1:
        if index not in to_skip:
            pokemons.append(parse_extracted_text_gen8(input_pdf, index,db_pokemons_names))
    for index in range_gen_7_2:
        if index not in to_skip:
            pokemons.append(parse_extracted_text_gen8(input_pdf, index,db_pokemons_names))
    for index in range_gen_8:
        if index not in to_skip:
            pokemons.append(parse_extracted_text_gen8(input_pdf, index,db_pokemons_names))
    for index in range_gen_9:
        if index not in to_skip:
            pokemons.append(parse_extracted_text_gen9(input_pdf, index,db_pokemons_names))
    
    with open(output_json, "w", encoding="utf-8") as f:
        json.dump(
            to_serializable(pokemons),
            f,
            indent=2,  # pretty print
            ensure_ascii=False
        )
    """
    """
    for index in range_eevolution:
        pokemons.append(parse_extracted_text_gen8("data/Eveeloutions.pdf", index, db_pokemons_names))
    with open("data/eveelutions.json", "w", encoding="utf-8") as f:
        json.dump(
            to_serializable(pokemons),
            f,
            indent=2,  # pretty print
            ensure_ascii=False
        )
        """
    with open("data/pokemon.json", "r") as f:
        pokemons = json.load(f)
    poke_to_mega = parse_mega_evolutions("data/Pokemon MegaDex.pdf",range_megaevolution)
    for index, value in enumerate(pokemons):
        if value["name"].lower() in poke_to_mega.keys():
            pokemons[index]["mega_evolution"] = poke_to_mega[value["name"].lower()]
    with open("data/pokemon.json", "w", encoding="utf-8") as f:
        json.dump(
            to_serializable(pokemons),
            f,
            indent=2,  # pretty print
            ensure_ascii=False
        )
