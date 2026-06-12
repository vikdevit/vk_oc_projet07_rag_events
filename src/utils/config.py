from dotenv import load_dotenv
import os

load_dotenv()

MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")

TOP_K = int(os.getenv("TOP_K", 5))

CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", 500))

CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", 50))

EMBEDDING_MODEL = os.getenv(
    "EMBEDDING_MODEL",
    "mistral-embed"
)

LLM_MODEL = os.getenv(
    "LLM_MODEL",
    "mistral-small-latest"
)
