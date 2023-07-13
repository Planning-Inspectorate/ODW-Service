# PINS Azure Logic App process  

## Purpose

Azure Logic Apps are being used to schedule regular extracts of data from the Zendesk Ticket API for further processing and consumption by downstream systems and consumers.  

## Options

1. Built-in Zendesk connector - out of the box ith Logic Apps
2. Custom connector - build a custom connector ourselves

![Zendesk built-in connector](/images/zendesk-built-in.jpg "Zendesk built-in connector")  

![Zendesk custom connector](/images/zendesk-custom.jpg "Zendesk custom connector")  

Zendesk built-in connector - [Zendesk](https://learn.microsoft.com/en-us/connectors/zendesk/)  

Creating a custom connector - [Custom connector](https://learn.microsoft.com/en-us/connectors/custom-connectors/create-logic-apps-connector)  

Example of custom connector Open API definition  

```yaml
openapi: 3.0.1
info:
  title: Zendesk custom API
  description: Custom API for Zendesk
  version: "0.1"
servers:
- url: https://pinssupport.zendesk.com
```  

## Limitations of the built-in Zendesk connector

Taken from the documentation here - [Zendesk connector limitations](https://learn.microsoft.com/en-us/connectors/zendesk/)  

>Connector returns only atomic properties of Zendesk entity (i.e. lists, records and other complex types are not supported). For instance, Ticket entity has tags property represented by array on Zendesk's side. Zendesk connector returns [List] string for such fields.
>
>Connector requires updated_at column to exist for any table that is used with triggers.
>
>Zendesk Search API has a limitation on returning 1000 results per query. This affects some connector actions, that would fail with an error ("Http request failed: the content was not a valid JSON") if target table contains 1000 records or more:

Below is an example of the missing array values returned by the built-in connector.  

```json
{
  "tags": [List]
}
```

Rather than complete data, which would be more useful, like below.  

```json
{
  "tags": [
          "tag_value_1",
          "tag_value_2",
          "tag_value_3"
          ]
}
```

**Solution = Custom Connector**  

## Process to build a custom connector

Step 1: Create a new custom connector resource in the subscription. Guidance can be followed here - [Custom connector](https://learn.microsoft.com/en-us/connectors/custom-connectors/create-logic-apps-connector)

Step 2: Define the custom connector.

There are two main methods to define a custom connector to be used by Logic Apps (and Power Automate).  

1. [Import Postman Collection](https://learn.microsoft.com/en-us/connectors/custom-connectors/define-postman-collection)
2. [Import Open API definition file](https://learn.microsoft.com/en-us/connectors/custom-connectors/define-openapi-definition)  

In the Azure portal, after clicking on the newly created Logic APp custom connector resource, you can click on edit and see this screen below.  

![Edit custom connector](/images/edit-custom-connector.png "Edit custom connector")  

### Import Postman Collection

The full Zendesk public API can be viewed online in Postman here - [Postman Zendesk API](https://www.postman.com/zendesk-redback/workspace/zendesk-public-api/overview).  

The Zendesk documentation also contains this guidance - [Exploring Zendesk with Postman](https://developer.zendesk.com/documentation/api-basics/working-with-the-zendesk-apis/exploring-zendesk-apis-with-postman/)  

**NB: The concept of Postman, creating collections and how to test API requests in general is out of the scope of this documentation.**  

There are 2 main issues with using a Postman collection for this purpose:

1. The collection file size is limited to 1MB. This is quite small and means cropping the collection to the bare minimum for what you need. It wasn't a huge issue here but an awkward process and for the full Zendesk API to be utilised we'd have to have multiple small collections which would be a bit of work to achieve initially and possibly hard to update.

2. When importing the collection into the custom connector, it attempted to convert the .json file into a swagger definition. It wasn't able to achieve this very well and led to various formatting errors that were hard to understand and fix in the UI itself.  

For those reasons the Open API definition file was the best and easier option to go with.  

### Import Open API definition file

Some useful guidance at the following sites:

[Basic structure](https://swagger.io/docs/specification/basic-structure/)  
[Getting started with Open API](https://learn.openapis.org/)  
[Open API specification - Github](https://github.com/OAI/OpenAPI-Specification/)  
[Swggerhub - tool to help to build an API](https://app.swaggerhub.com/home)  
[Swagger Inspect (soon replaced by Explore)](https://inspector.swagger.io/builder)  

There is a lot of documentation online and many tools to help with creating an API definition but the ones listed above are what I have used. The alternative is to just write the definition yourself if you're comfortable doing that. A sample of the definition file is shown below.  

```yaml
openapi: 3.0.1
info:
  title: Zendesk custom API
  description: Custom API for Zendesk
  version: "0.1"
servers:
- url: https://pinssupport.zendesk.com
paths:
  /api/v2/tickets/{ticket_id}/related:
    get:
      description: Call to get related tickets
      summary: Get related tickets
      operationId: GetRelatedTickets
      parameters:
      - name: ticket_id
        in: path
        description: The ticket id if you want a specific ticket
        required: true
        style: simple
        explode: false
        schema:
          type: integer
      responses:
        "200":
          description: Auto generated using Swagger Inspector
          content:
            application/json; charset=utf-8:
              schema:
                type: string
              examples: {}
      servers:
      - url: https://pinssupport.zendesk.com
    servers:
    - url: https://pinssupport.zendesk.com
```

In order to create this file I used Swagger Inspect which is a tool that allows you to create http requests and view the results. The requests you make can then be added to a collection and grouped together and then used to create an Open API definition. This is a quick way to get a sample file structure in place which you cna add to at a later date.  

![Swagger Inspector](/images/swagger-inspector.png "Swagger Inspector")  

The API can then be viewed in Swaggerhub as below.  

![Swaggerhub](/images/swaggerhub.png "Swaggerhub")  

Once confortable with what's required the file can then be edited directly in VS Code or elsewhere and version controlled.  

The Logic App Custom Connector can recognise this file without any issues so it can be used in Logic App workflows.  

### Defining the trigger for Logic App workflow

Logic App workflows require a trigger to determine what event causes the workflow to run. Our trigger in this case is defined in the Open API definition as follows:  

```yaml
  /api/v2/search.json:
    get:
      responses:
        "200":
          description: OK
          content:
            application/json; charset=utf-8:
              schema:
                type: string
              examples: {}
      summary: Triggers when a new ticket is created
      description: Triggers when a new ticket is created
      operationId: OnNewTicket
      x-ms-trigger: batch
      x-ms-trigger-metadata:
        mode: polling
        kind: query
      x-ms-trigger-hint: New ticket trigger
      parameters:
        - name: query
          in: query
          required: false
          allowReserved: true
          schema:
            type: string
            default: '?query=type:ticket created_at>1hour order_by:created_at sort:desc'
          description: Search query for latest tickets
          x-ms-visibility: none
```

