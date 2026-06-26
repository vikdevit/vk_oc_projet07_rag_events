"""
Evaluation RAG stable
Optimisé:
- réponses courtes
- expected_answer longues
- refus "Je ne sais pas"
- hallucination faible
"""

import json
import re

from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity


GENERATED_FILE = "data/test_dataset/generated_answers.json"
EXPECTED_FILE = "data/test_dataset/expected_answers.json"
REPORT_FILE = "data/test_dataset/evaluation_report.json"


print("Loading evaluation model...")

MODEL = SentenceTransformer(
    "sentence-transformers/paraphrase-multilingual-mpnet-base-v2"
)


def clean(x):

    if x is None:
        return ""

    x=str(x).lower()

    x=re.sub(
        r"[^a-zàâäéèêëîïôöùûüç0-9 ]",
        " ",
        x
    )

    return " ".join(x.split())



def similarity(a,b):

    if not a or not b:
        return 0

    emb=MODEL.encode(
        [
            clean(a),
            clean(b)
        ]
    )

    return float(
        cosine_similarity(
            [emb[0]],
            [emb[1]]
        )[0][0]
    )



def coverage(answer, values):

    if not values:
        return 1

    answer=clean(answer)

    found=0

    for v in values:

        if clean(v) in answer:
            found+=1

    return found/len(values)



def required_score(answer, values):

    if not values:
        return 1

    answer=clean(answer)

    return max(
        [
            1 if clean(v) in answer else 0
            for v in values
        ]
        +
        [0]
    )



def is_refusal(answer):

    a=clean(answer)

    return any(
        x in a
        for x in [
            "je ne sais pas",
            "je ne peux pas",
            "aucune information"
        ]
    )



#def hallucination(answer, forbidden):
#
#    if not forbidden:
#        return 0
#
#    a=clean(answer)
#
#    # refus = pas hallucination
#    if is_refusal(a):
#        return 0
#
#
#    for f in forbidden:
#
#        if clean(f) in a:
#            return 1
#
#
#    return 0

def hallucination(
        text,
        forbidden
):

    if not forbidden:
        return 0

    text = clean(text)

    for word in forbidden:

        w = clean(word)

        # éviter faux positifs courts
        if len(w) < 5:
            continue

        if w in text:
            return 1

    return 0

def evaluate():

    generated=json.load(
        open(
            GENERATED_FILE,
            encoding="utf8"
        )
    )


    expected=json.load(
        open(
            EXPECTED_FILE,
            encoding="utf8"
        )
    )


    results=[]


    for g,e in zip(generated,expected):

        answer=g.get("answer","")

        exp=e["expected"]

        sim=similarity(
            answer,
            e.get("expected_answer","")
        )


        keyword=coverage(
            answer,
            exp.get("keywords",[])
        )

        event=coverage(
            answer,
            exp.get("events",[])
        )

        city=coverage(
            answer,
            exp.get("cities",[])
        )

        category=coverage(
            answer,
            exp.get("categories",[])
        )


        required=required_score(
            answer,
            exp.get("must_contain",[])
        )


        halluc=hallucination(
            answer,
            exp.get("must_not_contain",[])
        )


        # cas refus attendu
        if exp.get("must_contain"):

            score=(
                0.6*required
                +
                0.3*sim
                +
                0.1*(1-halluc)
            )


        else:

            score=(
                0.25*sim
                +
                0.25*keyword
                +
                0.25*event
                +
                0.15*city
                +
                0.10*category
            )


        if halluc:
            status="incorrect"

        elif score>=0.65:
            status="correct"

        elif score>=0.40:
            status="partial"

        else:
            status="incorrect"



        results.append(
            {
            "id":g["id"],
            "score":round(score,3),
            "similarity":round(sim,3),
            "required":round(required,3),
            "hallucination":halluc,
            "status":status
            }
        )


    return results



if __name__=="__main__":


    results=evaluate()


    correct=sum(
        r["status"]=="correct"
        for r in results
    )

    partial=sum(
        r["status"]=="partial"
        for r in results
    )

    incorrect=sum(
        r["status"]=="incorrect"
        for r in results
    )


    print("===================")
    print("RAG EVALUATION")
    print("===================")


    for r in results:
        print(
            r["id"],
            "|",
            r["status"],
            "| score:",
            r["score"],
            "| sim:",
            r["similarity"],
            "| halluc:",
            r["hallucination"]
        )


    print("===================")
    print("SUMMARY")
    print("===================")

    print(
        "Correct:",
        correct,
        "/",
        len(results)
    )

    print(
        "Partial:",
        partial,
        "/",
        len(results)
    )

    print(
        "Incorrect:",
        incorrect,
        "/",
        len(results)
    )

    print(
        "Accuracy:",
        round(correct/len(results),3)
    )


    json.dump(
        results,
        open(
            REPORT_FILE,
            "w",
            encoding="utf8"
        ),
        indent=2,
        ensure_ascii=False
    )

    print(
        "Report saved:",
        REPORT_FILE
    )
