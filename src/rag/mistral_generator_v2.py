"""
Générateur Mistral via API

Pipeline:

retriever
    |
reranker
    |
prompt_builder
    |
Mistral API
"""


import os

from langchain_mistralai import ChatMistralAI
from langchain_core.messages import HumanMessage



MODEL_NAME = "mistral-small-latest"



# =====================
# LOAD LLM
# =====================

def load_llm():

    print("Loading Mistral API...")


    api_key = os.getenv(
        "MISTRAL_API_KEY"
    )


    if not api_key:

        raise ValueError(
            "MISTRAL_API_KEY manquante"
        )


    return ChatMistralAI(
        model=MODEL_NAME,
        temperature=0.2,
        max_tokens=500,
        api_key=api_key
    )



# =====================
# GENERATE
# =====================

def generate_answer(
    query,
    prompt
):


    llm = load_llm()


    response = llm.invoke(
        [
            HumanMessage(
                content=prompt
            )
        ]
    )


    return response.content



# =====================
# TEST PIPELINE COMPLET
# =====================

if __name__ == "__main__":


    from src.rag.retriever_v3 import retrieve
    from src.rag.reranker_v5 import rerank
    from src.rag.prompt_builder_v3 import build_prompt



    query = (
        "activité enfant à Paris"
    )


    print("Retrieving...")


    docs = retrieve(
        query,
        top_k=10
    )


    docs = rerank(
        query,
        docs
    )


    prompt = build_prompt(
        query,
        docs
    )


    print()
    print("===================")
    print("PROMPT")
    print("===================")

    print(prompt)



    print()
    print("===================")
    print("MISTRAL ANSWER")
    print("===================")


    answer = generate_answer(
        query,
        prompt
    )


    print(answer)
