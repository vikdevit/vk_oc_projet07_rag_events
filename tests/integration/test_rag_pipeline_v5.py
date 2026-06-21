from pathlib import Path


def test_semantic_pipeline_outputs():

    assert Path(
        "data/processed/clean_events.json"
    ).exists()


    assert Path(
        "data/processed/documents.json"
    ).exists()


    assert Path(
        "data/processed/semantic_chunks.json"
    ).exists()


def test_vectorstore_exists():

    assert Path(
        "data/vectorstore/semantic_events.index"
    ).exists()


    assert Path(
        "data/vectorstore/semantic_events_metadata.json"
    ).exists()
