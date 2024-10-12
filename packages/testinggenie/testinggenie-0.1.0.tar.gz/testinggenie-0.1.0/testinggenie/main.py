from testinggenie.client import setup_anthropic_client, load_config, anthropic_api_call
from testinggenie.utils import read_file_to_string, extract_content

def generate_test_cases(file_path):
    # Load the configuration (one-time setup)
    config = load_config()  # This will load from config.json
    
    # Setup the Anthropic client using the configuration
    client = setup_anthropic_client(config)

    # Read the code snippet from a file
    code_snippet = read_file_to_string(file_path)
    
    # Define the system prompt for the API call
    system_prompt = """You are a multi-programming expert who knows almost all the coding languages 
                     and your task is to take the code snippet given by the user and generate a test case code 
                     for it in ```result and ```,And give the explanation to run that test case code in $$$ and $$$ . If you think that the given code is not unit testable just 
                     return ```result None``` and explain why it is not unit testable in explanation section under $$$ and $$$ and first statement should be the given code is not unit testable.
                     delimeter. Strictly follow the delimeters given."""
    
    # Prepare the message for the API call
    messages = [{"role": "user", "content": code_snippet}]
    
    # Make the API call
    response = anthropic_api_call(client, system_prompt, messages)
    
    # Extract the content from the response
    explanation = extract_content(response)
    print(f"Explanation: {explanation}")

if __name__ == "__main__":
    generate_test_cases()
