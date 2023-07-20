# Standards for ingesting data from external APIs into ODW RAW layer

1. Create linked service to source data
2. Create source dataset based on linked service, specifying relative url and parameters  
3. Create Synapse pipeline using Copy data task using source dataset and specifying pagination rules  
4. Specify sink and if need be create sink dataset which uses a linked service, e.g. ls_storage if the sink is our storage account  
5. In sink, specify file pattern, e.g. array of objects for json responses  
