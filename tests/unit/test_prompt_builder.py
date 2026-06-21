from src.rag.prompt_builder_v3 import build_prompt


def test_prompt_contains_question():

    prompt = build_prompt(
        "activité enfant Paris",
        [
            {
                "title":"Atelier enfant",
                "type":"famille",
                "city":"Paris",
                "department":"75",
                "start_date":"2026-03-17",
                "description":"Jeux enfants"
            }
        ]
    )


    assert "activité enfant Paris" in prompt
    assert "Atelier enfant" in prompt
    assert "Paris" in prompt
