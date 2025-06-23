------------------------------------------------------------
-- Initialise Azure Purview permissions
------------------------------------------------------------
USE ODW_HARMONISED_DB

IF NOT EXISTS 
    (SELECT name  
     FROM sys.server_principals
     WHERE name = 'pins-pview')
BEGIN
    CREATE USER [pins-pview] FOR LOGIN [pins-pview];
END
ALTER ROLE db_datareader ADD MEMBER [pins-pview];

------------------------------------------------------------
-- Initialise Azure Functions permissions
------------------------------------------------------------
IF NOT EXISTS 
    (SELECT name  
     FROM sys.server_principals
     WHERE name = 'pins-fnapp01-odw-{ENV}-uks')
BEGIN
    CREATE USER [pins-fnapp01-odw-{ENV}-uks] FOR LOGIN [pins-fnapp01-odw-{ENV}-uks];
END
ALTER ROLE db_datareader ADD MEMBER [pins-fnapp01-odw-{ENV}-uks];
