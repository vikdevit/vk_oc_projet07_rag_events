from src.ingestion.fetch_openagenda_v34 import (
    is_valid,
    is_recent,
    is_target_zone
)



def test_valid_event():

    event = {

        "id": 1,

        "title": "Test",

        "start_date": "2026-01-01T10:00:00Z"

    }


    assert is_valid(event)



def test_invalid_event():

    event = {

        "id": None,

        "title": "",

        "start_date": None

    }


    assert not is_valid(event)



def test_target_zone():

    event = {

        "department": "Paris",

        "city": "Paris"

    }


    assert is_target_zone(event)



def test_not_target_zone():

    event = {

        "department": "Bretagne",

        "city": "Rennes"

    }


    assert not is_target_zone(event)
