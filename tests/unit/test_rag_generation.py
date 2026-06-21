import pytest

from src.rag.rag_chain_v3 import rag_answer



def test_generation_returns_answer():

    answer = rag_answer(
        "activité enfant à Paris"
    )


    assert answer is not None

    assert isinstance(
        answer,
        str
    )

    assert len(answer) > 20



def test_generation_no_empty_response():

    answer = rag_answer(
        "événement culturel Paris"
    )


    assert answer.strip() != ""
