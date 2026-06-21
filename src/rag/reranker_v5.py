"""
Reranker RAG semantic

Pipeline:
retriever semantic FAISS
        |
        v
reranker CrossEncoder
        |
        v
top documents
"""


from sentence_transformers import CrossEncoder

from src.rag.retriever_v3 import retrieve



# =====================
# CONFIG
# =====================

RERANKER_MODEL = (
    "cross-encoder/"
    "ms-marco-MiniLM-L-6-v2"
)


TOP_K_RETRIEVE = 10
TOP_K_FINAL = 5



# =====================
# LOAD MODEL
# =====================

print("Loading reranker model...")


reranker = CrossEncoder(
    RERANKER_MODEL
)



# =====================
# RERANK
# =====================

def rerank(
    query,
    docs
):

    pairs = []


    for doc in docs:

        text = (
            doc.get("page_content")
            or doc.get("description")
            or ""
        )


        pairs.append(
            [
                query,
                text
            ]
        )


    scores = reranker.predict(
        pairs
    )


    for doc, score in zip(
        docs,
        scores
    ):

        # ajout score reranker
        doc["rerank_score"] = float(score)



    docs = sorted(
        docs,
        key=lambda x: x["rerank_score"],
        reverse=True
    )


    return docs[:TOP_K_FINAL]



# =====================
# TEST
# =====================

if __name__ == "__main__":


    query = (
        "activité enfant à Paris"
    )


    print("Loading retriever...")


    docs = retrieve(
        query,
        top_k=TOP_K_RETRIEVE
    )


    print()
    print("===================")
    print("BEFORE RERANK")
    print("===================")


    for d in docs:

        print(
            d.get("title"),
            "|",
            d.get("city"),
            "|",
            d.get("start_date")
        )



    results = rerank(
        query,
        docs
    )


    print()
    print("===================")
    print("AFTER RERANK")
    print("===================")



    for d in results:

        print()

        print(
            "TITLE:",
            d.get("title")
        )

        print(
            "TYPE:",
            d.get("type")
        )

        print(
            "CITY:",
            d.get("city")
        )

        print(
            "DATE:",
            d.get("start_date")
        )


        print(
            "DESCRIPTION:",
            (
                d.get("description")
                or ""
            )[:200]
        )


        print(
            "FAISS:",
            round(
                d.get("score",0),
                3
            ),
            "RERANK:",
            round(
                d["rerank_score"],
                3
            )
        )
