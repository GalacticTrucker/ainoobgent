import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types


def main():
    load_dotenv()
    verbose_flag = False
    api_key = os.environ.get("GEMINI_API_KEY")
    # The client will automatically pick up the API key from the environment
    # variable GOOGLE_API_KEY or GEMINI_API_KEY.
    client = genai.Client(api_key=api_key)

    args = sys.argv[1:]

    if not args:
        print("AI Code Assistant")
        print('\nUsage: python main.py "your prompt here"')
        print('Example: python main.py "How do I build a calculator app?"')
        sys.exit(1)

    # Define your prompt
    user_prompt = " ".join(args)

    if sys.argv[-1] == "--verbose":
        verbose_flag = True

    messages = [
    types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]   

    # Use the correct syntax to call the generate_content method on the
    # client's models service
    response = client.models.generate_content(
        model='gemini-2.0-flash-001',
        contents=messages,
    )

    # Print the model's generated text
    print("--- Generated Response ---")
    print(response.text)

    if verbose_flag:
        # Check for and print the token usage metadata
        print("\n--- Verbose data ---")
        if hasattr(response, 'usage_metadata'):
            prompt_tokens = response.usage_metadata.prompt_token_count
            response_tokens = response.usage_metadata.candidates_token_count
            total_tokens = response.usage_metadata.total_token_count
            
            print(f"User prompt: {user_prompt}")
            print(f"Prompt tokens: {prompt_tokens}")
            print(f"Response tokens: {response_tokens}")
            print(f"Total tokens: {total_tokens}")
        else:
            print("Usage metadata not available in this response.")


if __name__ == "__main__":
    main()