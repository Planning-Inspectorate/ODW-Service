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



