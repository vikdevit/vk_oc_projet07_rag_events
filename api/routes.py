from fastapi import APIRouter, HTTPException
import subprocess

from api.schemas import (
    AskRequest,
    AskResponse,
    HealthResponse,
    RebuildResponse
)


from src.rag.rag_chain_v3 import rag_answer



router = APIRouter()



@router.get(
    "/health",
    response_model=HealthResponse
)
def health():

    return {
        "status": "ok",
        "service": "rag-api"
    }

@router.post("/ask")
def ask(request: AskRequest):

    if not request.question.strip():

        raise HTTPException(
            status_code=400,
            detail="Question cannot be empty"
        )

    try:

        answer = rag_answer(
            request.question
        )

        return {
            "question": request.question,
            "answer": answer
        }


    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )






@router.post("/rebuild")
def rebuild_index():

    try:

        subprocess.run(
            [
                "python",
                "src/vectorstore/faiss_semantic_index_v5.py"
            ],
            check=True
        )

        return {
            "status":"success",
            "message":"Vector database rebuilt"
        }


    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )
