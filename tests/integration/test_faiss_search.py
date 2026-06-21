import json
from pathlib import Path

import faiss

from sentence_transformers import (
    SentenceTransformer
)

INDEX_FILE = Path(
    "data/vectorstore/semantic_events.index"
)

METADATA_FILE = Path(
    "data/vectorstore/semantic_events_metadata.json"
)


def test_faiss_index_exists():

    assert INDEX_FILE.exists()


def test_metadata_exists():

    assert METADATA_FILE.exists()


def test_faiss_contains_all_vectors():

    index = faiss.read_index(
        str(INDEX_FILE)
    )

    with open(
        METADATA_FILE,
        encoding="utf-8"
    ) as f:

        metadata = json.load(f)

    assert index.ntotal == len(metadata)


def test_search_returns_results():

    index = faiss.read_index(
        str(INDEX_FILE)
    )

    with open(
        METADATA_FILE,
        encoding="utf-8"
    ) as f:

        metadata = json.load(f)

    model = SentenceTransformer(
        "paraphrase-multilingual-mpnet-base-v2"
    )

    query = model.encode(
        ["activité enfant"],
        convert_to_numpy=True
    )

    query = query.astype(
        "float32"
    )

    faiss.normalize_L2(
        query
    )

    scores, ids = index.search(
        query,
        5
    )

    assert len(ids[0]) > 0

    assert ids[0][0] >= 0

    assert scores[0][0] > 0
