#!/bin/bash

set -e

echo "Création de l'arborescence du projet..."

mkdir -p api

mkdir -p src/ingestion
mkdir -p src/preprocessing
mkdir -p src/embeddings
mkdir -p src/vectorstore
mkdir -p src/rag
mkdir -p src/reranker
mkdir -p src/utils

mkdir -p data/raw
mkdir -p data/processed
mkdir -p data/test_dataset

mkdir -p vectorstore/faiss_index

mkdir -p evaluation

mkdir -p tests/unit
mkdir -p tests/integration

mkdir -p docs/architecture
mkdir -p docs/screenshots

mkdir -p notebooks

mkdir -p docker

mkdir -p .github/workflows

echo "Arborescence créée avec succès!"
