
"""
RAG Chain orchestration

question
   |
retriever
   |
reranker
   |
prompt_builder
   |
Mistral
   |
answer
"""


from src.rag.retriever_v3 import retrieve
from src.rag.reranker_v5 import rerank
from src.rag.prompt_builder_v3 import build_prompt
from src.rag.mistral_generator_v2 import generate_answer



TOP_K_RETRIEVE = 10



def rag_answer(
    question
):


    # 1) semantic retrieval

    docs = retrieve(
        question,
        top_k=TOP_K_RETRIEVE
    )


    # 2) reranking

    docs = rerank(
        question,
        docs
    )


    # 3) prompt construction

    prompt = build_prompt(
        question,
        docs
    )


    # 4) generation

    answer = generate_answer(
        question,
        prompt
    )


    return answer



if __name__ == "__main__":


    question = (
        "activité enfant à Paris"
    )


    print("===================")
    print("QUESTION")
    print("===================")

    print(question)


    answer = rag_answer(
        question
    )


    print()
    print("===================")
    print("ANSWER")
    print("===================")

    print(answer)
