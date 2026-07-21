from elasticsearch import Elasticsearch

from config import *


es = Elasticsearch(

    ELASTIC_URL,

    basic_auth=(ELASTIC_USERNAME, ELASTIC_PASSWORD),

    verify_certs=False

)

INDEX_NAME = METADATA_INDEX


def get_document_by_citation(citation):

    print("\nSearching citation:", citation)

    response = es.search(

        index=INDEX_NAME,

        size=1,

        query={
            "match_phrase": {
                "citation": citation
            }
        }

    )

    hits = response["hits"]["hits"]

    print("\nTOTAL HITS:", len(hits))

    if len(hits) == 0:

        # fallback search using first SCC citation only

        short_citation = citation.split(":")[0].strip()

        print("Trying fallback:", short_citation)

        response = es.search(

            index=INDEX_NAME,

            size=1,

            query={
                "match_phrase": {
                    "citation": short_citation
                }
            }

        )

        hits = response["hits"]["hits"]

        print("FALLBACK HITS:", len(hits))

    if len(hits) == 0:

        return None

    return hits[0]["_source"]