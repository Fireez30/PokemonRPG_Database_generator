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
pattern = r'src="(.*?)"'
url = "https://bulbapedia.bulbagarden.net/wiki/Alolan_form"
img_max_size = 2
try:
    r = requests.get(url, timeout=10)
    if r.status_code == 200:
        matches = re.findall(pattern, r.text, re.DOTALL)
        for match in matches:
            # print(match)
            if "Alola.png" in match and "100px" in match:
                time.sleep(2)
                print(match)
                name_to_trim = match.split('/')[-1].replace("100px-","").replace("-","_").lower()
                name = re.sub(r"^\d+", "", name_to_trim)
                print(name)
                img_r = requests.get(match, timeout=10)

                if img_r.status_code == 200:
                    os.makedirs("../images", exist_ok=True)
                    local_png = f"../images/{name}"
                    # sauvegarde locale (cache)
                    with open(local_png, "wb") as f:
                        f.write(img_r.content)
                    skip = True
                    img = Image(BytesIO(img_r.content), width=img_max_size * cm, height=img_max_size * cm)
                    img.hAlign = "CENTER"
    else:
        print("#TODO")

except Exception:
    pass

