import requests
import json
from pathlib import Path
from datetime import datetime, timedelta, timezone
from collections import Counter


# =========================
# CONFIG
# =========================

API_KEY = "oa_pk_SMOBRlCiEhQcgohvLtbvuakEtxkoopLotSpzTWBIHsboNXMSSLbDdmydSvGcRFAv"

AGENDAS_URL = "https://api.openagenda.com/v2/agendas"
EVENTS_URL = "https://api.openagenda.com/v2/agendas/{uid}/events"


OUTPUT_FILE = Path(
    "data/raw/ingestion_events.json"
)


LIMIT = 100


NOW = datetime.now(timezone.utc)

ONE_YEAR_AGO = NOW - timedelta(days=365)

# =========================
# ZONE CIBLE
# =========================

TARGET_DEPARTMENTS = [

    # Paris
    "paris",
    "75",

    # Ile de France
    "hauts-de-seine",
    "seine-saint-denis",
    "val-de-marne",
    "val-d'oise",
    "essonne",
    "yvelines",
    "seine-et-marne"

]


TARGET_CITIES = [

    "paris",
    "versailles",
    "boulogne",
    "montreuil",
    "saint-denis",
    "créteil",
    "nanterre",
    "evry",
    "melun",
    "cergy"

]


# =========================
# FETCH AGENDAS
# =========================

def fetch_agendas():


    params = {

        "limit": 100

    }


    r = requests.get(

        AGENDAS_URL,

        headers={
            "key": API_KEY
        },

        params=params,

        timeout=30
    )


    if r.status_code != 200:

        print(r.text)

        return []


    return r.json().get(
        "agendas",
        []
    )



# =========================
# FETCH EVENTS
# =========================


def fetch_events(uid):


    events=[]

    offset=0


    while True:


        r = requests.get(

            EVENTS_URL.format(uid=uid),

            headers={
                "key": API_KEY
            },

            params={

                "limit":LIMIT,
                "offset":offset,
                "detailed":1

            },

            timeout=30

        )


        if r.status_code != 200:
            break



        batch = r.json().get(
            "events",
            []
        )


        if not batch:
            break



        events.extend(batch)

        offset += LIMIT



    return events




# =========================
# DATE
# =========================


def extract_date(event):


    candidates = [

        event.get("firstTiming"),
        event.get("firstDate"),
        event.get("dateRange")

    ]


    for c in candidates:


        if isinstance(c,dict):


            for k in [

                "begin",
                "start",
                "date",
                "value"

            ]:

                if isinstance(c.get(k),str):

                    return c[k]



    return None




# =========================
# URL
# =========================


def extract_url(event):


    links = event.get("links")


    if isinstance(links,dict):

        if links.get("self"):

            return links["self"]



    return (

        event.get("onlineAccessLink")
        or event.get("canonicalUrl")

    )

# =========================
# NORMALIZE
# =========================

def get_fr(value):

    if isinstance(value, dict):
        return value.get("fr", "")

    return value or ""


def normalize(event):

    location = event.get("location") or {}


    title = get_fr(
        event.get("title")
    )

    description = get_fr(
        event.get("description")
    )

    long_description = get_fr(
        event.get("longDescription")
    )

    motive = get_fr(
        event.get("motive")
    )


    keywords = event.get("keywords", {})

    if isinstance(keywords, dict):
        keywords = keywords.get("fr", [])

    if not isinstance(keywords, list):
        keywords = []

    # nettoyage keywords OpenAgenda
    keywords = [
        k for k in keywords
        if isinstance(k, str)
    ]

    return {

        "id":
            event.get("uid"),


        "title":
            title,


        "description":
            description,


        "longDescription":
            long_description,


        "motive":
            motive,

        
        "search_text":
        (
            "Titre: "
            + title
            + "\n"
            + "Description: "
            + description
            + "\n"
            + "Contenu: "
            + long_description
            + "\n"
            + "Type: "
            + " "
            + "\n"
            + "Mots clés: "
            + " ".join(keywords)
        ),        

        "city":
            location.get("city"),


        "department":
            location.get("department"),


        "keywords":
            keywords,


        "start_date":
            extract_date(event),


        "url":
            extract_url(event)

    }


# =========================
# TYPE EVENT
# =========================

def detect_event_type(event):

    title = event.get("title","")
    desc = event.get("description","")
    long_desc = event.get("longDescription","")
    keywords = event.get("keywords",[])
    motive = event.get("motive","")


    if isinstance(title,dict):
        title = title.get("fr","")

    if isinstance(desc,dict):
        desc = desc.get("fr","")

    if isinstance(long_desc,dict):
        long_desc = long_desc.get("fr","")


    if isinstance(keywords,dict):
        keywords = keywords.get("fr",[])


    if not isinstance(keywords,list):
        keywords=[]


    text = (
        str(title)
        + " "
        + str(desc)
        + " "
        + str(long_desc)
        + " "
        + str(motive)
        + " "
        + " ".join(keywords)
    ).lower()

    categories = {


    "culture": [

        "concert",
        "musique",
        "festival",
        "spectacle",
        "théâtre",
        "cinéma",
        "projection",
        "exposition",
        "art",
        "danse",
        "lecture",
        "littérature",
        "poésie",
        "conte",
        "contes",
        "livre",
        "bibliothèque",
        "kamishibai",
        "vernissage",
        "représentation",
        "scène"

    ],



    "patrimoine": [

        "patrimoine",
        "musée",
        "monument",
        "histoire",
        "archive",
        "château",
        "demeure",
        "site historique",
        "jardin",
        "visite guidée"

    ],



    "loisir": [

        "atelier",
        "animation",
        "activité",
        "découverte",
        "sortie",
        "jeu",
        "loisir",
        "balade",
        "parcours",
        "expérience",
        "initiation",
        "démonstration",
        "création",
        "créatif",
        "pratique",
        "cuisine",
        "éveil"

    ],



    "famille": [

        "famille",
        "enfant",
        "parent",
        "parents",
        "petite enfance",
        "bébé",
        "jeunesse",
        "jeune public",
        "ado",
        "en bas âge"

    ],



    "sport": [

        "sport",
        "course",
        "trail",
        "randonnée",
        "vélo",
        "football",
        "basket",
        "compétition",
        "tournoi"

    ],



    "professionnel": [

        "emploi",
        "recrutement",
        "entreprise",
        "entrepreneuriat",
        "entrepreneur",
        "startup",
        "incubateur",
        "innovation",
        "réseau",
        "forum",
        "salon professionnel",
        "job dating"

    ],



    "education": [

        "formation",
        "cours",
        "université",
        "recherche",
        "conférence",
        "colloque",
        "masterclass",
        "orientation"

    ],



    "vie_locale": [

        "marché",
        "foire",
        "brocante",
        "rencontre",
        "portes ouvertes",
        "association",
        "mairie",
        "quartier",
        "citoyen",
        "inauguration",
        "cérémonie",
        "commémoration"

    ]

}


    scores = {}


    for category, words in categories.items():

        score = sum(
            1
            for w in words
            if w in text
        )

        if score:
            scores[category]=score



    if scores:

        return max(
            scores,
            key=scores.get
        )

    
    if any(x in text for x in [
        "baba",
        "sorcière",
        "racontines",
        "histoire",
        "histoires",
        "chaussures",
        "équilibre",
        "snoezelen"
    ]):
        return "famille"

    return "autre"

# =========================
# VALIDATION
# =========================


def is_valid(e):


    return (

        e["id"]
        and e["title"]
        and e["start_date"]

    )




# =========================
# DATE FILTER
# =========================


def is_recent(e):


    try:

        d=datetime.fromisoformat(
            e["start_date"]
            .replace("Z","+00:00")
        )


        return d >= ONE_YEAR_AGO


    except:

        return False




# =========================
# GEO FILTER
# =========================


def is_target_zone(e):


    dept = (

        e.get("department")
        or ""

    ).lower()



    city = (

        e.get("city")
        or ""

    ).lower()



    return (

        dept in TARGET_DEPARTMENTS

        or

        city in TARGET_CITIES

    )




# =========================
# PIPELINE
# =========================


def run():


    print("FETCH AGENDAS")


    agendas = fetch_agendas()


    print(
        "AGENDAS:",
        len(agendas)
    )


    raw=[]


    for a in agendas:


        uid=a.get("uid")


        if uid:

            raw.extend(
                fetch_events(uid)
            )


    print(
        "RAW:",
        len(raw)
    )



    normalized=[

        normalize(e)

        for e in raw

    ]



    recent=[

        e for e in normalized

        if is_valid(e)
        and is_recent(e)

    ]



    print(
        "RECENT:",
        len(recent)
    )



    final=[

        e for e in recent

        if is_target_zone(e)

    ]



    for e in final:

        e["type"]=detect_event_type(e)

# =========================
# CONTROLES QUALITE AVANT CLEAN
# =========================

# doublons ID

    ids = [
        e["id"]
        for e in final
    ]


    print(
        "DUPLICATES:",
        len(ids) - len(set(ids))
    )



# textes trop courts

    short_text = [

        e for e in final

        if len(
            e.get("search_text","")
        ) < 100

    ]


    print(
        "SHORT TEXT:",
        len(short_text)
    )

    print(
        "FINAL:",
        len(final)
    )



    print(
        Counter(
            e["department"]
            for e in final
        )
    )



    print(
        Counter(
            e["type"]
            for e in final
        )
    )

    print(
        Counter(
            e["type"]
            for e in final
        )
    )


# =========================
# DEBUG AUTRE
# =========================

    print("\nEXEMPLES AUTRE:")

    count = 0

    for e in final:

        if e["type"] == "autre":

            print("\n---")
            print("TITLE:", e["title"])
            print("KEYWORDS:", e["keywords"])
            print("CITY:", e["city"])

            count += 1

            if count == 10:
                break

    OUTPUT_FILE.parent.mkdir(

        parents=True,

        exist_ok=True

    )


    with open(

        OUTPUT_FILE,

        "w",

        encoding="utf-8"

    ) as f:


        json.dump(

            final,

            f,

            ensure_ascii=False,

            indent=2

        )


    print(
        "Saved:",
        OUTPUT_FILE
    )



if __name__=="__main__":

    run()
