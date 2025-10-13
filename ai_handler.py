import sys
import json
import qmclient

def get_api_key(qm, provider):
    # Connect to QM
    status = qm.connect("localhost", "qm", "username", "password")
    if not status:
        return f"QM Connection Error: {qm.error()}"
    
    # Open API.KEYS file
    status = qm.open("API.KEYS")
    if not status:
        return f"Cannot open API.KEYS: {qm.error()}"
    
    # Read API key
    status, key = qm.read("API.KEYS", provider)
    if not status:
        return f"Cannot read {provider} key: {qm.error()}"
    
    return key

def main():
    if len(sys.argv) != 3:
        print("Error: Requires model and prompt arguments")
        sys.exit(1)

    model = sys.argv[1]
    prompt = sys.argv[2]
    
    # Initialize QM connection
    qm = qmclient.QMClient()
    
    # Get appropriate API key
    if model.startswith('gpt'):
        api_key = get_api_key(qm, "OPENAI")
        # Call OpenAI
        # ... OpenAI code here
    elif model.startswith('claude'):
        api_key = get_api_key(qm, "ANTHROPIC")
        # Call Anthropic
        # ... Anthropic code here
    else:
        print(f"Unsupported model: {model}")
        sys.exit(1)

    # Print response for QMBasic to capture
    print(response)

if __name__ == "__main__":
    main() 