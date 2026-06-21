"""
Interface utilisateur RAG

Usage:
PYTHONPATH=. python src/rag/ask_rag.py "activité enfant à Paris"
"""


import sys

from src.rag.rag_chain_v3 import rag_answer



def main():

    query = " ".join(
        sys.argv[1:]
    )


    if not query:

        query = (
            "activité enfant à Paris"
        )


    print("===================")
    print("QUESTION")
    print("===================")

    print(query)


    answer = rag_answer(
        query
    )


    print()
    print("===================")
    print("ANSWER")
    print("===================")

    print(answer)



if __name__ == "__main__":

    main()
