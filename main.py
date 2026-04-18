import os
import argparse
from dotenv import load_dotenv
from google import genai
from google.genai import types

def call_gemini_with_retry(client, messages, retries = 5):
    for i in range(retries):
        try:
            response = client.models.generate_content(
                    model = 'gemini-2.5-flash-lite',
                    contents = messages 
                    )
        except Exception as e:
            if "503" in str(e) and i < retries -1:
                wait_time = (2 ** i) # Waits 1, 2, 4, 8 seconds
                print(f"Server overloaded. Retrying in {wait_time}s...")
                time.sleep(wwait_time)
                continue
            raise e
        return response

def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    if api_key == None:
        raise RuntimeError("no API key found!")

    client = genai.Client(api_key=api_key)

    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()


    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]

    response = call_gemini_with_retry(client, messages)

    if response.usage_metadata == None:
        raise RuntimeError("failed API request!")

    if args.verbose:
        print(f"User prompt: {args.user_prompt}")
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
        
    print(response.text)

if __name__ == "__main__":
    main()
