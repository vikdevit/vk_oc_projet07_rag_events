import pytest

from src.preprocessing.clean_events_v2 import (
    clean_text,
    clean_event,
    build_rag_text
)


def test_clean_text_remove_spaces():

    text = "Bonjour     monde"

    result = clean_text(text)

    assert result == "Bonjour monde"



def test_clean_text_empty():

    assert clean_text(None) == ""



def test_build_rag_text():

    event = {

        "title": "Concert",

        "description": "Un concert",

        "longDescription": "Musique"

    }


    result = build_rag_text(event)


    assert "Concert" in result
    assert "Musique" in result



def test_clean_event_metadata():

    event = {

        "id":123,

        "title":"Test",

        "description":
            "Description assez longue pour passer le filtre " * 5,

        "city":"Paris",

        "department":"Paris",

        "type":"culture"

    }


    result = clean_event(event)


    assert result is not None
    assert result["metadata"]["city"]=="Paris"
    assert "text" in result
