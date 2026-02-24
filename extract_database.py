from parsers import parse_extracted_text_gen8,parse_extracted_text_gen9
import json
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
if __name__ == "__main__":
    to_skip = [865,866,1015,1016,1017,987]
    stop_at = 1353
    range_gen_7_1 = range(15,1015)
    range_gen_8 = range(1018,1130)
    range_gen_9 = range(1132,1150)
    range_gen_7_2 = range(1153,1353)
    input_pdf = "data/PokedexDocumentation.pdf"
    output_json = "database.json"
    pokemons = []
    for index in range_gen_7_1:
        if index not in to_skip:
            pokemons.append(parse_extracted_text_gen8(input_pdf, index))
    for index in range_gen_7_2:
        if index not in to_skip:
            pokemons.append(parse_extracted_text_gen8(input_pdf, index))
    for index in range_gen_8:
        if index not in to_skip:
            pokemons.append(parse_extracted_text_gen8(input_pdf, index))
    for index in range_gen_9:
        if index not in to_skip:
            pokemons.append(parse_extracted_text_gen9(input_pdf, index))
    with open("output.json", "w", encoding="utf-8") as f:
        json.dump(
            to_serializable(pokemons),
            f,
            indent=2,  # pretty print
            ensure_ascii=False
        )