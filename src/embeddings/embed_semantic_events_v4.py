import json
from pathlib import Path

from sentence_transformers import SentenceTransformer


INPUT="data/processed/semantic_chunks.json"
OUTPUT="data/processed/semantic_embeddings.json"


MODEL_NAME="sentence-transformers/paraphrase-multilingual-mpnet-base-v2"


def main():

    print("Loading model...")

    model=SentenceTransformer(MODEL_NAME)


    chunks=json.load(
        open(INPUT,encoding="utf-8")
    )


    texts=[
        c["text"]
        for c in chunks
    ]


    vectors=model.encode(
        texts,
        normalize_embeddings=True,
        show_progress_bar=True
    )


    result=[]

    for chunk,vector in zip(chunks,vectors):

        result.append({

            "chunk_id":chunk["chunk_id"],

            "text":chunk["text"],

            "metadata":chunk["metadata"],

            "embedding":vector.tolist()

        })


    json.dump(
        result,
        open(OUTPUT,"w",encoding="utf-8"),
        ensure_ascii=False
    )


    print("===================")
    print("CHUNKS:",len(result))
    print("DIMENSION:",len(result[0]["embedding"]))
    print("SAVED:",OUTPUT)
    print("===================")



if __name__=="__main__":
    main()
