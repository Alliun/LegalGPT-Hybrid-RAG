from llm.claude_client import ask_claude

from query_processor.relevance_prompt import SYSTEM_PROMPT


# =====================================================
# Generate Relevance Analysis
# =====================================================

def explain_relevance(user_query, document):

    citation = document.get("citation", "")

    case_number = document.get("case_number", "")

    court = document.get("court", "")

    judges = document.get("judges", "")

    decided_date = document.get("decided_date", "")

    judgment_text = document.get("judgment_text", "")

    prompt = f"""
================================================================================
USER QUERY
================================================================================

{user_query}

================================================================================
RETRIEVED JUDGMENT
================================================================================

Citation:
{citation}

Case Number:
{case_number}

Court:
{court}

Judges:
{judges}

Decision Date:
{decided_date}

================================================================================
FULL JUDGMENT
================================================================================

{judgment_text}
"""

    return ask_claude(

        system_prompt=SYSTEM_PROMPT,

        user_prompt=prompt,

        temperature=0

    )