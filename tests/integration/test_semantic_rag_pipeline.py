import subprocess


def run_search(query):

    result=subprocess.run(
        [
            "python",
            "src/vectorstore/search_semantic_faiss_v4.py",
            query
        ],
        capture_output=True,
        text=True
    )

    return result.stdout



def test_search_family_event():

    output=run_search(
        "activité enfant à Paris"
    )

    assert "Paris" in output
    assert "famille" in output



def test_search_museum():

    output=run_search(
        "exposition photographie musée"
    )


    assert (
        "Exposition" in output
        or
        "photographique" in output
    )



def test_search_versailles():

    output=run_search(
        "événement Versailles"
    )


    assert "Versailles" in output
