#!/bin/bash

echo "================================"
echo "Building FAISS vector index..."
echo "================================"

python src/vectorstore/faiss_semantic_index_v5.py

echo "================================"
echo "Index build completed"
echo "================================"
