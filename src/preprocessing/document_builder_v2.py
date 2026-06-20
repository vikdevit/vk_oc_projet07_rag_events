"""
Document builder
================

Transforme les événements nettoyés en documents RAG.

Input:
    data/processed/clean_events.json

Output:
    data/processed/documents.json

Format:
[
 {
   "id": "...",
   "page_content": "...",
   "metadata": {...}
 }
]

Préparation:
- chunking
- embeddings
- FAISS
"""


import json
from pathlib import Path



# =========================
# CONFIG
# =========================

INPUT_FILE = Path(
    "data/processed/clean_events.json"
)


OUTPUT_FILE = Path(
    "data/processed/documents.json"
)



# =========================
# BUILD CONTENT
# =========================

def build_content(event):
    """
    Construit le texte utilisé par le moteur RAG.
    """

    metadata = event.get(
        "metadata",
        {}
    )


    title = metadata.get(
        "title",
        ""
    )

    city = metadata.get(
        "city",
        ""
    )

    department = metadata.get(
        "department",
        ""
    )

    event_type = metadata.get(
        "type",
        ""
    )

    date = metadata.get(
        "start_date",
        ""
    )

    url = metadata.get(
        "url"
    )


    text = event.get(
        "text",
        ""
    )


    parts = [

        f"Titre: {title}",

        f"Type: {event_type}",

        f"Lieu:\n{city}\n{department}",

        f"Date:\n{date}",

        f"Description:\n{text}"

    ]


    # ajoute le lien seulement s'il existe
    if url:

        parts.append(
            f"Lien:\n{url}"
        )


    return "\n\n".join(parts)



# =========================
# METADATA FOR FAISS
# =========================

def build_metadata(event):
    """
    Métadonnées conservées pour FAISS.
    """

    metadata = event.get(
        "metadata",
        {}
    )


    return {

        "event_id":
            event.get("id"),


        "title":
            metadata.get("title"),


        "city":
            metadata.get("city"),


        "department":
            metadata.get("department"),


        "type":
            metadata.get("type"),


        "start_date":
            metadata.get("start_date"),


        "url":
            metadata.get("url"),


        "keywords":
            metadata.get("keywords", [])

    }



# =========================
# BUILD DOCUMENTS
# =========================

def build_documents():


    with open(
        INPUT_FILE,
        "r",
        encoding="utf-8"
    ) as f:

        events = json.load(f)



    documents = []



    for event in events:


        document = {


            "id":
                str(event.get("id")),


            "page_content":
                build_content(event),


            "metadata":
                build_metadata(event)

        }


        documents.append(
            document
        )



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
            documents,
            f,
            ensure_ascii=False,
            indent=2
        )



    print("===================")

    print(
        f"INPUT DOCUMENTS: {len(events)}"
    )

    print(
        f"OUTPUT DOCUMENTS: {len(documents)}"
    )

    print(
        f"SAVED: {OUTPUT_FILE}"
    )

    print("===================")



if __name__ == "__main__":

    build_documents()
