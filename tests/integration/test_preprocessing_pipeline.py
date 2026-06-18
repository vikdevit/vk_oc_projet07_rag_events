# tests/integration/test_preprocessing_pipeline.py

import json
from pathlib import Path


def test_preprocessing_pipeline():


    files = [

        "data/processed/clean_events.json",

        "data/processed/documents.json",

        "data/processed/chunks.json"

    ]


    for file in files:

        assert Path(file).exists()



    clean=json.load(
        open(files[0])
    )

    docs=json.load(
        open(files[1])
    )

    chunks=json.load(
        open(files[2])
    )


    assert len(clean) > 0

    assert len(docs) == len(clean)

    assert len(chunks) > len(docs)


    # format RAG

    assert "text" in clean[0]


    assert "page_content" in docs[0]


    assert "metadata" in docs[0]


    assert "chunk_id" in chunks[0]


    assert len(chunks[0]["page_content"]) <= 500
