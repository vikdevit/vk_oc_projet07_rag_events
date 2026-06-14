from src.ingestion.fetch_openagenda_v20 import is_relevant_agenda


def test_is_relevant_agenda_true():

    agenda = {
        "title": "Festival de musique en Normandie",
        "description": "concert, spectacle et art"
    }

    assert is_relevant_agenda(agenda) is True


def test_is_relevant_agenda_false():

    agenda = {
        "title": "Conférence sur la finance",
        "description": "marchés et investissements"
    }

    assert is_relevant_agenda(agenda) is False
