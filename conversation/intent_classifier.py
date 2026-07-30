import re

# =====================================================
# Keyword Lists
# =====================================================

GREETINGS = {
    "hi",
    "hello",
    "hey",
    "good morning",
    "good afternoon",
    "good evening"
}

GOODBYES = {
    "bye",
    "goodbye",
    "see you",
    "take care"
}

THANKS = {
    "thanks",
    "thank you",
    "thankyou",
    "thx"
}

HELP = {
    "help",
    "what can you do",
    "how can you help"
}


# =====================================================
# Detect Intent
# =====================================================

def detect_intent(query):

    query = query.lower().strip()

    # -----------------------------------------
    # Greetings
    # -----------------------------------------

    if query in GREETINGS:

        return {

            "intent": "greeting"

        }

    # -----------------------------------------
    # Goodbye
    # -----------------------------------------

    if query in GOODBYES:

        return {

            "intent": "goodbye"

        }

    # -----------------------------------------
    # Gratitude
    # -----------------------------------------

    if query in THANKS:

        return {

            "intent": "thanks"

        }

    # -----------------------------------------
    # Help
    # -----------------------------------------

    if query in HELP:

        return {

            "intent": "help"

        }

    # -----------------------------------------
    # Explain Judgment
    # Example:
    # Explain Judgment 2
    # Explain Case 3
    # -----------------------------------------

    match = re.search(

        r"(judgment|case)\s+(\d+)",

        query

    )

    if match:

        return {

            "intent": "follow_up",

            "action": "explain",

            "judgment_number": int(match.group(2))

        }

    # -----------------------------------------
    # Compare
    # -----------------------------------------

    if query.startswith("compare"):

        return {

            "intent": "follow_up",

            "action": "compare"

        }

    # -----------------------------------------
    # Open
    # -----------------------------------------

    if query.startswith("open"):

        return {

            "intent": "follow_up",

            "action": "open"

        }

    # -----------------------------------------
    # Why Relevant
    # -----------------------------------------

    if "why" in query and "relevant" in query:

        return {

            "intent": "follow_up",

            "action": "relevance"

        }

    # -----------------------------------------
    # Default
    # -----------------------------------------

    return {

        "intent": "legal_query"

    }