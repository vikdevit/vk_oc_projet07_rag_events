import json
import os


def test_semantic_chunks_exist():

    path = "data/processed/semantic_chunks.json"

    assert os.path.exists(path)

    with open(path, encoding="utf-8") as f:
        chunks = json.load(f)

    assert len(chunks) > 0



def test_chunk_structure():

    with open(
        "data/processed/semantic_chunks.json",
        encoding="utf-8"
    ) as f:
        chunks = json.load(f)


    chunk = chunks[0]


    assert "chunk_id" in chunk
    assert "text" in chunk
    assert len(chunk["text"]) > 50



def test_one_event_is_not_split_badly():

    with open(
        "data/processed/semantic_chunks.json",
        encoding="utf-8"
    ) as f:
        chunks = json.load(f)


    for c in chunks:

        text = c["text"]

        # un chunk doit garder son contexte
        assert "Titre" in text or "Événement" in text
