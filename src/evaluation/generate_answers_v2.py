"""
Génération automatique des réponses du chatbot RAG
pour le jeu de test annoté.

Usage :

PYTHONPATH=. python src/evaluation/generate_answers_v2.py
"""

import json
import subprocess
import os


QUESTIONS_FILE = (
    "data/test_dataset/questions.json"
)

OUTPUT_FILE = (
    "data/test_dataset/generated_answers.json"
)


def clean_answer(output):
    """
    Garde uniquement la réponse générée
    après le bloc ANSWER.
    """

    if "===================" in output:

        parts = output.split(
            "==================="
        )

        # ask_rag affiche :
        # QUESTION
        # ...
        # ANSWER
        # ...
        #
        # on récupère la dernière partie

        answer = parts[-1].strip()

        return answer

    return output.strip()



def main():

    with open(
        QUESTIONS_FILE,
        encoding="utf-8"
    ) as f:

        questions = json.load(f)


    results = []


    env = os.environ.copy()
    env["PYTHONPATH"] = "."


    for item in questions:

        question = item["question"]


        print()
        print("=" * 60)
        print(question)
        print("=" * 60)


        result = subprocess.run(
            [
                "python",
                "src/rag/ask_rag.py",
                question
            ],
            capture_output=True,
            text=True,
            env=env
        )


        answer = clean_answer(
            result.stdout
        )


        results.append(
            {
                "id": item["id"],
                "question": question,
                "answer": answer,
                "returncode": result.returncode
            }
        )


        print(
            "RETURN CODE:",
            result.returncode
        )


    with open(
        OUTPUT_FILE,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            results,
            f,
            ensure_ascii=False,
            indent=2
        )


    print()
    print("===================")
    print("Saved:")
    print(OUTPUT_FILE)
    print("===================")



if __name__ == "__main__":

    main()
