import re


def detect_intent(query):

    query = query.lower().strip()

    # ----------------------------------------
    # Explain Judgment
    # ----------------------------------------

    match = re.search(r"explain\s+judgment\s+(\d+)", query)

    if match:

        return {

            "intent": "explain",

            "judgment_number": int(match.group(1))

        }

    # ----------------------------------------
    # Search
    # ----------------------------------------

    return {

        "intent": "search"

    }