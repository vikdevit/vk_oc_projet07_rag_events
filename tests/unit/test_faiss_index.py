import json
from pathlib import Path

import faiss


INDEX_FILE = Path(
    "data/vectorstore/events.index"
)

METADATA_FILE = Path(
    "data/vectorstore/events_metadata.json"
)



def test_faiss_index_exists():

    assert INDEX_FILE.exists()



def test_faiss_index_load():

    index = faiss.read_index(
        str(INDEX_FILE)
    )

    assert isinstance(
        index,
        faiss.Index
    )



def test_faiss_index_dimension():

    index = faiss.read_index(
        str(INDEX_FILE)
    )

    assert index.d == 384



def test_faiss_index_number_vectors():

    index = faiss.read_index(
        str(INDEX_FILE)
    )

    assert index.ntotal > 0



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
