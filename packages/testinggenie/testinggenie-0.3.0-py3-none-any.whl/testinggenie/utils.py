import re

def read_file_to_string(file_path):
    """
    Read the content of a file and return it as a string.
    """
    try:
        with open(file_path, 'r') as file:
            file_contents = file.read()
        return file_contents
    except FileNotFoundError:
        return "File not found. Please check the file path."
    except Exception as e:
        return f"An error occurred: {str(e)}"

def extract_content(file_content):
    """
    Extract the content between custom delimiters from the file content.
    """
    # Regex patterns to extract the contents
    result_pattern = r"```result([\s\S]*?)```"
    explanation_pattern = r"\${3}([\s\S]*?)\${3}"

    # Extract the content between ```result and ``` using regex
    result_match = re.search(result_pattern, file_content)
    if result_match:
        result_content = result_match.group(1).strip()
    else:
        result_content = "No result content found."

    # Extract the content between $$$ and $$$ using regex
    explanation_match = re.search(explanation_pattern, file_content)
    if explanation_match:
        explanation = explanation_match.group(1).strip()
    else:
        explanation = "No explanation content found."
    
    # Write the result content to test_case.txt
    if result_content != "No result content found.":
        with open('test_case.txt', 'w') as file:
            file.write(result_content)
    
    return explanation
