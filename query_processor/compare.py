from llm.claude_client import ask_claude

from query_processor.compare_prompt import SYSTEM_PROMPT


def compare_judgments(document1, document2):

    judgment1 = document1.get("judgment_text", "")

    judgment2 = document2.get("judgment_text", "")

    citation1 = document1.get("citation", "")

    citation2 = document2.get("citation", "")

    prompt = f"""
Compare the following two legal judgments.

====================================================
Judgment 1
====================================================

Citation:
{citation1}

Judgment:

{judgment1}

====================================================
Judgment 2
====================================================

Citation:
{citation2}

Judgment:

{judgment2}
"""

    comparison = ask_claude(

        system_prompt=SYSTEM_PROMPT,

        user_prompt=prompt,

        temperature=0

    )

    return comparison