from src.rag.reranker_v5 import rerank
from src.rag.retriever_v3 import retrieve


def test_reranker_returns_sorted_results():

    query = "activité enfant Paris"


    docs = retrieve(
        query,
        top_k=5
    )


    ranked = rerank(
        query,
        docs
    )


    assert len(ranked) > 0


    assert (
        ranked[0]
        is not None
    )
