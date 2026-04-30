import requests
import os
import json
import re
from io import BytesIO
from reportlab.lib.units import cm
from reportlab.platypus import (
    Image,
)
import time
#url = f"https://img.pokemondb.net/artwork/{name}.jpg"
#url = "https://wiki.p-insurgence.com/Delta_Bulbasaur_(Pok%C3%A9mon)"
with open("../data/final_pokemons.json","r") as f:
    pokemons = json.load(f)
delta_names = [p["name"] for p in pokemons if "delta form" in p["name"].lower()]
for raw_name in delta_names:
    time.sleep(2)
    real_name = "delta "+raw_name.replace(" delta form","")
    url = f"https://wiki.p-insurgence.com/Delta_{raw_name.replace(" delta form","").replace(" ","_").capitalize()}_(Pok%C3%A9mon)"
    print(real_name)
    pattern = r'<img (.*?) />'
    srcpattern = r'src="(.*?)"'
    img_max_size = 2
    try:
        r = requests.get(url, timeout=10)
        if r.status_code == 200:
            matches = re.findall(pattern, r.text, re.DOTALL)
            skip = False
            for match in matches:
                #print(match)
                if not skip and "alt" in match and real_name.lower() in match.lower():
                    matchesrc = re.findall(srcpattern, match, re.DOTALL)
                    if len(matchesrc) > 0:
                        print(matchesrc[0])
                        url = f"https://wiki.p-insurgence.com/{matchesrc[0]}"
                        img_r = requests.get(url, timeout=10)

                        if img_r.status_code == 200:
                            os.makedirs("../images", exist_ok=True)
                            local_png = f"../images/{raw_name.replace(" ","_")}.png"
                            # sauvegarde locale (cache)
                            with open(local_png, "wb") as f:
                                f.write(img_r.content)
                            skip = True
                            img = Image(BytesIO(img_r.content), width=img_max_size * cm, height=img_max_size * cm)
                            img.hAlign = "CENTER"

        else:
            print("#TODO")
            """
            url = f"https://forwardfeed.github.io/ER-nextdex/sprites/{name.upper().replace(" ","_")}.png"
            r = requests.get(url, timeout=10)
    
            if r.status_code == 200:
                os.makedirs(folder, exist_ok=True)
    
                # sauvegarde locale (cache)
                with open(local_png, "wb") as f:
                    f.write(r.content)
    
                img = Image(BytesIO(r.content), width=img_max_size * cm, height=img_max_size * cm)
                img.hAlign = "CENTER"
    
                return img
            """
    except Exception:
        pass

