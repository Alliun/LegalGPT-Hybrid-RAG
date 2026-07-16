from elasticsearch import Elasticsearch

es = Elasticsearch(
    "https://localhost:9200",
    basic_auth=("elastic", "mRdWR4YB9yC4PsAE2zlx"),
    verify_certs=False
)

INDEX_NAME = "legal_metadata"


def get_document_by_citation(citation):

    print("\nSearching citation:", citation)

    response = es.search(

        index=INDEX_NAME,

        size=5,

        query={
            "match": {
                "citation": citation
            }
        }

    )

    print("\nTOTAL HITS:", response["hits"]["total"])

    for hit in response["hits"]["hits"]:

        print(hit["_source"].get("citation"))

    hits = response["hits"]["hits"]

    if not hits:
        return None

    return hits[0]["_source"]