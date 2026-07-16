import json

from llm.claude_client import ask_claude

from .prompts import SYSTEM_PROMPT


# ---------------------------------------------------
# Clean Claude JSON
# ---------------------------------------------------

def clean_json(text):

    text = text.strip()

    if text.startswith("```json"):

        text = text.replace("```json", "", 1)

    if text.startswith("```"):

        text = text.replace("```", "", 1)

    if text.endswith("```"):

        text = text[:-3]

    return text.strip()


# ---------------------------------------------------
# Extract Metadata
# ---------------------------------------------------

def extract_metadata(user_query):

    response = ask_claude(

        system_prompt=SYSTEM_PROMPT,

        user_prompt=user_query,

        temperature=0

    )

    response = clean_json(response)

    try:

        metadata = json.loads(response)

        return metadata

    except json.JSONDecodeError as e:

        print("\n" + "=" * 80)
        print("CLAUDE RESPONSE")
        print("=" * 80)
        print(response)

        print("\n" + "=" * 80)
        print("JSON ERROR")
        print("=" * 80)
        print(e)

        raise Exception("Claude did not return valid JSON.")


# ---------------------------------------------------
# Test
# ---------------------------------------------------

if __name__ == "__main__":

    query = input("Enter Legal Query:\n\n")

    result = extract_metadata(query)

    print("\nExtracted Metadata\n")

    print(json.dumps(result, indent=4))