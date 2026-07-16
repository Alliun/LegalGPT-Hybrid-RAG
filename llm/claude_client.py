import time

from anthropic import Anthropic

from config import ANTHROPIC_API_KEY, CLAUDE_MODEL

client = Anthropic(api_key=ANTHROPIC_API_KEY)


def ask_claude(system_prompt, user_prompt, temperature=0):

    retries = 3

    for attempt in range(retries):

        try:

            response = client.messages.create(

                model=CLAUDE_MODEL,

                max_tokens=4096,

                temperature=temperature,

                system=system_prompt,

                messages=[
                    {
                        "role": "user",
                        "content": user_prompt
                    }
                ]

            )

            return response.content[0].text

        except Exception as e:

            print(f"\nClaude attempt {attempt + 1} failed:")
            print(e)

            if attempt == retries - 1:
                raise

            time.sleep(2)