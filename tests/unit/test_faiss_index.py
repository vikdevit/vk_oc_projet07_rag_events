import json
from pathlib import Path

import faiss

INDEX_FILE = Path(
    "data/vectorstore/semantic_events.index"
)

METADATA_FILE = Path(
    "data/vectorstore/semantic_events_metadata.json"
)


def test_faiss_index_exists():

    assert INDEX_FILE.exists()


def test_faiss_index_load():

    index = faiss.read_index(
        str(INDEX_FILE)
    )

    assert index is not None


def test_faiss_index_dimension():

    index = faiss.read_index(
        str(INDEX_FILE)
    )

    # mpnet-base-v2
    assert index.d == 768


def test_faiss_index_number_vectors():

    index = faiss.read_index(
        str(INDEX_FILE)
    )

    with open(
        METADATA_FILE,
        encoding="utf-8"
    ) as f:

        metadata = json.load(f)

    assert index.ntotal == len(metadata)


def test_metadata_exists():

    assert METADATA_FILE.exists()


def test_metadata_matches_index():

    index = faiss.read_index(
        str(INDEX_FILE)
    )

    with open(
        METADATA_FILE,
        encoding="utf-8"
    ) as f:

        metadata = json.load(f)

    assert len(metadata) == index.ntotal
