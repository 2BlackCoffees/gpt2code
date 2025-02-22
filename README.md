# Introduction to GPT2Code

GPT2Code is a highly extensible script designed to transform a hierarchical directory of source code into a new, similar hierarchical directory with  modified files. This powerful tool offers a range of predefined configurations to streamline your code development and optimization process.

## Important Security Consideration
Please note that this script is highly configurable and should only be used with an LLM endpoint that ensures the privacy and security of your requests, especially when dealing with confidential information.

## Predefined Configurations
GPT2Code comes with the following built-in configurations:

* Create Unittests: Automatically generate unit tests for your codebase.
* Comments Creation: Add informative comments to your source code to improve readability and maintainability.
* Language Best Practices: Enforce language-specific best practices to ensure consistency and quality in your code.
* OOP Best Practices: Apply object-oriented programming principles to enhance code organization and reusability.
* UML Class Diagrams Reverse Engineering: Generate UML class diagrams from your existing codebase.

## Custom Transformations
In addition to the predefined configurations, GPT2Code allows you to define custom transformations using a JSON file. This feature enables you to:

* Rewrite source code from one language to another
* Perform specific command-line operations
* Leverage external requests to enhance your code transformation process
* Adapt the script to your unique needs, making it an easy to reuse tool for any developer or development team.

To create new custom requests, a JSON file must be created with the following schema:

```json
[
    
    {
        "request_name": "Rewrite code to typescript very close to intial source code",
        "request": "Rewrite the whole code to node.js/typescript ensuring you stay as close as possible to the existing code, same function name, code organization, variable names, code block, ...",
        "temperature": 0.2, "top_p": 0.1
    }
]
```
This JSON file must be referenced using an environment variable. Please see the documentation for more information on this process.

## Error Handling
The program incorporates a backoff retry mechanism out of the box. However, if the number of tokens exceeds the limit, the script will stop executing. Currently, the only solution is to split the presentation into smaller parts. Note that token counting is not implemented, as this feature depends on the specific LLM being used.

## Prerequisites

Ensure that Python3 and openai libraries are installed.
Run `pip install -r gpt2code/requirements.txt`

## Environment Variables

The following environment variables are required to run the program:

* `OPENAI_BASE_URL`: The URL adress of your LLM (For example: `https://api.openai.com/v1`) 
* `OPENAI_API_KEY`: Your OpenAI API key
* `GPT2CODE_EXTERNAL_FILE_CODE_REQUESTS`: Path to the JSON file containing your additional requests to transforem the initial code, 

## Usage

To run the program, use the following command:
`python gpt2code [options]`

## Options

The program accepts the following options:
```bash
usage: gpt2code [-h] [--from_directory FROM_DIRECTORY] [--to_directory TO_DIRECTORY] [--model_name MODEL_NAME] [--skip_files SKIP_FILES] [--language_name LANGUAGE_NAME] [--code_request CODE_REQUEST]
                [--force_source_file_types FORCE_SOURCE_FILE_TYPES] [--force_destination_file_type FORCE_DESTINATION_FILE_TYPE] [--force_comment_string FORCE_COMMENT_STRING]
                [--force_destination_language_name FORCE_DESTINATION_LANGUAGE_NAME] [--debug] [--show_temperature_recommendations] [--simulate_calls_only] [--force_top_p] [--force_temperature]

options:
  -h, --help            show this help message and exit
  --from_directory FROM_DIRECTORY
                        Specify the directory to open
  --to_directory TO_DIRECTORY
                        Specify the directory where to store generated files
  --model_name MODEL_NAME
                        Specify the name of the LLM model to use. Default is llama3-70b
  --skip_files SKIP_FILES
                        Comma separated list of files to be skipped
  --language_name LANGUAGE_NAME
                        Language name: Java, Python, C++, C, Typescript, Shell, PlantUML, All
  --code_request CODE_REQUEST
                        Specify code request to process from the following list: [[ 0: Create Unittests, 1: Comments creation, 2: Language best practices, 3: OOP Best practices, 4: UML Class diagrams reverse
                        engineering ]], default is 0
  --force_source_file_types FORCE_SOURCE_FILE_TYPES
                        Specify source file types as regexp separated by commas
  --force_destination_file_type FORCE_DESTINATION_FILE_TYPE
                        Specify source file types as regexp separated by commas
  --force_comment_string FORCE_COMMENT_STRING
                        Specify the string to be used for comments
  --force_destination_language_name FORCE_DESTINATION_LANGUAGE_NAME
                        Specify the destination language name
  --debug               Set logging to debug
  --show_temperature_recommendations
                        Display values for various use cases
  --simulate_calls_only
                        Do not perform the calls to LLM: used for debugging purpose.
  --force_top_p         Increases diversity from various probable outputs in results.
  --force_temperature   Higher temperature increses non sense and creativity while lower yields to focused and predictable results.
```

### Example to create documentation including Doxygen comments: 
See the command line to create Doxygen documentation for a whole directory structure. Depending on the performance of your LLM model this could take several 10s of seconds per file. 

```bash
python gpt2code --from_directory data-platform/device-management --to_directory data-platform-commented-tmp-0.3-top-0.2 --language_name java --code_request 1
```

This will read all files from the directory data-platform/device-management and regenerate a similar directory tree with the same code having the various comments. This will include additional details from the LLM engine that would need to be filtered out but should not prevent the program to compile.

Please note that it can be useful to provide a destination directoy specifying the temperaturs and top_p parameters for future reference.

### Example to create your own requests:

Create the content of the file my_request.json:
```bash
cat > my_request.json << EOF
[
    
    {
        "request_name": "Rewrite code to typescript very close to initial source code",
        "request": "Rewrite the whole code to node.js/typescript ensuring you stay as close as possible to the existing code, same function name, code organization, variable names, code block, ...",
        "temperature": 0.2, "top_p": 0.1
    }
]
EOF
```
We need to define the following variable 
```bash
export  GPT2CODE_EXTERNAL_FILE_CODE_REQUESTS=my_request.json
```
Check that the file is properly loaded, and note that the parameter `--code_request` accepts now the value 5:
```bash
python gpt2code -h
2025-02-22 18:58:19 INFO     File my_request.json was read.
...
  --code_request CODE_REQUEST
                        Specify code request to process from the following list: [[ 0: Create Unittests, 1: Comments creation, 2: Language best practices, 3: OOP Best practices, 4: UML Class diagrams reverse
                        engineering, 5: Rewrite code to typescript very close to source code ]], default is 0
...
```

To use this new request, you might want to consider specific input or output language names. In addition comments of the target labguage shall be used to comment out what is not code specific relevant if the current LLM engine encoding provides a markdown response instead of pure languare response:
```bash
python gpt2code --from_directory java_code --to_directory new_code --force_comment_string '///' --force_source_file_types 'java' --force_destination_language_name typescript --code_request 5
```
