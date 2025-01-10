# Documentation of the use of Function Apps with ODW  

[High level architecture](#high-level-architecture)  
[Service User process](#service-user-process)  
[DaRT API](#dart-api)  
[Timesheet API](#timesheet-api)  

## High level architecture  

![architecture](../../images/function-apps.drawio.svg)  

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


