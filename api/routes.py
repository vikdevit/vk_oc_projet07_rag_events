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
    response_model=HealthResponse,
    tags=["system"]
)
def health():

    return {
        "status": "ok",
        "service": "rag-api"
    }

@router.get(
        "/metadata",
        tags=["system"]
)
def metadata():

    return {
            "project": "RAG Events Viken OC",
            "version": "1.0",
            "vector_store": "FAISS",
            "embedding_model": "paraphrase-multilingual-mpnet-base-v2",
            "llm": "Mistral"
    }

@router.post(
    "/ask",
    response_model=AskResponse,
    tags=["rag"]
)
def ask(
    request: AskRequest
):

    question = request.question.strip()


    if not question:

        raise HTTPException(
            status_code=400,
            detail="Question cannot be empty"
        )


    try:

        answer = rag_answer(
            question
        )


        return {
            "question": question,
            "answer": answer
        }


    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )



@router.post(
    "/rebuild",
    response_model=RebuildResponse,
    tags=["admin"]
)
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
            "message":
            "Vector database rebuilt"
        }


    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )
