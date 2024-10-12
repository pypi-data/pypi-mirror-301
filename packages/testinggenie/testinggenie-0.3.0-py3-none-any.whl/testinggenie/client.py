import json
import os
from anthropic import AnthropicVertex

def load_config(config_path="config.json"):
    """
    Load the configuration from a JSON file.
    """
    try:
        with open(config_path, 'r') as config_file:
            config = json.load(config_file)
        return config
    except FileNotFoundError:
        raise Exception("Configuration file not found. Please create a config.json file with your credentials.")
    except json.JSONDecodeError:
        raise Exception("Error parsing config.json file. Please check the format.")

def setup_anthropic_client(config):
    """
    Set up the Anthropic client using the loaded configuration.
    """
    # Set the Google credentials from the config file
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = config['google_application_credentials']
    
    # Set up the Anthropic API client with the user-provided location and project ID
    client = AnthropicVertex(region=config['location'], project_id=config['project_id'])
    return client

def anthropic_api_call(client, system_prompt, messages):
    """
    Call the Anthropic API using the client, system prompt, and user messages.
    """
    message = client.messages.create(
        system=system_prompt,
        model="claude-3-5-sonnet@20240620",
        max_tokens=4096,
        temperature=0.0,
        messages=messages,
    )
    response = message.model_dump_json(indent=2)
    response_dictionary = json.loads(response)
    return response_dictionary['content'][0]['text']
