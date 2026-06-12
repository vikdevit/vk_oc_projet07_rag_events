# Assistant intelligent de recommandation d'événements culturels

Projet réalisé dans le cadre de la formation AI Engineer OpenClassrooms.

## Technologies

- OpenAgenda
- Mistral AI
- LangChain
- FAISS
- FastAPI
- Docker

## Installation

création du ficher de dépendances environment.yml

conda env create --prefix /mnt/projects/vk_oc_rag_events/envs/vk-oc-rag-events -f environment.yml

conda activate /mnt/projects/vk_oc_rag_events/envs/vk-oc-rag-events

contrôle des dépendances installées : pip list

test des imports en lançant le script test_envrionment.py
PYTHONPATH=. python tests/test_environment.py

résultats attendus 
FAISS OK
LangChain OK
Mistral OK

vérification de la clé API
PYTHONPATH=. python tests/test_config.py

résultat attendu
API KEY OK


à compléter
