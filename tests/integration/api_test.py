# tests/integration/api_test_v2.py

import requests


# serveur FastAPI :
# PYTHONPATH=. uvicorn api.main:app --host 0.0.0.0 --port 8000

BASE_URL = "http://192.168.1.26:8000"


# -------------------------
# REBUILD INDEX
# -------------------------

def test_rebuild():

    print("\n=== TEST REBUILD ===")

    response = requests.post(
        f"{BASE_URL}/rebuild",
        timeout=300
    )

    print(
        response.status_code,
        response.json()
    )

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "success"

    assert (
        "rebuilt"
        in data["message"].lower()
    )



# -------------------------
# HEALTH
# -------------------------

def test_health():

    print("\n=== TEST HEALTH ===")

    response = requests.get(
        f"{BASE_URL}/health",
        timeout=10
    )

    print(
        response.status_code,
        response.json()
    )

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "ok"

    assert data["service"] == "rag-api"



# -------------------------
# NORMAL RAG QUESTION
# -------------------------

def test_ask():

    print("\n=== TEST ASK RAG ===")


    payload = {
        "question": "activité enfant à Paris"
    }


    response = requests.post(
        f"{BASE_URL}/ask",
        json=payload,
        timeout=120
    )


    print(
        response.status_code
    )

    print(
        response.json()
    )


    assert response.status_code == 200


    data=response.json()


    assert "question" in data

    assert "answer" in data

    assert len(data["answer"]) > 0


    # validation métier :
    # cette question doit avoir une réponse
    assert (
        data["answer"].lower()
        !=
        "je ne sais pas."
    )



# -------------------------
# EMPTY QUESTION
# -------------------------

def test_empty_question():

    print("\n=== TEST EMPTY QUESTION ===")


    payload = {
        "question": ""
    }


    response = requests.post(
        f"{BASE_URL}/ask",
        json=payload,
        timeout=10
    )


    print(
        response.status_code,
        response.json()
    )


    assert response.status_code == 400


    assert (
        response.json()["detail"]
        ==
        "Question cannot be empty"
    )



# -------------------------
# OUT OF DOMAIN
# -------------------------

def test_unknown_domain_question():

    print("\n=== TEST OUT OF DOMAIN ===")


    payload = {
        "question":
        "prix du pétrole aujourd'hui"
    }


    response = requests.post(
        f"{BASE_URL}/ask",
        json=payload,
        timeout=120
    )


    print(
        response.status_code
    )

    print(
        response.json()
    )


    assert response.status_code == 200


    data=response.json()


    assert "answer" in data


    # le RAG doit refuser
    assert (
        "je ne sais pas"
        in
        data["answer"].lower()
    )
