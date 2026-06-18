from src.preprocessing.chunk_events import split_text


def test_chunk_size():

    text = "a" * 1200


    chunks = split_text(
        text,
        chunk_size=500,
        overlap=50
    )


    assert len(chunks) > 1


    for c in chunks:
        assert len(c) <= 500



def test_no_empty_chunks():

    text = "Bonjour ceci est un texte"


    chunks = split_text(text)


    assert all(
        len(c) > 0
        for c in chunks
    )
