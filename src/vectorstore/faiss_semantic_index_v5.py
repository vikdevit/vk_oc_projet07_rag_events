import json
from pathlib import Path

import faiss
import numpy as np


INPUT = Path(
    "data/processed/semantic_embeddings.json"
)

INDEX = Path(
    "data/vectorstore/semantic_events.index"
)

META = Path(
    "data/vectorstore/semantic_events_metadata.json"
)


def build():

    with open(
        INPUT,
        encoding="utf-8"
    ) as f:
        data = json.load(f)


    vectors = np.array(
        [
            x["embedding"]
            for x in data
        ],
        dtype="float32"
    )


    # cosine similarity
    faiss.normalize_L2(vectors)


    dim = vectors.shape[1]


    index = faiss.IndexFlatIP(dim)

    index.add(vectors)


    INDEX.parent.mkdir(
        exist_ok=True
    )


    faiss.write_index(
        index,
        str(INDEX)
    )


    metadata = []

    for x in data:

        metadata.append(
            {
                "chunk_id": x["chunk_id"],

                "title":
                    x["metadata"].get("title"),

                "type":
                    x["metadata"].get("type"),

                "city":
                    x["metadata"].get("city"),

                "department":
                    x["metadata"].get("department"),

                "start_date":
                    x["metadata"].get("start_date"),

                "description":
                    x["metadata"].get("description"),

                "page_content":
                    x["text"]
            }
        )


    with open(
        META,
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
    print("VECTORS:", index.ntotal)
    print("DIMENSION:", dim)
    print("INDEX:", INDEX)
    print("META:", META)
    print("===================")



if __name__ == "__main__":
    build()
