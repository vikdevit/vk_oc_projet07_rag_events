import subprocess
import os



def test_ask_rag_cli():


    env = os.environ.copy()

    env["PYTHONPATH"] = "."


    result = subprocess.run(
        [
            "python",
            "src/rag/ask_rag.py",
            "activité enfant Paris"
        ],
        capture_output=True,
        text=True,
        env=env
    )


    assert result.returncode == 0


    assert (
        "ANSWER"
        in result.stdout
    )


    assert len(
        result.stdout
    ) > 100
