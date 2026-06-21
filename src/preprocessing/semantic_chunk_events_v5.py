import json
from pathlib import Path

from langchain_text_splitters import RecursiveCharacterTextSplitter


INPUT = "data/raw/ingestion_events.json"
OUTPUT = "data/processed/semantic_chunks.json"


class EventSemanticChunker(
    RecursiveCharacterTextSplitter
):

    def split_event(self, event):

        title = event.get("title","")
        event_type = event.get("type","")
        city = event.get("city","")
        department = event.get("department","")

        date = (
            event.get("start_date")
            or event.get("date")
            or ""
        )

        description = event.get(
            "description",
            ""
        )


        text = f"""
Titre: {title}

Catégorie: {event_type}

Ville: {city}

Département: {department}

Date: {date}

Description:
{description}
""".strip()


        return [
            {
                "chunk_id": event["id"],

                "text": text,

                "metadata": {

                    "title": title,

                    "type": event_type,

                    "city": city,

                    "department": department,

                    "start_date": date,

                    "description": description

                }
            }
        ]



def main():


    with open(
        INPUT,
        encoding="utf-8"
    ) as f:

        events = json.load(f)



    chunker = EventSemanticChunker(
        chunk_size=800,
        chunk_overlap=0
    )


    chunks=[]


    for event in events:

        chunks.extend(
            chunker.split_event(event)
        )



    Path(
        "data/processed"
    ).mkdir(
        exist_ok=True
    )


    with open(
        OUTPUT,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            chunks,
            f,
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
