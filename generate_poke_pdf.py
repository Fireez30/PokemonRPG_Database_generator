import json
import requests
from io import BytesIO
from reportlab.lib import utils
from pypdf import PdfWriter
import glob
import os
from reportlab.platypus import (
    SimpleDocTemplate,
    Table,
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

def get_image(path, width=1*cm):
    img = utils.ImageReader(path)
    iw, ih = img.getSize()
    aspect = ih / float(iw)
    return Image(path, width=width, height=(width * aspect))

def get_pokemon_image(name):
    folder = "images"

    local_jpg = os.path.join(folder, f"{name}.jpg")
    local_png = os.path.join(folder, f"{name}.png")

    # --- 1. Vérifie si image locale existe

    if os.path.exists(local_jpg):
        img = get_image(local_jpg, width=3 * cm)
        img.hAlign = "CENTER"
        return img

    if os.path.exists(local_png):
        img =  get_image(local_png, width=3 * cm)
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

            img = Image(BytesIO(r.content), width=3 * cm, height=3 * cm)
            img.hAlign = "CENTER"

            return img
        else:
            url = f"https://forwardfeed.github.io/ER-nextdex/sprites/{name.upper().replace(" ","_")}.png"
            r = requests.get(url, timeout=10)

            if r.status_code == 200:
                os.makedirs(folder, exist_ok=True)

                # sauvegarde locale (cache)
                with open(local_png, "wb") as f:
                    f.write(r.content)

                img = Image(BytesIO(r.content), width=3 * cm, height=3 * cm)
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
    from reportlab.lib.colors import white, black
    from reportlab.lib.enums import TA_LEFT, TA_CENTER
    from reportlab.lib.styles import ParagraphStyle,StyleSheet1
    from reportlab.lib.fonts import tt2ps
    from reportlab.rl_config import canvas_basefontname as _baseFontName
    _baseFontNameB = tt2ps(_baseFontName, 1, 0)
    _baseFontNameI = tt2ps(_baseFontName, 0, 1)
    _baseFontNameBI = tt2ps(_baseFontName, 1, 1)
    styles = StyleSheet1()

    styles.add(ParagraphStyle(name='Normal',
                                  fontName=_baseFontName,
                                  fontSize=8,
                                  leading=12)
                   )

    styles.add(ParagraphStyle(name='BodyText',
                                  parent=styles['Normal'],
                                  spaceBefore=6)
                   )
    styles.add(ParagraphStyle(name='Italic',
                                  parent=styles['BodyText'],
                                  fontName = _baseFontNameI)
                   )

    styles.add(ParagraphStyle(name='Heading1',
                                  parent=styles['Normal'],
                                  fontName = _baseFontNameB,
                                  fontSize=18,
                                  leading=22,
                                  spaceAfter=6),
                                    alias='h1')

    styles.add(ParagraphStyle(name='Title',
                                  parent=styles['Normal'],
                                  fontName = _baseFontNameB,
                                  fontSize=18,
                                  leading=22,
                                  alignment=TA_CENTER,
                                  spaceAfter=6),
                   alias='title')

    styles.add(ParagraphStyle(name='Heading2',
                                  parent=styles['Normal'],
                                  fontName = _baseFontNameB,
                                  fontSize=14,
                                  leading=18,
                                  spaceBefore=12,
                                  spaceAfter=6),
                   alias='h2')

    styles.add(ParagraphStyle(name='Heading3',
                                  parent=styles['Normal'],
                                  fontName = _baseFontNameBI,
                                  fontSize=12,
                                  leading=14,
                                  spaceBefore=12,
                                  spaceAfter=6),
                   alias='h3')

    styles.add(ParagraphStyle(name='Heading4',
                                  parent=styles['Normal'],
                                  fontName = _baseFontNameBI,
                                  fontSize=10,
                                  leading=12,
                                  spaceBefore=10,
                                  spaceAfter=4),
                   alias='h4')

    styles.add(ParagraphStyle(name='Heading5',
                                  parent=styles['Normal'],
                                  fontName = _baseFontNameB,
                                  fontSize=9,
                                  leading=10.8,
                                  spaceBefore=8,
                                  spaceAfter=4),
                   alias='h5')

    styles.add(ParagraphStyle(name='Heading6',
                                  parent=styles['Normal'],
                                  fontName = _baseFontNameB,
                                  fontSize=7,
                                  leading=8.4,
                                  spaceBefore=6,
                                  spaceAfter=2),
                   alias='h6')

    styles.add(ParagraphStyle(name='Bullet',
                                  parent=styles['Normal'],
                                  firstLineIndent=0,
                                  spaceBefore=3),
                   alias='bu')

    styles.add(ParagraphStyle(name='Definition',
                                  parent=styles['Normal'],
                                  firstLineIndent=0,
                                  leftIndent=36,
                                  bulletIndent=0,
                                  spaceBefore=6,
                                  bulletFontName=_baseFontNameBI),
                   alias='df')

    styles.add(ParagraphStyle(name='Code',
                                  parent=styles['Normal'],
                                  fontName='Courier',
                                  fontSize=8,
                                  leading=8.8,
                                  firstLineIndent=0,
                                  leftIndent=36))


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
    # -------- NAME --------

    story.append(Paragraph(f"<b>{data['name'].capitalize()}</b>", styles["Title"]))
    story.append(Spacer(1,5))
    # -------- IMAGE --------

    img = get_pokemon_image(data["name"])

    if img:
        story.append(img)
        story.append(Spacer(1,5))



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

    story.append(Spacer(1,5))

    # -------- BASIC INFO --------

    story.append(Paragraph("<b>Basic Information</b>", styles["Heading3"]))

    if type(data['pokemon_types']) == str:
        story.append(
            Paragraph(
                f"Type: {data['pokemon_types']}",
                styles["Normal"]
            )
        )
    else:
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

    story.append(Spacer(1,5))

    # -------- EVOLUTION --------

    story.append(Paragraph("<b>Evolution</b>", styles["Heading3"]))

    for e in data["evolutions"]:
        story.append(Paragraph(e, styles["Normal"]))

    story.append(Spacer(1,5))

    # -------- SIZE --------

    story.append(Paragraph("<b>Size Information</b>", styles["Heading3"]))

    story.append(
        Paragraph(f"Height: {data['height']}", styles["Normal"])
    )

    story.append(
        Paragraph(f"Weight: {data['weight']}", styles["Normal"])
    )

    story.append(Spacer(1,5))

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

    # -------- CAPABILITIES --------

    story.append(Paragraph("<b>Capability List</b>", styles["Heading3"]))

    story.append(
        Paragraph(
            format_capabilities(data["capabilities"]),
            styles["Normal"]
        )
    )

    story.append(Spacer(1,5))
    # -------- SKILLS --------
    story.append(Paragraph("<b>Skill List</b>", styles["Heading3"]))

    story.append(
        Paragraph(
            format_skills(data["skills"]),
            styles["Normal"]
        )
    )

    # -------- COLONNE DROITE --------

    story.append(FrameBreak())
    # -------- MOVE LIST --------

    story.append(Paragraph("<b>Move List</b>", styles["Heading3"]))

    for m in data["moves"]:
        story.append(
            Paragraph(
                f"{m['level']} {m['name']} - {m['type'].strip()}",
                styles["Normal"]
            )
        )

    story.append(Spacer(1,5))

    # -------- EGG MOVES --------

    if data["egg_moves"]:
        story.append(Paragraph("<b>Egg Move List</b>", styles["Heading3"]))

        story.append(
            Paragraph(
                ", ".join(data["egg_moves"]),
                styles["Normal"]
            )
        )

        story.append(Spacer(1,5))

    # -------- TM MOVES --------

    story.append(Paragraph("<b>TM/HM List</b>", styles["Heading3"]))

    story.append(
        Paragraph(
            ", ".join(data["tm_moves"]),
            styles["Normal"]
        )
    )

    story.append(Spacer(1,5))

    # -------- TUTOR MOVES --------

    story.append(Paragraph("<b>Tutor Move List</b>", styles["Heading3"]))

    story.append(
        Paragraph(
            ", ".join(data["tutor_moves"]),
            styles["Normal"]
        )
    )

    if data["mega_evolution"] is not None:
        story.append(Spacer(1, 10))
        mega_name = data["name"]+"-mega"
        if "redux" in data["name"].lower():
            mega_name = data["name"].replace("Redux","Mega Redux")

        img = get_pokemon_image(mega_name)
        if type(data["mega_evolution"]["type"]) == str:
            mega_evo_types = data["mega_evolution"]["type"]
        else:
            mega_evo_types = ' / '.join(data["mega_evolution"]["type"])
        mega_evo_ability = data["mega_evolution"]["ability"]
        mega_evo_stats = data["mega_evolution"]["stats"].replace("Speed PokéDex Update. ","")
        title = Paragraph("Mega Evolution", styles["Heading3"])
        data_text = "Type : "+str(mega_evo_types)+"<br></br>"
        data_text += "Ability : "+str(mega_evo_ability)+"<br></br><br></br>"
        data_text += "Stats : "+str(mega_evo_stats)+"<br></br>"
        mega_data = Paragraph(data_text, styles["Normal"])
        # Création d'un tableau pour aligner l'image et le texte
        final_table_data = [
            [img, [title,mega_data]]
        ]

        final_table = Table(final_table_data, colWidths=[3.5 * cm, 5.5 * cm])
        story.append(
            final_table
        )

    doc.build(story)



if __name__ == "__main__":

    pokemon = load_pokemon("data/final_pokemons.json")
    for poke in pokemon:
        create_pdf(poke, "output_pdf/"+poke["name"]+".pdf")

    merger = PdfWriter()

    pdfs = list(filter(os.path.isfile, glob.glob("output_pdf/*.pdf")))
    pdfs.sort(key=os.path.basename)

    for pdf in pdfs:
        if pdf != "output_pdf/'.pdf":
            merger.append(pdf)

    merger.write("output_pdf/merged_dex.pdf")
    merger.close()