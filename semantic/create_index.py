from elasticsearch import Elasticsearch
from config import *

es = Elasticsearch(
    ELASTIC_URL,
    basic_auth=(ELASTIC_USERNAME, ELASTIC_PASSWORD),
    verify_certs=False
)

if es.indices.exists(index=SEMANTIC_INDEX):
    es.indices.delete(index=SEMANTIC_INDEX)

mapping = {
    "mappings": {
        "properties": {

            "citation": {
                "type": "keyword"
            },

            "court": {
                "type": "keyword"
            },

            "case_number": {
                "type": "keyword"
            },

            "source_file": {
                "type": "keyword"
            },

            "judgment_text": {
                "type": "text"
            },

            "embedding": {
                "type": "dense_vector",
                "dims": EMBEDDING_DIMENSION,
                "index": True,
                "similarity": "cosine"
            }

        }
    }
}

es.indices.create(
    index=SEMANTIC_INDEX,
    body=mapping
)

print("Semantic index created successfully.")