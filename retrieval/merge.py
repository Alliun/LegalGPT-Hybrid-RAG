from collections import defaultdict

# Reciprocal Rank Fusion constant
K = 60


def reciprocal_rank_fusion(metadata_results, semantic_results):

    fused = defaultdict(
        lambda: {
            "score": 0.0,
            "metadata_score": 0.0,
            "semantic_score": 0.0,
            "document": None,
        }
    )

    # ---------------------------------------------------
    # Metadata Results
    # ---------------------------------------------------
    for rank, hit in enumerate(metadata_results, start=1):

        source = hit["_source"]

        doc_id = source.get(
            "source_file",
            hit["_id"]
        )

        rrf = 1 / (K + rank)

        fused[doc_id]["score"] += rrf
        fused[doc_id]["metadata_score"] += rrf

        if fused[doc_id]["document"] is None:
            fused[doc_id]["document"] = hit

    # ---------------------------------------------------
    # Semantic Results
    # ---------------------------------------------------
    for rank, hit in enumerate(semantic_results, start=1):

        source = hit["_source"]

        doc_id = source.get(
            "source_file",
            hit["_id"]
        )

        rrf = 1 / (K + rank)

        fused[doc_id]["score"] += rrf
        fused[doc_id]["semantic_score"] += rrf

        if fused[doc_id]["document"] is None:
            fused[doc_id]["document"] = hit

    merged = sorted(
        fused.values(),
        key=lambda x: x["score"],
        reverse=True
    )

    return merged