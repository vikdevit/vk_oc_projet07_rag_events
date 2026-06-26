import json
import faiss
import numpy as np

from sentence_transformers import SentenceTransformer

import json

with open(
    "data/processed/semantic_chunks.json",
    encoding="utf-8"
) as f:
    chunks = json.load(f)

INDEX="data/vectorstore/semantic_events.index"

META="data/vectorstore/semantic_events_metadata.json"

MODEL="paraphrase-multilingual-mpnet-base-v2"

TOP_K=5


def search(query):

    index = faiss.read_index(INDEX)

    metadata=json.load(
        open(META,encoding="utf-8")
    )


    model=SentenceTransformer(MODEL)


    vector=model.encode(
        [query],
        convert_to_numpy=True
    )


    vector=vector.astype("float32")

    faiss.normalize_L2(vector)


    scores,ids=index.search(
        vector,
        TOP_K
    )


    print("===================")
    print(query)
    print("===================")


    for score,idx in zip(
        scores[0],
        ids[0]
    ):

        doc=metadata[idx]

        print()
        print("SCORE:",round(float(score),3))
        print("TITLE:",doc["title"])
        print("TYPE:",doc["type"])
        print("CITY:",doc["city"])
        print("DATE:",doc["start_date"])
        #print("DESC:",doc["description"][:200])
        #print(
        #    "DESC:",
        #    chunks[idx]["text"][:300]
        #)

        print(
            "DESC:",
            chunks[idx]["metadata"].get("description") or ""
        )

if __name__=="__main__":

    import sys

    q=" ".join(sys.argv[1:])

    if not q:
        q="activité enfant à Paris"

    search(q)
