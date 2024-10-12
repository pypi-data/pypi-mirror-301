# Your Package Name

This package generates unit test cases for code snippets using the Anthropic API.

## Setup

1. Create a `config.json` file in the root directory of the package with the following content:

    ```json
    {
        "location": "your-region",
        "project_id": "your-project-id",
        "google_application_credentials": "path/to/your/credentials.json"
    }
    ```

2. Install the package:

    ```bash
    pip install testinggenie
    ```

## Usage

Run the main program:

```bash
from testinggenie import generate_test_cases
print (generate_test_cases("path_to_code_file"))
