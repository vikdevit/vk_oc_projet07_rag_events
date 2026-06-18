import pytest

from src.ingestion.fetch_openagenda_v34 import (
    fetch_agendas,
    fetch_events
)



@pytest.mark.integration
def test_fetch_agendas_api():


    agendas = fetch_agendas()


    assert isinstance(
        agendas,
        list
    )


    assert len(agendas) > 0




@pytest.mark.integration
def test_fetch_events_api():


    agendas = fetch_agendas()


    assert len(agendas) > 0


    uid = agendas[0]["uid"]


    events = fetch_events(uid)


    assert isinstance(
        events,
        list
    )
