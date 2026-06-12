#!/bin/bash

echo "📁 Création des .gitkeep pour structure projet RAG..."

# API
touch api/.gitkeep

# SRC
touch src/ingestion/.gitkeep
touch src/preprocessing/.gitkeep
touch src/embeddings/.gitkeep
touch src/vectorstore/.gitkeep
touch src/rag/.gitkeep
touch src/reranker/.gitkeep
touch src/utils/.gitkeep

# DATA (sauf raw/processed ignorés par gitignore)
touch data/test_dataset/.gitkeep

# VECTORSTORE
touch vectorstore/faiss_index/.gitkeep

# EVALUATION
touch evaluation/.gitkeep

# TESTS
touch tests/unit/.gitkeep
touch tests/integration/.gitkeep

# DOCS
touch docs/architecture/.gitkeep
touch docs/screenshots/.gitkeep

# AUTRES
touch notebooks/.gitkeep
touch docker/.gitkeep

# GITHUB WORKFLOWS
mkdir -p .github/workflows
touch .github/workflows/.gitkeep

echo "✅ Structure .gitkeep créée avec succès"
