from llm.claude_client import ask_claude

from query_processor.rerank_prompt import SYSTEM_PROMPT


def rerank(query, merged_results):

    cases = []

    for item in merged_results[:10]:

        src = item["document"]["_source"]

        cases.append({

            "citation": src.get("citation"),

            "court": src.get("court"),

            "judge": src.get("judges"),

            "sections": src.get("sections_referred"),

            "outcome": src.get("outcome"),

            "preview": src.get("judgment_text", "")[:1200]

        })

    prompt = f"""

User Query

{query}

Retrieved Judgments

{cases}

"""

    response = ask_claude(

        system_prompt=SYSTEM_PROMPT,

        user_prompt=prompt,

        temperature=0

    )

    return response