import pytest

from src.rag.retriever_v3 import retrieve


def test_retrieve_returns_documents():

    docs = retrieve(
        "activité enfant à Paris",
        top_k=5
    )

    assert docs is not None
    assert len(docs) > 0



def test_retrieve_contains_event_fields():

    docs = retrieve(
        "activité famille",
        top_k=3
    )

    doc = docs[0]

    assert "title" in doc
    assert "city" in doc
    assert "description" in doc
