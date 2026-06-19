"""
Generate embeddings from chunks.

Input:
    data/processed/chunks.json

Output:
    data/processed/embeddings.json
"""

import json
from pathlib import Path

from sentence_transformers import SentenceTransformer


INPUT_FILE = Path(
    "data/processed/chunks.json"
)

OUTPUT_FILE = Path(
    "data/processed/embeddings.json"
)


MODEL_NAME = (
    "sentence-transformers/"
    "paraphrase-multilingual-MiniLM-L12-v2"
)


def load_chunks():

    with open(
        INPUT_FILE,
        "r",
        encoding="utf-8"
    ) as f:

        return json.load(f)


def build_embeddings(chunks):

    model = SentenceTransformer(
        MODEL_NAME
    )

    embeddings = []

    total = len(chunks)

    for i, chunk in enumerate(chunks, start=1):

        vector = model.encode(
            chunk["page_content"],
            normalize_embeddings=True
        )

        embeddings.append({

            "chunk_id":
                chunk["chunk_id"],

            "embedding":
                vector.tolist(),

            "metadata":
                chunk["metadata"],

            "page_content":
                chunk["page_content"]

        })

        if i % 100 == 0:

            print(
                f"{i}/{total} embeddings generated"
            )

    return embeddings


def save_embeddings(data):

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
            data,
            f,
            ensure_ascii=False
        )


def run():

    chunks = load_chunks()

    embeddings = build_embeddings(
        chunks
    )

    save_embeddings(
        embeddings
    )

    print("===================")
    print(
        f"CHUNKS: {len(chunks)}"
    )
    print(
        f"EMBEDDINGS: {len(embeddings)}"
    )
    print(
        f"SAVED: {OUTPUT_FILE}"
    )
    print("===================")


if __name__ == "__main__":

    run()
