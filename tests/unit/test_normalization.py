from src.ingestion.fetch_openagenda_v34 import normalize


def test_normalize_event():

    raw = {

        "uid": 123,

        "title": {
            "fr": "Concert Jazz"
        },

        "description": {
            "fr": "Un super concert"
        },

        "longDescription": {
            "fr": "Une soirée jazz"
        },

        "motive": {
            "fr": ""
        },

        "keywords": {
            "fr": [
                "musique"
            ]
        },

        "location": {

            "city": "Paris",

            "department": "Paris"
        },

        "firstTiming": {

            "begin": "2026-01-01T10:00:00Z"

        }

    }


    event = normalize(raw)


    assert event["id"] == 123

    assert event["title"] == "Concert Jazz"

    assert event["description"] == "Un super concert"

    assert event["city"] == "Paris"

    assert event["department"] == "Paris"

    assert event["keywords"] == ["musique"]

    assert "Concert Jazz" in event["search_text"]

    assert "musique" in event["search_text"]

    assert event["start_date"] == "2026-01-01T10:00:00Z"
