# Documentation of the use of Function Apps with ODW  

[High level architecture](#high-level-architecture)  
[Service User process](#service-user-process)  
[DaRT process](#dart-process)  
[Folder structure example](#folder-structure-example)  
[Authorisation flow](#authorisation-flow)  
[DaRT API](#dart-api)
[Timesheet API](#timesheet-api)

## High level architecture  

![architecture](../../images/apim-function-apps.drawio.svg)  

## Key points to note

- All Function Apps will be on a Premium plan (e.g. EP1) to allow VNET integration
- All Function Apps will use the same App Service Plan
- A system assigned managed identity will be created for each Function App
- Azure Key Vault will be used to store API secrets used to call the APIs
- Clients to fetch secrets as needed from Key Vault

## Service User process  
### Goal
Back Office (ODT) wants to send and receive data from ODW via Service Buses. 

### Process
The end-to-end process has been automated as follows.

1. An **Azure Function** will be triggerred whenever the Back Office sends a new message to their **Service bus**. This message is expected to be in json format.
2. **Azure Function** will write this data as a json blob in a **Storage Account** at `odw-raw/Service-Bus/Service-User/{rand-guid}.json`.
3. A Storage Event trigger `tr_odw_raw_service_user` will be fired as a result of this write operation which then will trigger a **Synapse Pipeline** `pln_service_user_main`.
4. This pipeline will process and ingest the new data in Standardised, Harmonised, and Curated layers within the ODW and as a final step, publish the data the ODW **Service Bus** at `service-user` topic.
5. In addition to the new data coming from the Back Office, ODW will also process/host legacy Service User data obtained from **Horizon**. This data is originally present at `odw-raw/Horizon/2023-05-19/CaseInvolvement.csv`.
6. Back Office will be able to subscribe to this topic and consume the processed data.
7. For other entities like NSIP, we will be able to re-use the above process.

### Service User architecture  

![architecture](../../images/service-user-architecture.drawio.svg)

### Key notes
- Make sure the Function App and the Storage Account are in the same VNET to allow communication.
- Make sure that the Azure Data Factory application (search Azure Data Factory in managed identities when doing a role assignment) has the right role assigned (EventGrid EventSubscription Contributor) in the Subscription to be able to publish the trigger.

# DaRT API
### Goal
Back Office (ODT) wants to read data from ODW. An API needs to be provided which reads data from specified SQL tables and returns it to the calling process.

### Process

To simply things, the code exists within the service bus functions **functions/function_app.py** file. This makes deploying and maintaining it easier

```python
@_app.function_name(name="getDaRT")
@_app.route(route="getDaRT", methods=["get"], auth_level=func.AuthLevel.FUNCTION)
@_app.sql_input(arg_name="dart",
                command_text="""
                SELECT *
                FROM odw_curated_db.dbo.dart_api
                WHERE UPPER([applicationReference]) = UPPER(@applicationReference) 
                OR UPPER([caseReference]) = UPPER(@caseReference)
                """,
                command_type="Text",
                parameters="@caseReference={caseReference},@applicationReference={applicationReference}",
                connection_string_setting="SqlConnectionString"
                )
def getDaRT(req: func.HttpRequest, dart: func.SqlRowList) -> func.HttpResponse:
    try:
        rows = []
        for r in dart:
            row = json.loads(r.to_json())
            for key, value in row.items():
                if isinstance(value, str):
                    try:
                        parsed_value = json.loads(value)
                        row[key] = parsed_value
                    except json.JSONDecodeError:
                        row[key] = "Invalid json"
                        print(f"Failed to parse field '{key}': {value}\nError: {e}")
            rows.append(row)
        return func.HttpResponse(
            json.dumps(rows),
            status_code=200,
            mimetype="application/json"
        )
    except Exception as e:
        return func.HttpResponse(f"Unknown error: {str(e)}", status_code=500)
``` 

This function exposes an endpoint which can be called from external applications.

The URL looks a little like this:

```https://<FUNCTION_APP_URL>/api/getDaRT?code=<ACCESS_TOKEN>==&applicationReference=<APPLICATION_REFERENCE>&caseReference=<CASE_REFERENCE>```

```<APPLICATION_REFERENCE>``` is expected to be a string to match against the column applicationReference. The sql_input decorator protects against SQL injection.

```<CASE_REFERENCE>``` is expected to be a string to match against the column caseReference. The sql_input decorator protects against SQL injection.

CORS headers are returned which means that Web UIs from other origins can access the API.


# Timesheet API
### Goal
Back Office (ODT) wants to read data from ODW. An API needs to be provided which reads data from specified SQL tables and returns it to the calling process.

### Process

To simply things, the code exists within the service bus functions **functions/function_app.py** file. This makes deploying and maintaining it easier

```python
@_app.function_name(name="gettimesheets")
@_app.route(route="gettimesheets", methods=["get"], auth_level=func.AuthLevel.FUNCTION)
@_app.sql_input(arg_name="timesheet",
                command_text="SELECT [caseReference], [applicationReference], [siteAddressLine1], [siteAddressLine2], [siteAddressTown], [siteAddressCounty], [siteAddressPostcode] FROM [odw_curated_db].[dbo].[appeal_has] WHERE UPPER([caseReference]) LIKE Concat(Char(37), UPPER(@searchCriteria), Char(37)) OR UPPER([applicationReference]) LIKE Concat(Char(37), UPPER(@searchCriteria), Char(37)) OR UPPER([siteAddressLine1]) LIKE Concat(Char(37), UPPER(@searchCriteria), Char(37)) OR UPPER([siteAddressLine2]) LIKE Concat(Char(37), UPPER(@searchCriteria), Char(37)) OR UPPER([siteAddressTown]) LIKE Concat(Char(37), UPPER(@searchCriteria), Char(37)) OR UPPER([siteAddressCounty]) LIKE Concat(Char(37), UPPER(@searchCriteria), Char(37)) OR UPPER([siteAddressPostcode]) LIKE Concat(Char(37), UPPER(@searchCriteria), Char(37))",
                command_type="Text",
                parameters="@searchCriteria={searchCriteria}",
                connection_string_setting="SqlConnectionString")
def gettimesheets(req: func.HttpRequest, timesheet: func.SqlRowList) -> func.HttpResponse:
    """
    We need to use Char(37) to escape the % 
    https://stackoverflow.com/questions/71914897/how-do-i-use-sql-like-value-operator-with-azure-functions-sql-binding
    """
    try:
        rows = list(map(lambda r: json.loads(r.to_json()), timesheet))
        return func.HttpResponse(
            json.dumps(rows),
            status_code=200,
            mimetype="application/json"
        )
    except Exception as e:
        return (
            func.HttpResponse(f"Unknown error: {str(e)}", status_code=500)
        )
``` 

This function exposes an endpoint which can be called from external applications.

The URL looks a little like this:

```https://<FUNCTION_APP_URL>/api/gettimesheets?code=<ACCESS_TOKEN>==&searchCriteria=<SEARCH CRITERIA>```

```<SEARCH_CRITERIA>``` is expected to be a free text string which is resolved to ```%<SEARCH_CRITERIA>%``` internally and searches across the following columns. The sql_input decorator handles SQL injection protection.

```
[caseReference],
[applicationReference],
[siteAddressLine1],
[siteAddressLine2],
[siteAddressTown],
[siteAddressCounty],
[siteAddressPostcode]
```

CORS headers are returned which means that Web UIs from other origins can access the API.

#### Notes

For now, we use the LIKE and UPPER operands to give a wildcard search. You cannot combine the % operand and the @searchCriteria parameter so we have to work around it by uaing a CONCAT and the Char(37) (which is %) to reproduce this functionality.


To make use of the **sql_input** declarator (which is defined here 
[here](https://learn.microsoft.com/en-us/azure/azure-functions/functions-bindings-azure-sql-input?tabs=isolated-process%2Cnodejs-v4%2Cpython-v2&pivots=programming-language-python)), the requirements.txt has needed to be updated to use a later version of ***azure-functions***
```
azure-identity==1.15.0
azure-functions==1.20.0
azure-servicebus==7.11.4
azure-storage-blob==12.19.0
azure-mgmt-web==7.2.0
azure-keyvault==4.2.0
PyYAML==6.0.1
jsonschema==4.20.0
iso8601==2.1.0
aiohttp==3.9.4
pytest==7.4.0
pytest-asyncio==0.23.3
git+https://github.com/Planning-Inspectorate/data-model@main#egg=pins_data_model
```
If the previous version 1.17.0 was used then the functions app deployed but zero functions were available with no apparent logging as to the cause.

### Functionality
This function simply  makes a query to the curated table [odw_curated_db].[dbo].[s62a] which surfaces the required data. The function app needs to have the right permissions to make these queries which uses a SqlConnectionString variable in the function app configuration

```SqlConnectionString: Server=tcp:<SQL INSTANCE>,1433;Persist Security Info=False;MultipleActiveResultSets=False;Encrypt=True;TrustServerCertificate=False;Database=odw_curated_db;Authentication=Active Directory Managed Identity;",```

The SQL permissions are created in a similar way to [DaRT process](#dart-process)
