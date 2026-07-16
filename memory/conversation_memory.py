# =====================================================
# Conversation Memory
# =====================================================

conversation = {

    "last_query": None,

    "last_results": []

}


# =====================================================
# Save Search Results
# =====================================================

def save_search(query, results):

    conversation["last_query"] = query

    conversation["last_results"] = results


# =====================================================
# Get Last Results
# =====================================================

def get_last_results():

    return conversation["last_results"]


# =====================================================
# Get Last Query
# =====================================================

def get_last_query():

    return conversation["last_query"]