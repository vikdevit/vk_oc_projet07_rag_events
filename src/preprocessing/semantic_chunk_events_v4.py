import json
from pathlib import Path

from langchain_text_splitters import RecursiveCharacterTextSplitter


INPUT = "data/raw/ingestion_events.json"
OUTPUT = "data/processed/semantic_chunks.json"


class EventSemanticChunker(RecursiveCharacterTextSplitter):
    """
    Chunker LangChain custom :
    - garde 1 événement complet
    - utilise RecursiveCharacterTextSplitter comme fallback
    """

    def split_event(self, event):

        text = f"""
Titre: {event.get('title','')}

Catégorie: {event.get('type','')}

Ville: {event.get('city','')}

Département: {event.get('department','')}

Date: {event.get('date','')}

Description:
{event.get('description','')}
""".strip()

        # un événement = un chunk
        return [{
            "chunk_id": event["id"],
            "text": text,
            "metadata": {
                "title": event.get("title"),
                "type": event.get("type"),
                "city": event.get("city"),
                "date": event.get("date")
            }
        }]


def main():

    events = json.load(open(INPUT, encoding="utf-8"))

    chunker = EventSemanticChunker(
        chunk_size=800,
        chunk_overlap=0
    )

    chunks=[]

    for event in events:

        chunks.extend(
            chunker.split_event(event)
        )


    Path("data/processed").mkdir(exist_ok=True)

    json.dump(
        chunks,
        open(OUTPUT,"w",encoding="utf-8"),
        ensure_ascii=False,
        indent=2
    )

    print("===================")
    print("DOCUMENTS:",len(events))
    print("CHUNKS:",len(chunks))
    print("SAVED:",OUTPUT)
    print("===================")


if __name__=="__main__":
    main()
