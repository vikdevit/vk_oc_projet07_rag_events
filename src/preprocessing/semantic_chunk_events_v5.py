import json
from pathlib import Path

from langchain_text_splitters import RecursiveCharacterTextSplitter


#INPUT = "data/raw/ingestion_events.json"
INPUT = "data/processed/documents.json"
OUTPUT = "data/processed/semantic_chunks.json"


class EventSemanticChunker(
    RecursiveCharacterTextSplitter
):

    def split_document(self, document):

        metadata = document.get(
            "metadata",
            {}
        )

        content = document.get(
        "page_content",
        ""
        )

        description = ""

        if "Description:" in content:
            description = content.split(
                "Description:",
                1
            )[1].strip()


        metadata["description"] = description


        return [
            {

                "chunk_id":
                    document["id"],

                "text":
                    content,

                "metadata":
                    metadata

            }
        ]

def main():

    with open(
        INPUT,
        encoding="utf-8"
    ) as f:

        documents = json.load(f)


    chunker = EventSemanticChunker(
        chunk_size=800,
        chunk_overlap=0
    )


    chunks = []


    for document in documents:

        chunks.extend(
            chunker.split_document(document)
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
    print("DOCUMENTS :", len(documents))
    print("CHUNKS    :", len(chunks))
    print("SAVED     :", OUTPUT)
    print("===================")


if __name__ == "__main__":

    main()
