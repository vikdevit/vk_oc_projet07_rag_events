import json
import os


def test_embeddings_exist():

    path = "data/processed/semantic_embeddings.json"

    assert os.path.exists(path)



def test_embedding_dimension():

    with open(
        "data/processed/semantic_embeddings.json",
        encoding="utf-8"
    ) as f:
        data = json.load(f)


    vector = data[0]["embedding"]

    # mpnet multilingual
    assert len(vector) == 768



def test_embedding_count_matches_chunks():

    chunks=json.load(
        open(
        "data/processed/semantic_chunks.json",
        encoding="utf-8"
        )
    )


    embeddings=json.load(
        open(
        "data/processed/semantic_embeddings.json",
        encoding="utf-8"
        )
    )


    assert len(chunks)==len(embeddings)
