import streamlit as st
import random
import time
from datetime import datetime
import io
from reportlab.lib.pagesizes import A4, landscape
from reportlab.pdfgen import canvas
from reportlab.lib import colors

# ==========================================
# STATIO LATIJN TRAINER - DATABANK & LOGICA
# Gebaseerd op Systematische woordenlijst Stationes I-VIII & Leren Leren Grammatica
# ==========================================

VOCABULARY = [
    # Substantieven 1e klasse -a (vr)
    {"nom": "lingua", "gen": "linguae", "geslacht": "vr", "klasse": "1_a", "vertaling": "de taal; de tong", "tekst": 1},
    {"nom": "pecunia", "gen": "pecuniae", "geslacht": "vr", "klasse": "1_a", "vertaling": "het geld", "tekst": 1},
    {"nom": "umbra", "gen": "umbrae", "geslacht": "vr", "klasse": "1_a", "vertaling": "de schaduw", "tekst": 1},
    {"nom": "via", "gen": "viae", "geslacht": "vr", "klasse": "1_a", "vertaling": "de weg", "tekst": 12},
    {"nom": "puella", "gen": "puellae", "geslacht": "vr", "klasse": "1_a", "vertaling": "het meisje", "tekst": 12},
    {"nom": "patria", "gen": "patriae", "geslacht": "vr", "klasse": "1_a", "vertaling": "het vaderland", "tekst": 3},
    {"nom": "filia", "gen": "filiae", "geslacht": "vr", "klasse": "1_a", "vertaling": "de dochter", "tekst": 4},
    {"nom": "ripa", "gen": "ripae", "geslacht": "vr", "klasse": "1_a", "vertaling": "de oever", "tekst": 5},
    {"nom": "roma", "gen": "romae", "geslacht": "vr", "klasse": "1_a", "vertaling": "Rome", "tekst": 8},
    {"nom": "aqua", "gen": "aquae", "geslacht": "vr", "klasse": "1_a", "vertaling": "het water", "tekst": 17},

    # Substantieven 1e klasse -us (m)
    {"nom": "hortus", "gen": "horti", "geslacht": "m", "klasse": "1_us", "vertaling": "de tuin", "tekst": 1},
    {"nom": "servus", "gen": "servi", "geslacht": "m", "klasse": "1_us", "vertaling": "de slaaf", "tekst": 2},
    {"nom": "amicus", "gen": "amici", "geslacht": "m", "klasse": "1_us", "vertaling": "de vriend", "tekst": 3},
    {"nom": "filius", "gen": "filii", "geslacht": "m", "klasse": "1_us", "vertaling": "de zoon", "tekst": 3},
    {"nom": "annus", "gen": "anni", "geslacht": "m", "klasse": "1_us", "vertaling": "het jaar", "tekst": 4},
    {"nom": "deus", "gen": "dei", "geslacht": "m", "klasse": "1_us", "vertaling": "de god", "tekst": 6},
    {"nom": "murus", "gen": "muri", "geslacht": "m", "klasse": "1_us", "vertaling": "de muur", "tekst": 7},
    {"nom": "dominus", "gen": "domini", "geslacht": "m", "klasse": "1_us", "vertaling": "de heer, de meester", "tekst": 34},
    {"nom": "equus", "gen": "equi", "geslacht": "m", "klasse": "1_us", "vertaling": "het paard", "tekst": 12},

    # Substantieven 1e klasse -um (onz)
    {"nom": "arma", "gen": "armorum", "geslacht": "onz", "klasse": "1_um", "vertaling": "de wapens", "tekst": 1},
    {"nom": "verbum", "gen": "verbi", "geslacht": "onz", "klasse": "1_um", "vertaling": "het woord", "tekst": 1},
    {"nom": "vinum", "gen": "vini", "geslacht": "onz", "klasse": "1_um", "vertaling": "de wijn", "tekst": 1},
    {"nom": "bellum", "gen": "belli", "geslacht": "onz", "klasse": "1_um", "vertaling": "de oorlog", "tekst": 3},
    {"nom": "oppidum", "gen": "oppidi", "geslacht": "onz", "klasse": "1_um", "vertaling": "de stad", "tekst": 3},
    {"nom": "regnum", "gen": "regni", "geslacht": "onz", "klasse": "1_um", "vertaling": "het koningschap, het rijk", "tekst": 4},
    {"nom": "consilium", "gen": "consilii", "geslacht": "onz", "klasse": "1_um", "vertaling": "de raad, het advies", "tekst": 6},

    # Substantieven 2e klasse m/vr (-is genitief)
    {"nom": "flos", "gen": "floris", "geslacht": "m", "klasse": "2_mvr", "stam": "flor", "vertaling": "de bloem", "tekst": 1},
    {"nom": "mater", "gen": "matris", "geslacht": "vr", "klasse": "2_mvr", "stam": "matr", "vertaling": "de moeder", "tekst": 1},
    {"nom": "rex", "gen": "regis", "geslacht": "m", "klasse": "2_mvr", "stam": "reg", "vertaling": "de koning", "tekst": 3},
    {"nom": "pater", "gen": "patris", "geslacht": "m", "klasse": "2_mvr", "stam": "patr", "vertaling": "de vader", "tekst": 3},
    {"nom": "urbs", "gen": "urbis", "geslacht": "vr", "klasse": "2_mvr", "stam": "urb", "vertaling": "de stad", "tekst": 3},
    {"nom": "miles", "gen": "militis", "geslacht": "m", "klasse": "2_mvr", "stam": "milit", "vertaling": "de soldaat", "tekst": 2},
    {"nom": "civitas", "gen": "civitatis", "geslacht": "vr", "klasse": "2_mvr", "stam": "civitat", "vertaling": "de gemeenschap, de staat", "tekst": 8},
    {"nom": "hostis", "gen": "hostis", "geslacht": "m", "klasse": "2_mvr", "stam": "host", "vertaling": "de vijand", "tekst": 9},

    # Substantieven 2e klasse onzijdig
    {"nom": "corpus", "gen": "corporis", "geslacht": "onz", "klasse": "2_onz", "stam": "corpor", "vertaling": "het lichaam", "tekst": 1},
    {"nom": "tempus", "gen": "temporis", "geslacht": "onz", "klasse": "2_onz", "stam": "tempor", "vertaling": "de tijd", "tekst": 1},
    {"nom": "caput", "gen": "capitis", "geslacht": "onz", "klasse": "2_onz", "stam": "capit", "vertaling": "het hoofd", "tekst": 11},
    {"nom": "flumen", "gen": "fluminis", "geslacht": "onz", "klasse": "2_onz", "stam": "flumin", "vertaling": "de rivier", "tekst": 20},

    # Adjectieven 1e klasse (-us, -a, -um)
    {"nom_m": "bonus", "nom_v": "bona", "nom_o": "bonum", "klasse": "adj_1", "vertaling": "goed", "tekst": 34},
    {"nom_m": "altus", "nom_v": "alta", "nom_o": "altum", "klasse": "adj_1", "vertaling": "hoog; diep", "tekst": 16},
    {"nom_m": "magnus", "nom_v": "magna", "nom_o": "magnum", "klasse": "adj_1", "vertaling": "groot", "tekst": 8},
    {"nom_m": "parvus", "nom_v": "parva", "nom_o": "parvum", "klasse": "adj_1", "vertaling": "klein", "tekst": 31},
    {"nom_m": "novus", "nom_v": "nova", "nom_o": "novum", "klasse": "adj_1", "vertaling": "nieuw", "tekst": 1},

    # Adjectieven 2e klasse (-is, -is, -e)
    {"nom_m": "fortis", "nom_v": "fortis", "nom_o": "forte", "stam": "fort", "klasse": "adj_2", "vertaling": "moedig, dapper, sterk", "tekst": 34},
    {"nom_m": "omnis", "nom_v": "omnis", "nom_o": "omne", "stam": "omn", "klasse": "adj_2", "vertaling": "geheel, al, ieder", "tekst": 1},
    {"nom_m": "crudelis", "nom_v": "crudelis", "nom_o": "crudele", "stam": "crudel", "klasse": "adj_2", "vertaling": "wreed, hard", "tekst": 32}
]

ENDINGS = {
    "1_a": {
        "nom_sing": "a", "voc_sing": "a", "acc_sing": "am", "gen_sing": "ae", "dat_sing": "ae", "abl_sing": "a",
        "nom_plur": "ae", "voc_plur": "ae", "acc_plur": "as", "gen_plur": "arum", "dat_plur": "is", "abl_plur": "is"
    },
    "1_us": {
        "nom_sing": "us", "voc_sing": "e", "acc_sing": "um", "gen_sing": "i", "dat_sing": "o", "abl_sing": "o",
        "nom_plur": "i", "voc_plur": "i", "acc_plur": "os", "gen_plur": "orum", "dat_plur": "is", "abl_plur": "is"
    },
    "1_um": {
        "nom_sing": "um", "voc_sing": "um", "acc_sing": "um", "gen_sing": "i", "dat_sing": "o", "abl_sing": "o",
        "nom_plur": "a", "voc_plur": "a", "acc_plur": "a", "gen_plur": "orum", "dat_plur": "is", "abl_plur": "is"
    },
    "2_mvr": {
        "nom_sing": "", "voc_sing": "", "acc_sing": "em", "gen_sing": "is", "dat_sing": "i", "abl_sing": "e",
        "nom_plur": "es", "voc_plur": "es", "acc_plur": "es", "gen_plur": "um", "dat_plur": "ibus", "abl_plur": "ibus"
    },
    "2_onz": {
        "nom_sing": "", "voc_sing": "", "acc_sing": "", "gen_sing": "is", "dat_sing": "i", "abl_sing": "e",
        "nom_plur": "a", "voc_plur": "a", "acc_plur": "a", "gen_plur": "um", "dat_plur": "ibus", "abl_plur": "ibus"
    }
}

CASE_NAMES = {
    "nom_sing": "nominatief enkelvoud",
    "gen_sing": "genitief enkelvoud",
    "dat_sing": "datief enkelvoud",
    "acc_sing": "accusatief enkelvoud",
    "abl_sing": "ablatief enkelvoud",
    "nom_plur": "nominatief meervoud",
    "gen_plur": "genitief meervoud",
    "dat_plur": "datief meervoud",
    "acc_plur": "accusatief meervoud",
    "abl_plur": "ablatief meervoud"
}


def generate_pdf_certificate(student_name, student_class, score, total, tekst_num, elapsed_minutes):
    """Genereert een PDF Certificaat van Deelname via ReportLab."""
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=landscape(A4))
    width, height = landscape(A4)

    # Buitenste kader (Sjiek klassiek Latijns blauw/goud)
    c.setLineWidth(4)
    c.setStrokeColor(colors.HexColor('#1E3A8A')) # Donkerblauw
    c.rect(20, 20, width - 40, height - 40)

    c.setLineWidth(1.5)
    c.setStrokeColor(colors.HexColor('#D97706')) # Goud
    c.rect(28, 28, width - 56, height - 56)

    # Titel
    c.setFont("Helvetica-Bold", 26)
    c.setFillColor(colors.HexColor('#1E3A8A'))
    c.drawCentredString(width / 2, height - 85, "CERTIFICAAT VAN OEFENSESSIE LATIJN")

    c.setFont("Helvetica", 16)
    c.setFillColor(colors.HexColor('#4B5563'))
    c.drawCentredString(width / 2, height - 115, "Statio Latijn Trainer — Eerste Graad")

    # Decoratieve lijn
    c.setLineWidth(1)
    c.setStrokeColor(colors.HexColor('#D97706'))
    c.line(width / 2 - 150, height - 130, width / 2 + 150, height - 130)

    # Inhoud
    c.setFont("Helvetica", 14)
    c.setFillColor(colors.HexColor('#1F2937'))
    c.drawCentredString(width / 2, height - 175, "Dit officieel certificaat bevestigt dat")

    # Naam & Klas
    display_name = f"{student_name} ({student_class})" if student_class else (student_name if student_name else "Leerling Latijn")
    c.setFont("Helvetica-Bold", 22)
    c.setFillColor(colors.HexColor('#1E3A8A'))
    c.drawCentredString(width / 2, height - 210, display_name)

    c.setFont("Helvetica", 14)
    c.setFillColor(colors.HexColor('#374151'))
    c.drawCentredString(width / 2, height - 250, f"zelfstandig een oefensessie Latijn van {elapsed_minutes} minuten heeft voltooid.")
    c.drawCentredString(width / 2, height - 275, f"Geselecteerd niveau: Teksten 1 t/m {tekst_num} (Systematische woordenlijst Stationes I - VIII)")

    # Resultatenbox
    pct = round((score / total) * 100) if total > 0 else 0
    c.setLineWidth(1)
    c.setStrokeColor(colors.HexColor('#CBD5E1'))
    c.setFillColor(colors.HexColor('#F8FAFC'))
    c.roundRect(width / 2 - 170, height - 365, 340, 65, 8, stroke=1, fill=1)

    c.setFont("Helvetica-Bold", 16)
    c.setFillColor(colors.HexColor('#1E3A8A'))
    c.drawCentredString(width / 2, height - 330, f"Behaalde Score: {score} / {total} ({pct}%)")
    
    date_str = datetime.now().strftime("%d-%m-%Y om %H:%M")
    c.setFont("Helvetica", 11)
    c.setFillColor(colors.HexColor('#4B5563'))
    c.drawCentredString(width / 2, height - 352, f"Datum voltooiing: {date_str}")

    # Footer
    c.setFont("Helvetica-Oblique", 10)
    c.setFillColor(colors.HexColor('#6B7280'))
    c.drawCentredString(width / 2, 48, "Statio Latijn Trainer • Ingezonden als bewijs voor de leerkracht Latijn")

    c.showPage()
    c.save()
    buffer.seek(0)
    return buffer.getvalue()


# Streamlit App Layout
st.set_page_config(page_title="Statio Latijn Trainer", page_icon="🏛️", layout="centered")

st.title("🏛️ Statio Latijn Trainer")
st.subheader("Oefenplatform Latijn — Eerste Graad (Stationes I - VIII)")

# Session State Initialisatie
if "start_time" not in st.session_state:
    st.session_state.start_time = time.time()
if "score" not in st.session_state:
    st.session_state.score = 0
if "total" not in st.session_state:
    st.session_state.total = 0
if "repeat_queue" not in st.session_state:
    st.session_state.repeat_queue = []

# Sidebar Menu & Instellingen
st.sidebar.header("⚙️ Instellingen & Sessie")
student_name = st.sidebar.text_input("Naam leerling:", placeholder="bv. Sophie De Smet")
student_class = st.sidebar.text_input("Klas:", placeholder="bv. 1A1")

max_tekst = st.sidebar.slider("Selecteer hoogste tekstnummer (1 - 41):", min_value=1, max_value=41, value=15)
module = st.sidebar.radio("Kies Oefenmodule:", [
    "2. Basismodule: Determineren",
    "3. Uitbreidingsmodule: Verbuigen",
    "📜 Sessie Afronden & PDF Certificaat"
])

# Timer berekenen
elapsed_seconds = int(time.time() - st.session_state.start_time)
elapsed_minutes = max(1, round(elapsed_seconds / 60))

st.sidebar.markdown("---")
st.sidebar.metric("⏱️ Verstreken Tijd", f"{elapsed_minutes} min")
st.sidebar.metric("📊 Behaalde Score", f"{st.session_state.score} / {st.session_state.total}")

if len(st.session_state.repeat_queue) > 0:
    st.sidebar.info(f"🔄 **Herhalingswachtrij**: {len(st.session_state.repeat_queue)} vorm(en) om te herhalen!")

# Available vocabulary
available_words = [w for w in VOCABULARY if w["tekst"] <= max_tekst]

if module == "2. Basismodule: Determineren":
    st.header("📝 Module 2: Determineren")
    st.markdown("Analyseer de getoonde Latijnse vorm uit de geselecteerde leesteksten.")

    if not available_words:
        st.warning("Geen woorden beschikbaar voor dit tekstnummer. Verhoog de schuifbalk in de zijbalk.")
    else:
        if "current_item" not in st.session_state or st.button("🔄 Volgende Vorm"):
            # Check if there are repeated items first (spaced repetition)
            if len(st.session_state.repeat_queue) > 0 and random.random() < 0.5:
                item = st.session_state.repeat_queue.pop(0)
                st.session_state.current_item = item
                st.session_state.is_repeat = True
            else:
                word = random.choice(available_words)
                if "nom" in word:
                    klasse = word["klasse"]
                    case_key = random.choice(list(ENDINGS[klasse].keys()))
                    ending = ENDINGS[klasse][case_key]
                    if klasse.startswith("1_"):
                        base = word["nom"][:-len(ENDINGS[klasse]["nom_sing"])] if ENDINGS[klasse]["nom_sing"] else word["nom"]
                        form = base + ending
                    else:
                        form = word["nom"] if case_key in ["nom_sing", "voc_sing"] and klasse != "1_um" else word.get("stam", word["nom"]) + ending

                    st.session_state.current_item = {
                        "word": word,
                        "form": form,
                        "case_key": case_key,
                        "type": "substantief"
                    }
                    st.session_state.is_repeat = False

        item = st.session_state.get("current_item", None)
        if item:
            if st.session_state.get("is_repeat", False):
                st.warning("🔄 **Herhalingsvraag**: Deze vorm maakte je eerder fout in deze sessie!")

            st.info(f"### Verbogen vorm: **{item['form']}**")

            col1, col2 = st.columns(2)
            with col1:
                ans_case = st.selectbox("Naamval + Getal:", list(CASE_NAMES.values()))
            with col2:
                ans_geslacht = st.selectbox("Geslacht:", ["mannelijk", "vrouwelijk", "onzijdig"])

            ans_vertaling = st.text_input("Vertaling (of kernwoord):")

            if st.button("Controleer Antwoord"):
                st.session_state.total += 1
                correct_geslacht = {"m": "mannelijk", "vr": "vrouwelijk", "onz": "onzijdig"}[item["word"]["geslacht"]]
                correct_case_name = CASE_NAMES[item["case_key"]]

                is_correct = True
                feedback = []

                if ans_case == correct_case_name:
                    feedback.append(f"✅ Naamval/getal is correct! ({correct_case_name})")
                else:
                    feedback.append(f"❌ Naamval/getal is fout. Correct: **{correct_case_name}**")
                    is_correct = False

                if correct_geslacht == ans_geslacht:
                    feedback.append(f"✅ Geslacht is correct! ({correct_geslacht})")
                else:
                    feedback.append(f"❌ Geslacht is fout. Correct: **{correct_geslacht}**")
                    is_correct = False

                if item["word"]["vertaling"].lower() in ans_vertaling.lower() or ans_vertaling.lower() in item["word"]["vertaling"].lower():
                    feedback.append(f"✅ Vertaling is goed! ({item['word']['vertaling']})")
                else:
                    feedback.append(f"💡 Verwachte vertaling: **{item['word']['vertaling']}**")

                if is_correct:
                    st.success("🎉 Uitstekend! Je hebt deze vorm volledig juist ingevuld.")
                    st.session_state.score += 1
                else:
                    st.error("Nog niet helemaal juist. Deze vorm komt later in deze sessie terug!")
                    st.session_state.repeat_queue.append(item)

                for f in feedback:
                    st.write(f)

elif module == "3. Uitbreidingsmodule: Verbuigen":
    st.header("⚡ Module 3: Verbuigen & Concordantie")
    st.markdown("Zet de verbinding van een substantief en adjectief in de gevraagde naamval en het getal.")

    substantieven = [w for w in available_words if "nom" in w]
    adjectieven_1 = [w for w in VOCABULARY if w.get("klasse") == "adj_1" and w["tekst"] <= max_tekst]

    if not substantieven or not adjectieven_1:
        st.warning("Onvoldoende woorden beschikbaar voor verbuiging in de gekozen teksten.")
    else:
        if "conjugate_item" not in st.session_state or st.button("🔄 Nieuwe Combinatie"):
            sub = random.choice(substantieven)
            adj = random.choice(adjectieven_1)
            case_key = random.choice(list(ENDINGS[sub["klasse"]].keys()))

            st.session_state.conjugate_item = {
                "sub": sub,
                "adj": adj,
                "case_key": case_key
            }

        c_item = st.session_state.get("conjugate_item", None)
        if c_item:
            target_case = CASE_NAMES[c_item["case_key"]]
            st.info(f"### Combineer: **{c_item['sub']['nom']}** + **{c_item['adj']['nom_m']}**\n👉 Gevraagde vorm: **{target_case}**")

            user_input = st.text_input("Typ de volledige verbogen combinatie (bv. dominorum bonorum):")

            if st.button("Controleer Verbuiging"):
                st.session_state.total += 1
                # Bereken correcte uitgangen
                sub_kl = c_item["sub"]["klasse"]
                sub_ending = ENDINGS[sub_kl][c_item["case_key"]]
                sub_base = c_item["sub"]["nom"][:-len(ENDINGS[sub_kl]["nom_sing"])] if ENDINGS[sub_kl]["nom_sing"] else c_item["sub"]["nom"]
                sub_form = sub_base + sub_ending

                # Adjectief stem volgens geslacht van substantief
                g = c_item["sub"]["geslacht"]
                adj_kl = "1_us" if g == "m" else ("1_a" if g == "vr" else "1_um")
                adj_ending = ENDINGS[adj_kl][c_item["case_key"]]
                adj_base = c_item["adj"]["nom_m"][:-2]
                adj_form = adj_base + adj_ending

                correct_combination = f"{sub_form} {adj_form}".lower().strip()

                if user_input.lower().strip() == correct_combination:
                    st.success(f"🎉 Fantastisch! **{correct_combination}** is helemaal correct gespeld en volgt de NGG-regel!")
                    st.session_state.score += 1
                else:
                    st.error(f"❌ Niet juist. De correcte vorm is: **{correct_combination}**")

elif module == "📜 Sessie Afronden & PDF Certificaat":
    st.header("📜 Sessie Afronden & Oefencertificaat")
    st.markdown("Download hier het officiële PDF-certificaat van je oefensessie om in te dienen bij je leerkracht Latijn.")

    st.success(f"⏱️ **Oefentijd in deze sessie**: {elapsed_minutes} minuten")
    st.info(f"📊 **Behaalde score**: {st.session_state.score} op {st.session_state.total} vragen ({round((st.session_state.score/st.session_state.total)*100) if st.session_state.total > 0 else 0}%)")

    if elapsed_minutes >= 10:
        st.balloons()
        st.success("🌟 **Proficiat! Je hebt de aanbevolen oefentijd van 10 minuten bereikt!**")
    else:
        st.warning(f"💡 Je hebt nu {elapsed_minutes} minuten geoefend. Probeer minstens 10 minuten te halen voor het beste resultaat!")

    st.subheader("Vul je gegevens in voor het certificaat:")
    c_name = st.text_input("Naam & Voornaam:", value=student_name)
    c_class = st.text_input("Klasgroep:", value=student_class)

    if st.button("🎓 Genereer PDF Certificaat"):
        if not c_name:
            st.error("Vul je naam in voor het certificaat.")
        else:
            pdf_bytes = generate_pdf_certificate(
                student_name=c_name,
                student_class=c_class,
                score=st.session_state.score,
                total=st.session_state.total,
                tekst_num=max_tekst,
                elapsed_minutes=elapsed_minutes
            )

            st.download_button(
                label="📥 Download PDF Certificaat",
                data=pdf_bytes,
                file_name=f"Statio_Latijn_Certificaat_{c_name.replace(' ', '_')}.pdf",
                mime="application/pdf"
            )
            st.success("Het PDF-certificaat is gereed! Klik op de knop hierboven om het te bewaren.")

st.markdown("---")
st.caption("Statio Latijn Trainer v2.0 | Ontwikkeld voor Latijn Eerste Graad | Gebaseerd op Statio I-VIII Vocabula & Grammatica")
