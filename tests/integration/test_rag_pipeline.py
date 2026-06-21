from src.rag.rag_chain_v3 import rag_answer



def test_complete_rag_pipeline():


    question = (
        "activité famille "
        "en Île-de-France"
    )


    answer = rag_answer(
        question
    )


    assert answer is not None


    assert len(answer) > 50


    assert (
        "famille"
        in answer.lower()
        or
        "activité"
        in answer.lower()
    )
