import os

from dotenv import load_dotenv
from openai import OpenAI


def get_openai_response(prompt: str) -> str:
    load_dotenv()

    api_key = os.environ.get("API_KEY")
    endpoint = os.environ.get("ENDPOINT")
    deployment_name = os.environ.get("DEPLOYMENT_NAME")

    client = OpenAI(base_url=endpoint, api_key=api_key)

    try:
        completion = client.chat.completions.create(
            model=deployment_name,
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
        )
        return completion.choices[0].message.content

    except (KeyError, IndexError, TypeError):
        raise SystemExit(f"Unexpected prompt format: {prompt}")


if __name__ == "__main__":
    test_prompt = "Hello, how are you?"
    print(get_openai_response(test_prompt))
