import json
import faiss
import numpy as np


INPUT="data/processed/semantic_embeddings.json"

INDEX="data/vectorstore/semantic_events.index"

META="data/vectorstore/semantic_events_metadata.json"



data=json.load(
    open(INPUT,encoding="utf-8")
)


vectors=np.array(
    [
        x["embedding"]
        for x in data
    ],
    dtype="float32"
)


dim=vectors.shape[1]


index=faiss.IndexFlatIP(dim)

index.add(vectors)


faiss.write_index(
    index,
    INDEX
)


metadata=[
    {
        "chunk_id":x["chunk_id"],
        "text":x["text"],
        "metadata":x["metadata"]
    }
    for x in data
]


json.dump(
    metadata,
    open(META,"w",encoding="utf-8"),
    ensure_ascii=False
)


print("===================")
print("VECTORS:",index.ntotal)
print("DIMENSION:",dim)
print("INDEX:",INDEX)
print("METADATA:",META)
print("===================")
