"""
Retriever RAG semantic uniquement
"""

import json
from pathlib import Path

import faiss
import numpy as np
from sentence_transformers import SentenceTransformer


# =========================
# CONFIG
# =========================

INDEX_FILE = Path(
    "data/vectorstore/semantic_events.index"
)

METADATA_FILE = Path(
    "data/vectorstore/semantic_events_metadata.json"
)


MODEL_NAME = (
    "sentence-transformers/"
    "paraphrase-multilingual-mpnet-base-v2"
)


TOP_K = 5


# =========================
# LOAD
# =========================

print("Loading semantic model...")

model = SentenceTransformer(
    MODEL_NAME
)


def load_store():

    index = faiss.read_index(
        str(INDEX_FILE)
    )

    with open(
        METADATA_FILE,
        encoding="utf-8"
    ) as f:

        metadata = json.load(f)

    return index, metadata



# =========================
# RETRIEVE
# =========================

def retrieve(
    query,
    top_k=TOP_K
):

    index, metadata = load_store()


    embedding = model.encode(
        [query],
        convert_to_numpy=True
    )


    embedding = np.array(
        embedding,
        dtype="float32"
    )


    # cosine similarity
    faiss.normalize_L2(
        embedding
    )


    scores, ids = index.search(
        embedding,
        top_k
    )


    results = []


    for score, idx in zip(
        scores[0],
        ids[0]
    ):

        if idx == -1:
            continue


        doc = metadata[idx]


        results.append(
            {
                "title":
                    doc.get("title"),

                "type":
                    doc.get("type"),

                "city":
                    doc.get("city"),

                "department":
                    doc.get("department"),

                "start_date":
                    doc.get("start_date"),

                "description":
                    doc.get("description"),

                "page_content":
                    doc.get("page_content"),

                "score":
                    float(score)
            }
        )


    return results



# =========================
# TEST
# =========================

if __name__ == "__main__":

    query = "activité enfant à Paris"


    docs = retrieve(
        query,
        top_k=5
    )


    print("===================")
    print("QUERY:", query)
    print("===================")


    for i, doc in enumerate(docs):

        print()
        print("RESULT:", i+1)

        print(
            "TITLE:",
            doc["title"]
        )

        print(
            "TYPE:",
            doc["type"]
        )

        print(
            "CITY:",
            doc["city"]
        )

        print(
            "DATE:",
            doc["start_date"]
        )

        print(
            "DESCRIPTION:",
            doc["description"][:200]
        )

        print(
            "SCORE:",
            round(doc["score"],3)
        )
