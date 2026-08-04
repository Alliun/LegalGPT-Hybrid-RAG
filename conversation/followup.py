# =====================================================
# Follow-up Resolution
# =====================================================

NUMBER_WORDS = {

    "first": 1,
    "second": 2,
    "third": 3,
    "fourth": 4,
    "fifth": 5

}


REFERENCE_WORDS = [

    "it",
    "this",
    "that",
    "previous"

]


def resolve_followup(query, conversation_context):

    query = query.lower()

    results = conversation_context.get_last_results()

    # ------------------------------------------
    # No previous search
    # ------------------------------------------

    if not results:

        return None

    # ------------------------------------------
    # first / second / third...
    # ------------------------------------------

    for word, number in NUMBER_WORDS.items():

        if word in query:

            index = number - 1

            if index < len(results):

                conversation_context.set_active_judgment(index)

                return index

    # ------------------------------------------
    # it / this / that
    # ------------------------------------------

    if any(word in query for word in REFERENCE_WORDS):

        if conversation_context.active_index is not None:

            return conversation_context.active_index

    return None