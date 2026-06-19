"""
FAISS semantic search test

Input:
    query utilisateur

Output:
    top événements similaires
"""


import json
from pathlib import Path

import faiss
from sentence_transformers import SentenceTransformer
import numpy as np



INDEX_FILE = Path(
    "data/vectorstore/events.index"
)


METADATA_FILE = Path(
    "data/vectorstore/events_metadata.json"
)


MODEL_NAME = (
    "paraphrase-multilingual-MiniLM-L12-v2"
)



TOP_K = 5



# =====================
# LOAD
# =====================

def load_index():

    index = faiss.read_index(
        str(INDEX_FILE)
    )


    with open(
        METADATA_FILE,
        encoding="utf-8"
    ) as f:

        metadata = json.load(f)


    return index, metadata



# =====================
# SEARCH
# =====================

def search(query):


    index, metadata = load_index()


    model = SentenceTransformer(
        MODEL_NAME
    )


    vector = model.encode(
        [query],
        convert_to_numpy=True
    )


    vector = vector.astype(
        "float32"
    )


    faiss.normalize_L2(
        vector
    )


    scores, ids = index.search(
        vector,
        TOP_K
    )


    print("===================")
    print(
        "QUERY:",
        query
    )
    print("===================")


    for score, idx in zip(
        scores[0],
        ids[0]
    ):


        item = metadata[idx]


        print(
            "\nSCORE:",
            round(float(score),3)
        )


        print(
            "TITLE:",
            item["title"]
        )


        print(
            "TYPE:",
            item["type"]
        )


        print(
            "CITY:",
            item["city"]
        )


        print(
            "DATE:",
            item["start_date"]
        )


        print(
            "URL:",
            item.get("url")
        )

if __name__ == "__main__":

    import sys


    query = " ".join(sys.argv[1:])


    if not query:
        query = "activité enfant à Paris"


    search(query)
