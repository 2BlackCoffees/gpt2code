# Introduction to GPT2Code

GPT2Code is a highly extensible script designed to transform a hierarchical directory of source code into a new, similar hierarchical directory with transformations applied to the source files. This powerful tool offers a range of predefined configurations to streamline your code development and optimization process.

## Important Security Consideration
Please note that this script is highly configurable and should only be used with an LLM endpoint that ensures the privacy and security of your requests, especially when dealing with confidential source code.

## Predefined Configurations
GPT2Code comes with the following built-in configurations:

### Create Unittests
* Automatically generate unit tests for your codebase trying to acheve 100% code coverage.
* This option is not designed to generate unittests that are ready to be used. Instead it is expected that the developer reviews them and updates them accordingly. Having a fully ready generated unit tests would defeat the purpose of creating unit tests!
### Comments Creation
* Add informative comments to your source code to improve readability and maintainability.
* This option works quite well. Still is is highly recommended to review in depth the generated comments to avoid misleading the next developer working on your code base.
### Review comments
* Verify that comments fit with the source code. 
* Provides list of files not fitting with additional explanations. 
* This is still a WIP and expected to be used in CI/CD.
### Language Best Practices
* Enforce language-specific best practices to ensure consistency and quality in your code.
* Generated code is based reading one file after the other.
* The LLM will rename some methods or improve some parameters in one file only.
* Other files reusing the improved class will currently not be modified (Thus still using old names).
* In order to achieve a proper update LLM should be used in coordination with an Abstract Syntax Tree.
* This might be a future evolution of this script.
### OOP Best Practices
* Apply object-oriented programming principles to enhance code organization and reusability.
* It is important to consider that the optimisation happens at a file level only.
* The script could be extended extracting the various classes, classes instantiations, methods and method calls calls to allow the LLM having a propoer high level view of the OOP design and propose a new one.
* The new generated design could only be applied as a manual refactoring leveraging many usefil tipps generated by the LLM. 
### UML Class Diagrams Reverse Engineering
* Generate UML class diagrams from your existing codebase in a plantUML format.
* Please note that despite the LLM typically properly finds classes, methods, method calls, it seems that class relations is not ptoperly handled and often wrongly reversed engineer.
* This could be due to the fact the LLM did not get trained with sufficient PlantUML files.

## Custom Transformations
In addition to the predefined configurations, GPT2Code allows you to define custom transformations using a JSON file. As a couple of examples, this feature can enable you to:

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
        "temperature": 0.2, 
        "top_p": 0.1
        // Following line is optional: To be used only if destination is a dufferent type as source file
        ,"forced_destination_language_name": "md"
    }
]
```
This JSON file must be referenced using the environment variable `GPT2CODE_EXTERNAL_FILE_CODE_REQUESTS` that should point to the json file either s an absolute path or relative to the location where the script os being called.

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

### Example to create documentation including Doxygen comments for Java sour files stored in one specific directory: 
See the command line to create Doxygen documentation for a whole directory structure. Depending on the performance of your LLM model this could take several 10s of seconds per file. 

```bash
python gpt2code --from_directory my-dir --to_directory my-dir-commented-tmp-0.3-top-0.2 --language_name java --code_request 1
```

This will read all files from the directory `my-dir` and regenerate a similar directory tree with the same code having the comments properly generated. 

Please note that it can be useful to provide a destination directoy specifying the transformation, the temperaturs and top_p parameters for future reference.

### Example to create your own requests:

Create the content of the file my_request.json:
```bash
cat > my_request.json << EOF
[
    
    {
        "request_name": "Rewrite code to typescript as the initial source code",
        "request": "Rewrite the whole code to node.js/typescript ensuring you keep exactly the same semantic and structure: same function name, code organization, variable names, code block, ...",
        "temperature": 0.2, 
        "top_p": 0.1
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
