from src.rag.rag_chain_v3 import rag_answer



def test_unknown_domain_question():


    answer = rag_answer(
        "vol spatial sur Mars"
    )


    answer = answer.lower()


    assert (
        "sais pas" in answer
        or
        "aucun" in answer
        or
        "pas d'information" in answer
    )
