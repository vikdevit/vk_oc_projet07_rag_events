"""
Prompt builder RAG

semantic retriever
        |
        v
reranker
        |
        v
prompt LLM
"""


from src.rag.retriever_v3 import retrieve
from src.rag.reranker_v5 import rerank



# =====================
# BUILD CONTEXT
# =====================

def build_context(docs):

    blocks = []


    for i, doc in enumerate(
        docs,
        start=1
    ):

        block = f"""
Événement {i}

Titre:
{doc.get("title")}

Type:
{doc.get("type")}

Ville:
{doc.get("city")}

Département:
{doc.get("department")}

Date:
{doc.get("start_date")}

Description:
{doc.get("description")}
"""

        blocks.append(block)


    return "\n".join(blocks)



# =====================
# BUILD PROMPT
# =====================

def build_prompt(
    query,
    docs
):

    context = build_context(
        docs
    )


    #return f"""
    
    #Tu es un assistant spécialisé dans les événements.

    #Réponds uniquement avec les informations présentes dans le contexte.

    #Pour chaque événement pertinent, indique si disponible :
    #- le titre
    #- la catégorie
    #- la ville
    #- la date
    #- une courte description

    #N'invente aucune information.

    #Si aucune information pertinente n'est présente,
    #indique que tu ne sais pas.

    #Question utilisateur:
    #{query}


    #Contexte événements:
    #{context}


    #Réponse:
    #"""
    return f"""

    Tu es un assistant spécialisé dans les événements.

    Réponds uniquement avec les informations présentes dans le contexte.

    Sélectionne uniquement les événements pertinents
    pour la question utilisateur.

    Pour chaque événement retenu, indique :

    - Titre
    - Catégorie
    - Ville
    - Date
    - Description

    N'invente aucune information.

    Ne mentionne jamais le numéro interne du contexte
    (Événement 1, Événement 2...).

    Renumérote les événements dans ta réponse
    à partir de 1.

    Si aucune information pertinente n'est présente,
    réponds :
    "Je ne sais pas."

    Question utilisateur:

    {query}


    Contexte événements:

    {context}


    Réponse:

    """


# =====================
# TEST
# =====================

if __name__ == "__main__":


    query = "activité enfant à Paris"


    docs = retrieve(
        query,
        top_k=10
    )


    docs = rerank(
        query,
        docs
    )


    prompt = build_prompt(
        query,
        docs
    )


    print(prompt)
