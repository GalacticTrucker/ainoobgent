import os
from dotenv import load_dotenv
from google import genai

def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    # The client will automatically pick up the API key from the environment
    # variable GOOGLE_API_KEY or GEMINI_API_KEY.
    client = genai.Client(api_key=api_key)

    # Define your prompt
    prompt = "Why is Boot.dev such a great place to learn backend development? Use one paragraph maximum."

    # Use the correct syntax to call the generate_content method on the
    # client's models service
    response = client.models.generate_content(
        model='gemini-2.0-flash-001',
        contents=prompt
    )

    # Print the model's generated text
    print("--- Generated Text ---")
    print(response.text)

    # Check for and print the token usage metadata
    print("\n--- Token Usage ---")
    if hasattr(response, 'usage_metadata'):
        prompt_tokens = response.usage_metadata.prompt_token_count
        response_tokens = response.usage_metadata.candidates_token_count
        total_tokens = response.usage_metadata.total_token_count

        print(f"Prompt tokens: {prompt_tokens}")
        print(f"Response tokens: {response_tokens}")
        print(f"Total tokens: {total_tokens}")
    else:
        print("Usage metadata not available in this response.")


if __name__ == "__main__":
    main()