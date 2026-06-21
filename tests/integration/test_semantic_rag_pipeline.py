import subprocess


def run_search(query):

    result = subprocess.run(
        [
            "python",
            "src/vectorstore/search_semantic_faiss_v5.py",
            query
        ],
        capture_output=True,
        text=True
    )

    assert result.returncode == 0

    return result.stdout


def test_search_family_event():

    output = run_search(
        "activité enfant à Paris"
    )

    assert "SCORE:" in output
    assert len(output.strip()) > 0


def test_search_museum():

    output = run_search(
        "exposition photographie musée"
    )

    assert "SCORE:" in output
    assert len(output.strip()) > 0


def test_search_versailles():

    output = run_search(
        "événement Versailles"
    )

    assert "SCORE:" in output
    assert len(output.strip()) > 0
