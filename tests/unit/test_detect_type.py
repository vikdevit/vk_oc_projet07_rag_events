from src.ingestion.fetch_openagenda_v34 import detect_event_type



def test_detect_culture():

    event = {

        "title": "Concert de musique classique",

        "description": "Festival et spectacle",

        "longDescription": "",

        "keywords": []

    }


    assert detect_event_type(event) == "culture"



def test_detect_patrimoine():

    event = {

        "title": "Visite du château",

        "description": "Découverte du patrimoine",

        "longDescription": "",

        "keywords": []

    }


    assert detect_event_type(event) == "patrimoine"



def test_detect_family():

    event = {

        "title": "Atelier bébé",

        "description": "Petite enfance",

        "longDescription": "",

        "keywords": []

    }


    assert detect_event_type(event) == "famille"



def test_detect_professional():

    event = {

        "title": "Job dating",

        "description": "Rencontre entreprises",

        "longDescription": "",

        "keywords": []

    }


    assert detect_event_type(event) == "professionnel"



def test_detect_other():

    event = {

        "title": "Evènement inconnu",

        "description": "",

        "longDescription": "",

        "keywords": []

    }


    assert detect_event_type(event) == "autre"
