"""
Chunk events for RAG

Input:
    data/processed/documents.json

Output:
    data/processed/chunks.json

Strategy:
    chunk_size = 500 chars
    overlap = 50 chars

Ready for:
    embeddings
    FAISS
"""

import json
from pathlib import Path


# =========================
# CONFIG
# =========================

INPUT_FILE = Path(
    "data/processed/documents.json"
)

OUTPUT_FILE = Path(
    "data/processed/chunks.json"
)


CHUNK_SIZE = 500
OVERLAP = 50



# =========================
# CHUNK TEXT
# =========================

def split_text(
    text,
    chunk_size=CHUNK_SIZE,
    overlap=OVERLAP
):

    chunks = []

    start = 0
    length = len(text)


    while start < length:

        end = start + chunk_size

        chunk = text[start:end].strip()


        # ignore les micro morceaux
        if len(chunk) >= 50:
            chunks.append(chunk)


        start = end - overlap


    return chunks


# =========================
# BUILD CHUNKS
# =========================

def build_chunks():


    with open(
        INPUT_FILE,
        encoding="utf-8"
    ) as f:

        documents = json.load(f)



    chunks = []



    for doc in documents:


        text = doc["page_content"]


        metadata = doc["metadata"]


        event_id = doc["id"]



        text_chunks = split_text(text)



        for index, chunk in enumerate(text_chunks):


            chunks.append(

                {

                    "chunk_id":
                        f"{event_id}_{index}",


                    "page_content":
                        chunk,


                    "metadata":
                    {

                        **metadata,

                        "event_id":
                            event_id,


                        "chunk_index":
                            index,


                        "total_chunks":
                            len(text_chunks)

                    }

                }

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
            chunks,
            f,
            ensure_ascii=False,
            indent=2
        )



    print("===================")

    print(
        "DOCUMENTS:",
        len(documents)
    )

    print(
        "CHUNKS:",
        len(chunks)
    )

    print(
        "AVG CHUNK SIZE:",
        sum(
            len(c["page_content"])
            for c in chunks
        )
        //
        len(chunks)
    )

    print(
        "SAVED:",
        OUTPUT_FILE
    )

    print("===================")




if __name__ == "__main__":

    build_chunks()
