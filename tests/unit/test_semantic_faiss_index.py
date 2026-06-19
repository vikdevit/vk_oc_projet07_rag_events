import os
import json


def test_faiss_index_exists():

    assert os.path.exists(
        "data/vectorstore/semantic_events.index"
    )



def test_metadata_exists():

    assert os.path.exists(
        "data/vectorstore/semantic_events_metadata.json"
    )



def test_metadata_matches():

    metadata=json.load(
        open(
        "data/vectorstore/semantic_events_metadata.json",
        encoding="utf-8"
        )
    )


    assert len(metadata)>0
