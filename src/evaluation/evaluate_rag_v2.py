"""
Evaluation automatique du RAG

Métriques:
- semantic similarity
- keyword coverage
- event coverage
- city accuracy
- category accuracy
- hallucination rate
- correct/partial/incorrect
- JSON report

Usage:

PYTHONPATH=. python src/evaluation/evaluate_rag_v2.py
"""


import json
import re

from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity



# ==========================
# FILES
# ==========================

GENERATED_FILE = (
    "data/test_dataset/generated_answers.json"
)

EXPECTED_FILE = (
    "data/test_dataset/expected_answers.json"
)

REPORT_FILE = (
    "data/test_dataset/evaluation_report.json"
)



# ==========================
# MODEL
# ==========================

print(
    "Loading evaluation model..."
)


EMBEDDING_MODEL = (
    "sentence-transformers/"
    "paraphrase-multilingual-mpnet-base-v2"
)


model = SentenceTransformer(
    EMBEDDING_MODEL
)



# ==========================
# TEXT CLEAN
# ==========================

def clean(text):

    if isinstance(text, dict):

        text = json.dumps(
            text,
            ensure_ascii=False
        )

    if isinstance(text, list):

        text = " ".join(
            map(str,text)
        )

    text = str(text)

    text = text.lower()

    text = re.sub(
        r"[^a-zàâäéèêëîïôöùûüç0-9 ]",
        " ",
        text
    )

    return text



# ==========================
# SEMANTIC SCORE
# ==========================

def semantic_score(
    generated,
    expected
):

    embeddings = model.encode(
        [
            clean(generated),
            clean(expected)
        ]
    )


    score = cosine_similarity(
        [
            embeddings[0]
        ],
        [
            embeddings[1]
        ]
    )[0][0]


    return float(score)



# ==========================
# COVERAGE
# ==========================

def coverage(
    text,
    items
):

    if not items:

        return 1.0


    text = clean(text)


    found = 0


    for item in items:

        if clean(item) in text:

            found += 1


    return found / len(items)



# ==========================
# HALLUCINATION
# ==========================

def hallucination(
    text,
    forbidden
):

    if not forbidden:

        return 0


    text = clean(text)


    for word in forbidden:

        if clean(word) in text:

            return 1


    return 0



# ==========================
# EVALUATE
# ==========================

def evaluate():


    with open(
        GENERATED_FILE,
        encoding="utf8"
    ) as f:

        generated = json.load(f)



    with open(
        EXPECTED_FILE,
        encoding="utf8"
    ) as f:

        expected = json.load(f)



    results = []


    for g,e in zip(
        generated,
        expected
    ):


        answer = g.get(
            "answer",
            ""
        )


        expected_data = e["expected"]


        # texte humain complet

        expected_text = (
            e.get(
                "expected_answer",
                ""
            )
        )



        sim = semantic_score(
            answer,
            expected_text
        )


        keyword_score = coverage(
            answer,
            expected_data.get(
                "keywords",
                []
            )
        )


        event_score = coverage(
            answer,
            expected_data.get(
                "events",
                []
            )
        )


        city_score = coverage(
            answer,
            expected_data.get(
                "cities",
                []
            )
        )


        category_score = coverage(
            answer,
            expected_data.get(
                "categories",
                []
            )
        )


        halluc = hallucination(
            answer,
            expected_data.get(
                "must_not_contain",
                []
            )
        )



        # score global amélioré

        final = (
            0.45 * sim
            +
            0.25 * keyword_score
            +
            0.20 * event_score
            +
            0.10 * city_score
        )



        if halluc:

            status="incorrect"


        elif final >= 0.70:

            status="correct"


        elif final >= 0.40:

            status="partial"


        else:

            status="incorrect"



        results.append(
            {
                "id":g["id"],

                "question":
                    g["question"],

                "similarity":
                    round(sim,3),

                "keyword_coverage":
                    round(keyword_score,3),

                "event_coverage":
                    round(event_score,3),

                "city_coverage":
                    round(city_score,3),

                "category_coverage":
                    round(category_score,3),

                "hallucination":
                    halluc,

                "final_score":
                    round(final,3),

                "status":
                    status
            }
        )


    return results



# ==========================
# MAIN
# ==========================

if __name__=="__main__":


    results = evaluate()


    print()
    print("===================")
    print("RAG EVALUATION")
    print("===================")



    for r in results:

        print(
            r["id"],
            "|",
            r["status"],
            "| score:",
            r["final_score"],
            "| similarity:",
            r["similarity"],
            "| keyword:",
            r["keyword_coverage"],
            "| event:",
            r["event_coverage"],
            "| city:",
            r["city_coverage"],
            "| category:",
            r["category_coverage"],
            "| halluc:",
            r["hallucination"]
        )


    total = len(results)


    correct = sum(
        1 for r in results
        if r["status"]=="correct"
    )


    partial = sum(
        1 for r in results
        if r["status"]=="partial"
    )


    incorrect = sum(
        1 for r in results
        if r["status"]=="incorrect"
    )



    print()
    print("===================")
    print("SUMMARY")
    print("===================")


    print(
        "Correct:",
        correct,
        "/",
        total
    )

    print(
        "Partial:",
        partial,
        "/",
        total
    )


    print(
        "Incorrect:",
        incorrect,
        "/",
        total
    )


    print(
        "Accuracy:",
        round(correct/total,3)
    )



    with open(
        REPORT_FILE,
        "w",
        encoding="utf8"
    ) as f:


        json.dump(
            results,
            f,
            ensure_ascii=False,
            indent=2
        )


    print()
    print(
        "Report saved:",
        REPORT_FILE
    )
