from src.preprocessing.document_builder import (
    build_content,
    build_metadata
)



def test_build_content():

    event = {

        "metadata":{

            "title":"Expo",

            "city":"Paris",

            "department":"Paris",

            "type":"culture",

            "start_date":"2026-01-01"

        },

        "text":"Description expo"

    }


    result = build_content(event)


    assert "Expo" in result
    assert "Paris" in result
    assert "Description expo" in result



def test_build_metadata():

    event={

        "id":123,

        "metadata":{

            "title":"Expo",

            "url":"http://test.fr",

            "keywords":["expo"]

        }

    }


    result=build_metadata(event)


    assert result["event_id"]==123
    assert result["url"]=="http://test.fr"
    assert result["keywords"]==["expo"]
