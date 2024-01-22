# Documentation of the use of Azure Function Apps to receive and process messages from Azure Servicebus  

[Functions folder structure](#functions-folder-structure)  
[Description of code](#description-of-code)  
[Process flow](#process-flow)
[Function app - how it works](#function-app---how-it-works)  

## Functions folder structure

```bash
functions/
    .funcignore
    config.yaml
    deploy.sh
    function_app.py
    helper/
        datamodel-codegen.sh
        getfunctionurlsandsetkeyvaultsecrets.py
    host.json
    local.settings.json
    requirements.txt
    servicebus_funcs.py
    set_environment.py
    tests/
        config.yaml
        config_test.ipynb
        servicebus_funcs.py
        set_environment.py
        test.ipynb
        validate_messages.py
        validate_test.ipynb
        var_funcs.py
    validate_messages.py
    var_funcs.py
```

## Description of code

| **File**                                | **Description**                                                                                                                       |
|-----------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------|
| config.yaml                             | Config file listing variables for dev, preprod and prod environments, global variables and servicebus message entities.               |
| deploy.sh                               | Shell script for manual deployments of the function app. Just comment out the environments you don't need.                            |
| function_app.py                         | The main function app code with all the functions. One function per servicebus topic.                                                 |
| helper/                                 | Folder for other useful code, e.g. the two below.                                                                                     |
| datamodel-codegen.sh                    | Shell script to generate pydantic models from json schemas. Replaced by code in the data-model repo.                                  |
| getfunctionurlsandsetkeyvaultsecrets.py | Code to extract all functions in a given function app and list their urls and put them into keyvault as secrets.                      |
| host.json                               | Mandatory file for function apps.                                                                                                     |
| local.settings.json                     | Mandatory file for function apps.                                                                                                     |
| requirements.txt                        | Required python packages for the function app.                                                                                        |
| servicebus_funcs.py                     | Functions to read servicebus messages and send them to storage. Additional functions needed by the function app can be stored here.   |
| set_environment.py                      | Code to set the environment (dev, preprod, prod) for manual deployments and to load the config file used in the function_app.py code. |
| tests/                                  | Folder for random testing files and unit tests                                                                                        |
| validate_messages.py                    | Functions to validate servicebus messages against a json schema with an ISO-8601 format checker.                                      |
| var_funcs.py                            | Other python variables and functions used as config, e.g. setting current time and date for file paths.                               |

## Process flow

```mermaid

---
title: Function App process flow
---
sequenceDiagram
    Synapse ->> Key Vault: Fetch function url
    Key Vault ->> Synapse: Function url returned
    Synapse ->> Function: Send http GET request
    Function ->> Servicebus: Get messages from Servicebus topic
    Servicebus ->> Function: Messages returned to function
    Function ->> Validate: Messages validated against json schema
    Function ->> Storage account: Messages saved to storage as json file
    Storage account ->> ODW standardised: Raw messages processed to standardised layer
```
## Function app - how it works