import json
import re
from pathlib import Path
from collections import Counter


# =========================
# CONFIG
# =========================

INPUT_FILE = Path(
    "data/raw/ingestion_events.json"
)


OUTPUT_FILE = Path(
    "data/processed/clean_events.json"
)


MIN_TEXT_LENGTH = 100



# =========================
# TEXT CLEANING
# =========================

def clean_text(text):

    if not text:
        return ""

    text = str(text)


    # suppression markdown links
    text = re.sub(
        r"\[([^\]]+)\]\([^)]+\)",
        r"\1",
        text
    )


    # suppression caractères inutiles
    text = text.replace(
        "\\n",
        " "
    )


    text = re.sub(
        r"\s+",
        " ",
        text
    )


    return text.strip()



# =========================
# BUILD RAG TEXT
# =========================

def build_rag_text(event):

    """
    Construction du texte utilisé
    pour embeddings + FAISS.

    IMPORTANT:
    On ne prend pas search_text
    car il contient déjà title,
    description et contenu.
    """

    parts = [

        event.get("title"),

        event.get("description"),

        event.get("longDescription"),

        event.get("motive")

    ]


    return clean_text(

        " ".join(
            p
            for p in parts
            if p
        )

    )



# =========================
# CLEAN ONE EVENT
# =========================

def clean_event(event):


    if not event.get("id"):
        return None



    title = clean_text(
        event.get("title")
    )


    if not title:
        return None



    text = build_rag_text(event)



    if len(text) < MIN_TEXT_LENGTH:
        return None



    return {


        "id":
            event["id"],



        "text":
            text,



        "metadata":
        {

            "title":
                title,


            "city":
                event.get("city") or "unknown",


            "department":
                event.get("department") or "unknown",


            "type":
                event.get("type"),


            "start_date":
                event.get("start_date"),


            "keywords":
                event.get("keywords", []),


            "url":
                event.get("url")

        }

    }



# =========================
# PIPELINE
# =========================

def run():


    with open(
        INPUT_FILE,
        encoding="utf-8"
    ) as f:

        events = json.load(f)



    cleaned=[]

    seen=set()



    duplicate=0



    for event in events:


        event_id = event.get("id")



        if event_id in seen:

            duplicate += 1

            continue



        seen.add(event_id)



        result = clean_event(event)



        if result:

            cleaned.append(result)




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

            cleaned,

            f,

            ensure_ascii=False,

            indent=2

        )



    # =====================
    # QUALITY REPORT
    # =====================


    short = [

        e for e in cleaned

        if len(e["text"]) < MIN_TEXT_LENGTH

    ]


    print("===================")

    print(
        "INPUT:",
        len(events)
    )

    print(
        "DUPLICATES:",
        duplicate
    )

    print(
        "SHORT TEXT:",
        len(short)
    )

    print(
        "CLEAN:",
        len(cleaned)
    )


    print("\nTYPES:")

    print(
        Counter(
            e["metadata"]["type"]
            for e in cleaned
        )
    )


    print("\nDEPARTMENTS:")

    print(
        Counter(
            e["metadata"]["department"]
            for e in cleaned
        )
    )


    print("===================")

    print(
        "Saved:",
        OUTPUT_FILE
    )



if __name__ == "__main__":

    run()
