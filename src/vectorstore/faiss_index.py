"""
FAISS index builder

Input:
    data/processed/embeddings.json

Output:
    data/vectorstore/events.index
    data/vectorstore/events_metadata.json

Build an approximate semantic search database.
"""


import json
from pathlib import Path

import faiss
import numpy as np



# ======================
# CONFIG
# ======================

INPUT_FILE = Path(
    "data/processed/embeddings.json"
)


INDEX_FILE = Path(
    "data/vectorstore/events.index"
)


METADATA_FILE = Path(
    "data/vectorstore/events_metadata.json"
)



# ======================
# LOAD EMBEDDINGS
# ======================

def load_embeddings():

    with open(
        INPUT_FILE,
        encoding="utf-8"
    ) as f:

        data = json.load(f)


    vectors = np.array(
        [
            item["embedding"]
            for item in data
        ],
        dtype="float32"
    )


    metadata = [
        {
            "chunk_id":
                item["chunk_id"],

            **item["metadata"]
        }

        for item in data
    ]


    return vectors, metadata



# ======================
# BUILD INDEX
# ======================

def build_index():


    vectors, metadata = load_embeddings()


    # dimension du vecteur
    dimension = vectors.shape[1]


    # normalisation pour cosine similarity
    faiss.normalize_L2(
        vectors
    )


    # Index basé sur similarité cosinus
    index = faiss.IndexFlatIP(
        dimension
    )


    index.add(
        vectors
    )


    INDEX_FILE.parent.mkdir(
        parents=True,
        exist_ok=True
    )


    faiss.write_index(
        index,
        str(INDEX_FILE)
    )


    with open(
        METADATA_FILE,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            metadata,
            f,
            ensure_ascii=False,
            indent=2
        )


    print("===================")

    print(
        "VECTORS:",
        index.ntotal
    )

    print(
        "DIMENSION:",
        dimension
    )

    print(
        "INDEX:",
        INDEX_FILE
    )

    print(
        "METADATA:",
        METADATA_FILE
    )

    print("===================")



if __name__ == "__main__":

    build_index()
