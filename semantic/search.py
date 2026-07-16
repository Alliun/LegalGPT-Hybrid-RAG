from elasticsearch import Elasticsearch

from config import *
from semantic.embeddings import embed_text


# ======================================================
# Elasticsearch Connection
# ======================================================

es = Elasticsearch(
    ELASTIC_URL,
    basic_auth=(ELASTIC_USERNAME, ELASTIC_PASSWORD),
    verify_certs=False
)


# ======================================================
# Semantic Search
# ======================================================

def semantic_search(query, top_k=TOP_K):

    query_embedding = embed_text(query)

    response = es.search(
        index=SEMANTIC_INDEX,
        knn={
            "field": "embedding",
            "query_vector": query_embedding,
            "k": top_k,
            "num_candidates": KNN_CANDIDATES
        }
    )

    return response["hits"]["hits"]


# ======================================================
# Standalone Test
# ======================================================

if __name__ == "__main__":

    query = input("\nEnter Legal Query:\n\n")

    results = semantic_search(query)

    print("\n")
    print("=" * 100)
    print("TOP SEMANTIC RESULTS")
    print("=" * 100)

    if len(results) == 0:

        print("\nNo matching judgments found.")

    else:

        for rank, hit in enumerate(results, start=1):

            source = hit["_source"]

            print("\n")
            print("=" * 100)

            print(f"Rank : {rank}")

            print(f"Similarity Score : {hit['_score']:.2f}")

            print(f"Citation : {source.get('citation')}")

            print(f"Court : {source.get('court')}")

            print(f"Case Number : {source.get('case_number')}")

            print(f"Source File : {source.get('source_file')}")

            print("\nPreview\n")

            print(source.get("judgment_text", "")[:700])