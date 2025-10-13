import sys
import openai
import anthropic

def main():
    if len(sys.argv) != 4:  # model, api_key, prompt
        print("Error: Requires model, api_key, and prompt arguments")
        sys.exit(1)

    model = sys.argv[1]
    api_key = sys.argv[2]
    prompt = sys.argv[3]
    
    try:
        if model.startswith('gpt'):
            openai.api_key = api_key
            response = openai.ChatCompletion.create(
                model=model,
                messages=[{"role": "user", "content": prompt}]
            )
            print(response.choices[0].message.content)
        elif model.startswith('claude'):
            client = anthropic.Anthropic(api_key=api_key)
            response = client.messages.create(
                model=model,
                messages=[{"role": "user", "content": prompt}]
            )
            print(response.content[0].text)
        else:
            print(f"Unsupported model: {model}")
            sys.exit(1)
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main() 