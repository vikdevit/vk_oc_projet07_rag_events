import sys
import json
import faiss
import numpy as np

from sentence_transformers import SentenceTransformer



MODEL="sentence-transformers/paraphrase-multilingual-mpnet-base-v2"


INDEX="data/vectorstore/semantic_events.index"
META="data/vectorstore/semantic_events_metadata.json"



def search(query,k=5):

    model=SentenceTransformer(MODEL)

    q=model.encode(
        [query],
        normalize_embeddings=True
    )


    index=faiss.read_index(INDEX)


    scores,ids=index.search(
        np.array(q,dtype="float32"),
        k
    )


    metadata=json.load(
        open(META,encoding="utf-8")
    )


    results=[]


    for score,i in zip(scores[0],ids[0]):

        item=metadata[i]

        results.append(
            {
            "score":float(score),
            **item
            }
        )


    return results



if __name__=="__main__":

    query=" ".join(sys.argv[1:])


    print("===================")
    print("QUERY:",query)
    print("===================")


    results=search(query)


    # filtre simple ville
    if "Paris" in query:

        results=[
            r for r in results
            if r["metadata"]["city"]=="Paris"
        ]


    for r in results:

        print()
        print("SCORE:",round(r["score"],3))
        print("TITLE:",r["metadata"]["title"])
        print("TYPE:",r["metadata"]["type"])
        print("CITY:",r["metadata"]["city"])
        print(r["text"][:300])
