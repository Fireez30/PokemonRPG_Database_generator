import json
import requests
from io import BytesIO
import os
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Image,
    Frame,
    PageTemplate,
    FrameBreak
)

from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import cm


def load_pokemon(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def get_pokemon_image(name):
    folder = "images"

    local_jpg = os.path.join(folder, f"{name}.jpg")
    local_png = os.path.join(folder, f"{name}.png")

    # --- 1. Vérifie si image locale existe

    if os.path.exists(local_jpg):
        img = Image(local_jpg, width=5 * cm, height=5 * cm)
        img.hAlign = "CENTER"
        return img

    if os.path.exists(local_png):
        img = Image(local_png, width=5 * cm, height=5 * cm)
        img.hAlign = "CENTER"
        return img

    # --- 2. Sinon télécharger

    url = f"https://img.pokemondb.net/artwork/{name}.jpg"

    try:
        r = requests.get(url, timeout=10)

        if r.status_code == 200:
            os.makedirs(folder, exist_ok=True)

            # sauvegarde locale (cache)
            with open(local_jpg, "wb") as f:
                f.write(r.content)

            img = Image(BytesIO(r.content), width=6 * cm, height=6 * cm)
            img.hAlign = "CENTER"

            return img

    except Exception:
        pass

    return None


def format_capabilities(capabilities):

    items = []

    for c in capabilities:
        if c["value"]:
            items.append(f'{c["name"]} {c["value"]}')
        else:
            items.append(c["name"])

    return ", ".join(items)


def format_skills(skills):

    return ", ".join(
        f'{s["name"]} {s["roll"]}'
        for s in skills
    )


def create_pdf(data, output="pokemon.pdf"):

    styles = getSampleStyleSheet()

    doc = SimpleDocTemplate(
        output,
        leftMargin=1.5 * cm,
        rightMargin=1.5 * cm,
        topMargin=1.5 * cm,
        bottomMargin=1.5 * cm
    )

    # --- 2 COLONNES
    col_width = doc.width / 2 - 0.25 * cm
    frame_left = Frame(
        doc.leftMargin,
        doc.bottomMargin,
        col_width,
        doc.height,
        id='left'
    )

    frame_right = Frame(
        doc.leftMargin + col_width + 0.5 * cm,
        doc.bottomMargin,
        col_width,
        doc.height,
        id='right'
    )

    doc.addPageTemplates([
        PageTemplate(id='TwoCol', frames=[frame_left, frame_right])
    ])

    story = []

    # -------- IMAGE --------

    img = get_pokemon_image(data["name"])

    if img:
        story.append(img)
        story.append(Spacer(1,10))

    # -------- NAME --------

    story.append(Paragraph(f"<b>{data['name'].upper()}</b>", styles["Title"]))
    story.append(Spacer(1,10))

    # -------- BASE STATS --------

    story.append(Paragraph("<b>Base Stats</b>", styles["Heading3"]))

    stats = [
        f"HP: {data['stat_hp']}",
        f"Attack: {data['stat_atk']}",
        f"Defense: {data['stat_def']}",
        f"SpAtk: {data['stat_sp_atk']}",
        f"SpDef: {data['stat_sp_def']}",
        f"Speed: {data['stat_spd']}",
    ]

    for s in stats:
        story.append(Paragraph(s, styles["Normal"]))

    story.append(Spacer(1,10))

    # -------- BASIC INFO --------

    story.append(Paragraph("<b>Basic Information</b>", styles["Heading3"]))

    story.append(
        Paragraph(
            f"Type: {' / '.join(data['pokemon_types'])}",
            styles["Normal"]
        )
    )

    for i, a in enumerate(data["base_abilities"], 1):
        story.append(
            Paragraph(f"Basic Ability {i}: {a}", styles["Normal"])
        )

    for i, a in enumerate(data["advanced_abilities"], 1):
        story.append(
            Paragraph(f"Adv Ability {i}: {a}", styles["Normal"])
        )

    for a in data["high_abilities"]:
        story.append(
            Paragraph(f"High Ability: {a}", styles["Normal"])
        )

    story.append(Spacer(1,10))

    # -------- EVOLUTION --------

    story.append(Paragraph("<b>Evolution</b>", styles["Heading3"]))

    for e in data["evolutions"]:
        story.append(Paragraph(e, styles["Normal"]))

    story.append(Spacer(1,10))

    # -------- SIZE --------

    story.append(Paragraph("<b>Size Information</b>", styles["Heading3"]))

    story.append(
        Paragraph(f"Height: {data['height']}", styles["Normal"])
    )

    story.append(
        Paragraph(f"Weight: {data['weight']}", styles["Normal"])
    )

    story.append(Spacer(1,10))

    # -------- BREEDING --------

    story.append(Paragraph("<b>Breeding Information</b>", styles["Heading3"]))

    story.append(
        Paragraph(
            f"Gender Ratio: {data['gender_ratio_m']}% M / {data['gender_ratio_f']}% F",
            styles["Normal"]
        )
    )

    story.append(
        Paragraph(
            f"Egg Group: {data['egg_group']}",
            styles["Normal"]
        )
    )

    story.append(
        Paragraph(
            f"Diet: {data['diet']}",
            styles["Normal"]
        )
    )

    story.append(
        Paragraph(
            f"Habitat: {data['habitat']}",
            styles["Normal"]
        )
    )

    # -------- COLONNE DROITE --------

    story.append(FrameBreak())

    # -------- CAPABILITIES --------

    story.append(Paragraph("<b>Capability List</b>", styles["Heading3"]))

    story.append(
        Paragraph(
            format_capabilities(data["capabilities"]),
            styles["Normal"]
        )
    )

    story.append(Spacer(1,10))

    # -------- SKILLS --------

    story.append(Paragraph("<b>Skill List</b>", styles["Heading3"]))

    story.append(
        Paragraph(
            format_skills(data["skills"]),
            styles["Normal"]
        )
    )

    story.append(Spacer(1,10))

    # -------- MOVE LIST --------

    story.append(Paragraph("<b>Level Up Move List</b>", styles["Heading3"]))

    for m in data["moves"]:
        story.append(
            Paragraph(
                f"{m['level']} {m['name']} - {m['type'].strip()}",
                styles["Normal"]
            )
        )

    story.append(Spacer(1,10))

    # -------- EGG MOVES --------

    if data["egg_moves"]:
        story.append(Paragraph("<b>Egg Move List</b>", styles["Heading3"]))

        story.append(
            Paragraph(
                ", ".join(data["egg_moves"]),
                styles["Normal"]
            )
        )

        story.append(Spacer(1,10))

    # -------- TM MOVES --------

    story.append(Paragraph("<b>TM/HM List</b>", styles["Heading3"]))

    story.append(
        Paragraph(
            ", ".join(data["tm_moves"]),
            styles["Normal"]
        )
    )

    story.append(Spacer(1,10))

    # -------- TUTOR MOVES --------

    story.append(Paragraph("<b>Tutor Move List</b>", styles["Heading3"]))

    story.append(
        Paragraph(
            ", ".join(data["tutor_moves"]),
            styles["Normal"]
        )
    )

    doc.build(story)


if __name__ == "__main__":

    pokemon = load_pokemon("data/pokemon_test.json")
    for poke in pokemon:
        create_pdf(poke, "output_pdf/"+poke["name"]+".pdf")