#!/usr/bin/env python3
import sys
import json
import requests

def call_openai(model, prompt, api_key):
    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    data = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}]
    }
    
    try:
        response = requests.post(url, headers=headers, json=data, timeout=30)
        if response.status_code == 200:
            result = response.json()
            return result['choices'][0]['message']['content']
        else:
            return f"Error: HTTP status {response.status_code}"
    except Exception as e:
        return f"Error: {str(e)}"

def call_anthropic(model, prompt, api_key):
    url = "https://api.anthropic.com/v1/messages"
    headers = {
        "Content-Type": "application/json",
        "x-api-key": api_key,
        "anthropic-version": "2023-06-01"
    }
    data = {
        "model": model,
        "max_tokens": 1024,
        "messages": [{"role": "user", "content": prompt}]
    }
    
    try:
        response = requests.post(url, headers=headers, json=data, timeout=30)
        if response.status_code == 200:
            result = response.json()
            return result['content'][0]['text']
        else:
            return f"Error: HTTP status {response.status_code}"
    except Exception as e:
        return f"Error: {str(e)}"

def main():
    if len(sys.argv) != 4:
        print("Error: Requires model, api_key, and prompt arguments")
        sys.exit(1)

    model = sys.argv[1]
    api_key = sys.argv[2]
    prompt = sys.argv[3]
    
    if model.startswith('gpt'):
        response = call_openai(model, prompt, api_key)
    elif model.startswith('claude'):
        response = call_anthropic(model, prompt, api_key)
    else:
        response = f"Unsupported model: {model}"
    
    print(response)

if __name__ == "__main__":
    main()
