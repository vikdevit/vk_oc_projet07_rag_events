# Assistant intelligent de recommandation d'événements culturels
### Projet 7 — Parcours AI Engineer OpenClassrooms

## Présentation

Ce projet consiste à développer un **assistant intelligent de recommandation d'événements culturels** basé sur une architecture **Retrieval-Augmented Generation (RAG)**.

Le système exploite les données publiques de **OpenAgenda** afin de répondre aux questions des utilisateurs en langage naturel en s'appuyant sur une recherche sémantique dans une base vectorielle **FAISS** avant la génération d'une réponse par un **LLM Mistral**.

L'objectif est de démontrer la faisabilité d'un système RAG capable de fournir des recommandations pertinentes tout en limitant les hallucinations du modèle de langage.

---

# Objectifs

Le projet répond aux besoins suivants :

- collecter automatiquement les événements OpenAgenda ;
- nettoyer et enrichir les données ;
- construire une base documentaire optimisée pour un système RAG ;
- rechercher les événements les plus pertinents grâce à la recherche vectorielle ;
- générer une réponse naturelle à partir d'un LLM ;
- exposer le système via une API REST ;
- déployer l'application dans un conteneur Docker.

---

# Fonctionnalités

Le système permet notamment :

- recherche d'événements culturels ;
- recherche d'activités pour enfants ;
- recherche par ville ;
- recherche par catégorie ;
- recommandations en langage naturel ;
- refus des questions hors domaine ("Je ne sais pas") ;
- reconstruction automatique de la base vectorielle ;
- documentation Swagger automatique.

Exemples de questions :

```
activité enfant à Paris ?
```

```
musée à Versailles ?
```

```
événements dans les Hauts-de-Seine ?
```

```
festival de musique à Paris ?
```

---

# Architecture du système

```text
                         OpenAgenda API
                               │
                               ▼
                     Collecte des événements
                               │
                               ▼
                  Nettoyage / Normalisation NLP
                               │
                               ▼
                Construction des documents RAG
                     (script document_builder_v2.py)
                               │
                               ▼
                       Chunking Sémantique
                               │
                               ▼
       Embeddings multilingues (SentenceTransformers)
                               │
                               ▼
                          Index FAISS
                               │
──────────────────────────────────────────────────────────────

                     Question utilisateur
                               │
                               ▼
                           FastAPI
                               │
                               ▼
                        Prompt Builder
                               │
                               ▼
                          Retriever
                               │
                               ▼
                           Reranker
                               │
                               ▼
                      Contexte pertinent
                               │
                               ▼
                     Chaîne RAG (LangChain)
                               │
                               ▼
                 LLM Mistral (génération)
                               │
                               ▼
                    Réponse utilisateur
                               │
                               ▼
                    API Dockerisée
```

---

# Technologies utilisées

## Langage

- Python 3.11

## Traitement du langage naturel (NLP)

- SentenceTransformers
- HuggingFace Transformers
- LangChain

Le NLP est utilisé à plusieurs niveaux :

- nettoyage et normalisation des données ;
- représentation sémantique des documents (embeddings) ;
- recherche sémantique ;
- reranking ;
- génération de la réponse avec le LLM.

## Base vectorielle

- FAISS

## Modèle de génération

- Mistral

## API

- FastAPI

## Tests

- Pytest

## Déploiement

- Docker

---

# Structure du projet

```text
api/
data/
docs/
scripts/
src/
tests/

Dockerfile
requirements.txt
README.md
```

Description des principaux dossiers :

| Dossier | Description |
|----------|-------------|
| api | API FastAPI |
| src | Pipeline RAG |
| tests | Tests unitaires et d'intégration |
| data | Données, documents et index FAISS |
| docs | Documentation |

---

# Installation

Créer un environnement virtuel

```bash
python -m venv env
```

Activation

Linux

```bash
source env/bin/activate
```

Installer les dépendances

```bash
pip install -r requirements.txt
```

---

# Pipeline de préparation

## 1. Collecte des données

```bash
PYTHONPATH=. python src/ingestion/fetch_openagenda_v34.py
```

## 2. Nettoyage

```bash
PYTHONPATH=. python src/preprocessing/clean_events_v2.py
```

## 3. Construction des documents

```bash
PYTHONPATH=. python src/preprocessing/document_builder_v2.py
```

## 4. Chunking sémantique

```bash
PYTHONPATH=. python src/preprocessing/semantic_chunk_events_v5.py
```

## 5. Génération des embeddings

```bash
PYTHONPATH=. python src/embeddings/embed_semantic_events_v4.py
```

## 6. Construction de l'index FAISS

```bash
PYTHONPATH=. python src/vectorstore/faiss_semantic_index_v5.py
```

## 7. Essai d'interrogation de l'index FAISS construit

```bash
PYTHONPATH=. python src/vectorstore/search_semantic_faiss_v5.py
```

## 8. Chaîne RAG : recherche des documents pertinents à partir de la requête user

```bash
PYTHONPATH=. python src/rag/retriever_v3.py
```

## 9. Chaîne RAG : réordonner les documents récupérés et conserver les plus pertinents pour la génération

```bash
PYTHONPATH=. python src/rag/reranker_v5.py
```

## 10. Chaîne RAG : construction du prompt envoyé au LLM à partir de la question du user et du contexte récupéré

```bash
PYTHONPATH=. python src/rag/prompt_builder_v3.py
```

## 11. Chaîne RAG : générer les réponses du modèle de langage à partir de l'API Mistral

```bash
PYTHONPATH=. python src/rag/mistral_generator_v3.py
```

## 12. Chaîne RAG : orchestration de la chaîne (recherche, reranking, construction du prompt et génération)

```bash
PYTHONPATH=. python src/rag/rag_chain_v3.py
```

## 13. Chaîne RAG : point d'entrée de la chaîne (question user -> chaîne RAG -> réponse produite)

```bash
PYTHONPATH=. python src/rag/ask_rag.py
```

---

# Lancement de l'API

```bash
PYTHONPATH=. uvicorn api.main:app --host 0.0.0.0 --port 8000
```

Documentation Swagger :

```
http://localhost:8000/docs
```

---

# Endpoints

## Vérification du service

```
GET /health
```

Réponse

```json
{
  "status": "ok",
  "service": "rag-api"
}
```

---

## Recherche d'événements

```
POST /ask
```

Exemple

```json
{
  "question": "activité enfant à Paris"
}
```

Réponse

```json
{
  "question": "activité enfant à Paris",
  "answer": "..."
}
```

---

## Reconstruction de la base vectorielle

```
POST /rebuild
```

Cette route reconstruit automatiquement :

- les documents RAG ;
- les embeddings ;
- l'index FAISS.

---

# Docker

Construction de l'image

```bash
docker build -t rag-events-api .
```

Lancement

```bash
docker run --rm \
--env-file .env \
-v ~/.cache/huggingface:/root/.cache/huggingface \
-p 8000:8000 \
rag-events-api
```

---

# Tests

Le projet comprend :

- tests unitaires ;
- tests d'intégration ;
- tests de la recherche FAISS ;
- tests du pipeline RAG ;
- tests API FastAPI.

Exécution

```bash
pytest
```

Résultat obtenu

```
63 tests
63 réussis
```

---

# Évaluation du système RAG

Le système est évalué sur un jeu de **30 questions annotées**.

Les métriques utilisées sont :

- similarité sémantique ;
- couverture des informations attendues ;
- détection d'hallucinations ;
- score global pondéré.

## Résultats

| Statut | Nombre |
|---------|--------:|
| Correct | 22 |
| Partiel | 6 |
| Incorrect | 2 |

Accuracy

```
73,3 %
```

Les réponses générées par le système sont volontairement concises tandis que les réponses de référence sont plus détaillées. L'évaluation combine donc une mesure de similarité sémantique et des critères métier afin d'obtenir un score représentatif des performances du système.

---

# Limites

Le projet constitue un **Proof of Concept (POC)**.

Les principales limites sont :

- dépendance aux données OpenAgenda ;
- couverture géographique limitée ;
- absence de mémoire conversationnelle ;
- performances dépendantes du modèle de génération ;
- temps de reconstruction de la base vectorielle.

---

# Perspectives

Les principales évolutions envisagées sont :

- combiner retrieval sémantique (embeddings pour correspondance de sens) et retrieval lexical (BM25 pour correspondance exacte de codes, numéros) avant le reranking ;
- ajout d'une mémoire conversationnelle ;
- mise à jour automatique des données OpenAgenda ;
- amélioration du reranking ;
- filtrage temporel avancé ;
- déploiement cloud ;
- supervision et monitoring ;
- optimisation des performances.

---

# Auteur
Viken KHATCHERIAN
Projet réalisé dans le cadre du **Projet 7 du parcours AI Engineer OpenClassrooms**.

