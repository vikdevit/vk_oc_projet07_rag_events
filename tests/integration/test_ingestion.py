import pytest

from src.ingestion.fetch_openagenda_v19 import (
    fetch_agendas,
    fetch_events,
)


def test_fetch_agendas_api():

    agendas = fetch_agendas()

    assert isinstance(agendas, list)
    assert len(agendas) > 0


def test_fetch_events_api():

    agendas = fetch_agendas()

    assert len(agendas) > 0

    uid = agendas[0].get("uid")

    events = fetch_events(uid)

    assert isinstance(events, list)
