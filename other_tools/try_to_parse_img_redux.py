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
with open("../output/finals/pokemons_redux_new.json","r") as f:
    pokemons = json.load(f)
delta_names = [p["name"] for p in pokemons]
for raw_name in delta_names:
    time.sleep(2)
    real_name = raw_name
    url = f"https://wiki.p-insurgence.com/Delta_{raw_name.replace(" delta form","").replace(" ","_").capitalize()}_(Pok%C3%A9mon)"
    print(real_name)
    img_max_size = 2

    url = f"https://forwardfeed.github.io/ER-nextdex/sprites/{real_name.upper().replace(" ","_")}.png"
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