from parsers import parse_extracted_text_gen8,parse_extracted_text_gen9,to_serializable,parse_mega_evolutions
import json

if __name__ == "__main__":
    replace_list = [
        ("wo-chien","wo chien"),
        ("chien-pao","chien pao"),
        ("ting-lu","ting lu"),
        ("chi-yu","chi yu"),
        ("gimmighoul (chest form)","gimmighoul"),
        ("gimmighoul (roaming form)","gimmighoul roaming"),
        ("enamorus incarnate forme","enamorus"),
        ("enamorus therian forme","enamorus therian"),
        ("urshifu single strike form","urshifu"),
        ("urshifu rapid strike form","urshifu rapid strike style"),
        ("shllnotlc","shiinotic"),
        ("salandlt","salandit"),
        ("wishiwashi solo","wishiwashi"),
        ("wishiwashi schooling","wishiwashi school"),
        ("nolvern","noivern"),
        ("nolbat","noibat"),
        ("mareanle","mareanie"),
        ("fomantls","fomantis"),
        ("lurantls","lurantis"),
        ("bergmlte","bergmite"),
        ("gourgelst","gourgeist"),
        ("meowstic (m)","meowstic"),
        ("meowstic (f)","meowstic female"),
        ("sklddo","skiddo"),
        ("lltleo","litleo"),
        ("dlggersby","diggersby"),
        ("kyurem normal forme","kyurem"),
        ("kyurem white fusion forme","kyurem white"),
        ("kyurem black fusion forme","kyurem black"),
        ("landorus incarnate forme","landorus"),
        ("landorus therian forme","landorus therian"),
        ("thundurus incarnate forme","thundurus"),
        ("thundurus therian forme","thundurus therian"),
        ("tornadus incarnate forme","tornadus"),
        ("tornadus therian forme","tornadus therian"),
        ("bravlary","braviary"),
        ("beartlc","beartic"),
        ("deerllng","deerling"),
        ("speed:3","reuniclus"),
        ("trubblsh","trubbish"),
        ("mlncclno","minccino"),
        ("clncclno","cinccino"),
        ("petllll","petilil"),
        ("darmanitan galar, zen mode","darmanitan zen mode galar"),
        ("darmanltan standard mode","darmanitan"),
        ("darmanltan zen mode","darmanitan zen"),
        ("darmanitan galar, standard mode","darmanitan galar"),
        ("basculegion male","basculegion"),
        ("basculegion female","basculegion f"),
        ("lllllgant","lilligant"),
        ("excadrlll","excadrill"),
        ("whlmslcott","whimsicott"),
        ("slmlsage","simisage"),
        ("drllbur","drilbur"),
        ("slmlsear","simisear"),
        ("mlsmaglus","mismagius"),
        ("llcklllcky","lickilicky"),
        ("toxlcroak","toxicroak"),
        ("draplon","drapion"),
        ("skorupl","skorupi"),
        ("hlppowdon","hippowdon"),
        ("hlppopotas","hippopotas"),
        ("chlngllng","chingling"),
        ("drlfloon","drifloon"),
        ("drlfbllm","drifblim"),
        ("amblpom","ambipom"),
        ("cherubl","cherubi"),
        ("cherrlm","cherrim"),
        ("bldoof","bidoof"),
        ("blbarel","bibarel"),
        ("ratlcate","raticate"),
        ("dlglett","diglett"),
        ("dugtrlo","dugtrio"),
        ("perslan","persian"),
        ("dodrlo","dodrio"),
        ("llckltung","lickitung"),
        ("grlmer","grimer"),
        ("kofflng","koffing"),
        ("weezlng","weezing"),
        ("mlme jr.", "mime jr."),
        ("giratina origin forme", "giratina origin"),
        ("shaymin land forme", "shaymin"),
        ("shaymin sky forme", "shaymin sky"),
        ("mr. mime galar", "mr mime galar"),
        ("rotom normal form", "rotom"),
        ("mr. mlme", "mr. mime"),
        ("mlsdreavus","misdreavus"),
        ("alpom","aipom"),
        ("gllgar","gligar"),
        ("gllscor","gliscor"),
        ("teddlursa","teddiursa"),
        ("ursarlng","ursaring"),
        ("zlgzagoon","zigzagoon"),
        ("llnoone","linoone"),
        ("talllow","taillow"),
        ("shroomlsh","shroomish"),
        ("skltty","skitty"),
        ("gulpln","gulpin"),
        ("spolnk","spoink"),
        ("grumplg","grumpig"),
        ("altarla","altaria"),
        ("chlmecho","chimecho"),
        ("glalle","glalie"),
        ("deoxys normal forme","deoxys"),
        ("wormadam sandy cloak","wormadam sandy"),
        ("wormadam plant cloak","wormadam"),
        ("wormadam trash cloak","wormadam trash"),
        ("deoxys attack forme","deoxys attack"),
        ("deoxys defense forme","deoxys defense"),
        ("deoxys speed forme","deoxys speed"),
        ("deoxys speed forme","deoxys speed"),
    ]
    with open("data/db_pokedex.json", "r") as f:
        db_pokemons = json.load(f)
    db_pokemons_names = list(filter(lambda x: x["name"]["english"].lower(),db_pokemons))
    range_gen_7 = range(14,866)
    pdf_gen_7 = "data/pokedex1_7_final_version.pdf"
    range_gen_galar = range(2,121)
    pdf_galar = "data/GalarDex_Armor_Crown.pdf"
    range_gen_9 = range(3,117)
    pdf_gen_9 = "data/Gen 9_Homebrew_Dex.pdf"
    range_gen_9_dlc = range(1,20)
    pdf_gen_9_dlc = "data/Gen9 DLC.pdf"
    range_insurgence = range(3,207)
    pdf_insurgence = "data/InsurgenceDex.pdf"
    range_hisui = range(3,31)
    pdf_hisui = "data/HisuiDex.pdf"
    range_eevolution = range(0,10)
    pdf_eevolution = "data/Eveeloutions.pdf"
    range_megaevolution = range(8,115)
    pdf_mega_evo = "data/Pokemon MegaDex.pdf"
    output_json = "data/pokemon.json"
    pokemons = []
    loaded_mons = parse_extracted_text_gen8(pdf_gen_7, range_gen_7,db_pokemons_names)
    if loaded_mons is not None:
        for mon in loaded_mons:
            pokemons.append(mon)
    loaded_mons = parse_extracted_text_gen8(pdf_galar, range_gen_galar,db_pokemons_names)
    if loaded_mons is not None:
        for mon in loaded_mons:
            pokemons.append(mon)
    loaded_mons = parse_extracted_text_gen8(pdf_gen_9, range_gen_9,db_pokemons_names)
    if loaded_mons is not None:
        for mon in loaded_mons:
            pokemons.append(mon)
    loaded_mons = parse_extracted_text_gen9(pdf_gen_9_dlc, range_gen_9_dlc,db_pokemons_names)
    if loaded_mons is not None:
        for mon in loaded_mons:
            pokemons.append(mon)
    loaded_mons = parse_extracted_text_gen8(pdf_insurgence, range_insurgence,db_pokemons_names)
    if loaded_mons is not None:
        for mon in loaded_mons:
            pokemons.append(mon)
    loaded_mons = parse_extracted_text_gen8(pdf_hisui, range_hisui,db_pokemons_names)
    if loaded_mons is not None:
        for mon in loaded_mons:
            pokemons.append(mon)
    loaded_mons = parse_extracted_text_gen8(pdf_eevolution, range_eevolution, db_pokemons_names)
    if loaded_mons is not None:
        for mon in loaded_mons:
            pokemons.append(mon)
    with open(output_json, "w", encoding="utf-8") as f:
        json.dump(
            to_serializable(pokemons),
            f,
            indent=2,  # pretty print
            ensure_ascii=False
        )
    with open(output_json, "r") as f:
        pokemons = json.load(f)
    poke_to_mega = parse_mega_evolutions(pdf_mega_evo,range_megaevolution)
    for index, value in enumerate(pokemons):
        if value["name"].lower() in poke_to_mega.keys():
            pokemons[index]["mega_evolution"] = poke_to_mega[value["name"].lower()]
    for pokenames in replace_list:
        to_replace = pokenames[0]
        replace_with = pokenames[1]
        for poke in pokemons:
            if poke["name"] == to_replace:
                poke["name"] = replace_with
    with open(output_json, "w", encoding="utf-8") as f:
        json.dump(
            to_serializable(pokemons),
            f,
            indent=2,  # pretty print
            ensure_ascii=False
        )
