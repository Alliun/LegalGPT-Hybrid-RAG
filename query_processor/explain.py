from llm.claude_client import ask_claude


SYSTEM_PROMPT = """
You are an expert legal research assistant.

Return your answer in clean GitHub Markdown.

Structure it exactly like this.

# Facts

...

# Legal Issues

...

# Court's Reasoning

...

# Final Decision

...

# Key Legal Principles

- Principle 1
- Principle 2
- Principle 3

Never return JSON.

Never include code fences.

Never invent facts.

Use only the supplied judgment.
"""


def explain_judgment(document):

    judgment = document.get("judgment_text", "")

    prompt = f"""
Explain the following legal judgment.

Judgment

{judgment}
"""

    print("\n" + "=" * 80)
    print("EXPLAIN REQUEST")
    print("=" * 80)
    print("Citation :", document.get("citation", ""))
    print("Case No. :", document.get("case_number", ""))
    print("Court    :", document.get("court", ""))
    print("Length   :", len(judgment), "characters")

    try:

        response = ask_claude(

            system_prompt=SYSTEM_PROMPT,

            user_prompt=prompt,

            temperature=0

        )

        print("\n" + "=" * 80)
        print("CLAUDE RESPONSE RECEIVED")
        print("=" * 80)
        print(response[:500])

        return response

    except Exception as e:

        print("\n" + "=" * 80)
        print("CLAUDE ERROR")
        print("=" * 80)
        print(str(e))

        raise