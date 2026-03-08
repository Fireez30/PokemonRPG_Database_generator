from parsers import parse_extracted_text_gen8,parse_extracted_text_gen9,to_serializable
import json

if __name__ == "__main__":
    to_skip = [865,866,1015,1016,1017,987]
    stop_at = 1353
    range_gen_7_1 = range(15,1015)
    range_gen_8 = range(1018,1130)
    range_gen_9 = range(1132,1150)
    range_gen_7_2 = range(1153,1353)
    input_pdf = "data/test_alkazam.pdf"
    pokemons = []
    pokemons.append(parse_extracted_text_gen8(input_pdf, 0))
    with open("data/pokemon_test.json", "w", encoding="utf-8") as f:
        json.dump(
            to_serializable(pokemons),
            f,
            indent=2,  # pretty print
            ensure_ascii=False
        )