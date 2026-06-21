from pydantic import BaseModel, Field


class AskRequest(BaseModel):
    """
    Question envoyée au RAG
    """

    question: str = Field(
        ...,
        min_length=3,
        description="Question utilisateur"
    )


class AskResponse(BaseModel):
    """
    Réponse RAG
    """

    question: str

    answer: str



class HealthResponse(BaseModel):

    status: str



class RebuildResponse(BaseModel):

    status: str

    message: str
