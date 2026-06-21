import requests


# serveur FastAPI lancé avec :
# PYTHONPATH=. uvicorn api.main:app --host 0.0.0.0 --port 8000

BASE_URL = "http://192.168.1.26:8000"


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


    data = response.json()


    assert "question" in data

    assert "answer" in data

    assert len(data["answer"]) > 0



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



def test_rebuild():

    print("\n=== TEST REBUILD ===")


    response = requests.post(
        f"{BASE_URL}/rebuild",
        timeout=180
    )


    print(
        response.status_code
    )


    print(
        response.json()
    )


    assert response.status_code == 200


    data = response.json()


    assert data["status"] == "success"

    assert (
        "rebuilt"
        in data["message"].lower()
    )
