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

    # markdown links
    text = re.sub(
        r"\[([^\]]+)\]\([^)]+\)",
        r"\1",
        text
    )

    # retour ligne
    text = text.replace(
        "\\n",
        " "
    )

    # espaces multiples
    text = re.sub(
        r"\s+",
        " ",
        text
    )

    return text.strip()



# =========================
# KEYWORDS EXTRACTION
# =========================

def extract_keywords(event):

    keywords = event.get("keywords")


    if isinstance(keywords, list):

        result = []

        for k in keywords:

            if isinstance(k, str):
                result.append(k)

            elif isinstance(k, dict):

                label = (
                    k.get("label")
                    or k.get("name")
                )

                if label:
                    result.append(label)


        return clean_keywords(result)



    tags = event.get("tags")


    if isinstance(tags, list):

        result = []

        for tag in tags:

            if isinstance(tag, str):
                result.append(tag)


            elif isinstance(tag, dict):

                label = (
                    tag.get("label")
                    or tag.get("name")
                )

                if label:
                    result.append(label)


        return clean_keywords(result)



    return []



def clean_keywords(values):

    cleaned=[]

    seen=set()


    for value in values:

        value = clean_text(value).lower()


        if value and value not in seen:

            seen.add(value)
            cleaned.append(value)


    return cleaned



# =========================
# BUILD RAG TEXT
# =========================

def build_rag_text(event):

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

        "id": event["id"],

        "text": text,


        "metadata":
        {

            "title": title,


            "city":
                event.get("city")
                or "unknown",


            "department":
                event.get("department")
                or "unknown",


            "type":
                event.get("type")
                or "unknown",


            "start_date":
                event.get("start_date"),


            "keywords":
                extract_keywords(event),


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

        events=json.load(f)



    cleaned=[]

    seen=set()

    duplicate=0



    for event in events:


        event_id=event.get("id")


        if event_id in seen:

            duplicate += 1
            continue


        seen.add(event_id)



        result=clean_event(event)


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


    print("\nKEYWORDS examples:")

    print(
        [
            e["metadata"]["keywords"]
            for e in cleaned[:5]
        ]
    )


    print("===================")

    print(
        "Saved:",
        OUTPUT_FILE
    )



if __name__ == "__main__":

    run()
