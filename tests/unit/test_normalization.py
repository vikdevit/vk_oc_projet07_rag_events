from src.ingestion.fetch_openagenda_v20 import normalize


def test_normalize_event():

    raw = {
        "uid": 123,
        "title_fr": "Concert Jazz",
        "description_fr": "Un super concert",
        "location_name": "Salle Pleyel",
        "location_city": "Paris",
        "location_department": "Paris",
        "firstdate_begin": "2026-01-01T10:00:00Z"
    }

    event = normalize(raw)

    assert event["id"] == 123
    assert event["title"] == "Concert Jazz"
    assert event["city"] == "Paris"
    assert event["start_date"] == "2026-01-01T10:00:00Z"
