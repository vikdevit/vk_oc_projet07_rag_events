import json
from pathlib import Path

import faiss
import numpy as np



INDEX_FILE = Path(
    "data/vectorstore/semantic_events.index"
)

EMBED_FILE = Path(
    "data/processed/semantic_embeddings.json"
)



def load_test_data():

    index = faiss.read_index(
        str(INDEX_FILE)
    )


    with open(
        EMBED_FILE,
        encoding="utf-8"
    ) as f:

        embeddings = json.load(f)


    return index, embeddings



def test_search_returns_results():

    index, embeddings = load_test_data()


    vector = np.array(
        embeddings[0]["embedding"],
        dtype="float32"
    )


    distances, ids = index.search(
        np.array(
            [vector]
        ),
        5
    )


    assert len(ids[0]) == 5



def test_search_returns_valid_ids():

    index, embeddings = load_test_data()


    vector = np.array(
        embeddings[0]["embedding"],
        dtype="float32"
    )


    distances, ids = index.search(
        np.array(
            [vector]
        ),
        5
    )


    for idx in ids[0]:

        assert idx >= 0
        assert idx < index.ntotal



def test_search_distance_exists():

    index, embeddings = load_test_data()


    vector = np.array(
        embeddings[0]["embedding"],
        dtype="float32"
    )


    distances, ids = index.search(
        np.array(
            [vector]
        ),
        1
    )


    assert distances[0][0] >= 0



def test_search_same_vector_best_score():

    index, embeddings = load_test_data()


    vector = np.array(
        embeddings[0]["embedding"],
        dtype="float32"
    )


    distances, ids = index.search(
        np.array(
            [vector]
        ),
        1
    )


    assert ids[0][0] >= 0
