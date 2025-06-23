------------------------------------------------------------
-- Initialise Azure Purview permissions
------------------------------------------------------------
USE ODW_CONFIG_DB

IF NOT EXISTS 
    (SELECT name  
     FROM sys.server_principals
     WHERE name = 'pins-pview')
BEGIN
    CREATE USER [pins-pview] FOR LOGIN [pins-pview];
END
ALTER ROLE db_datareader ADD MEMBER [pins-pview];
