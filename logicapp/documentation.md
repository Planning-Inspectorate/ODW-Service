# PINS Azure Logic App process  

## Purpose

Azure Logic Apps are being used to schedule regular extracts of data from the Zendesk Ticket API for further processing and consumption by downstream systems and consumers.  

## Options

1. Built-in Zendesk connector - out of the box ith Logic Apps
2. Custom connector - build a custom connector ourselves

![Zendesk built-in connector](/images/zendesk-built-in.jpg "Zendesk built-in connector")  

![Zendesk custom connector](/images/zendesk-custom.jpg "Zendesk custom connector")  

Zendesk built-in connector - **[Zendesk](https://learn.microsoft.com/en-us/connectors/zendesk/)**  

Creating a custom connector - **[Custom connector](https://learn.microsoft.com/en-us/connectors/custom-connectors/define-openapi-definition)**  

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

Taken from the documentation here - **[Zendesk connector limitations](https://learn.microsoft.com/en-us/connectors/zendesk/)**  

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

Step 1: Create a new custom connector resource in the subscription.  

Step 2: Define the custom connector.

There are two main methods to define a custom connector to be used by Logic Apps (and Power Automate).  

1. Import Postman Collection
2. Import Open API definition file


