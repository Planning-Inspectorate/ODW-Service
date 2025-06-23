USE MASTER

------------------------------------------------------------
-- Initialise Azure Purview user
------------------------------------------------------------

BEGIN TRY
    CREATE LOGIN [pins-pview] FROM EXTERNAL PROVIDER;
END TRY
BEGIN CATCH
    SELECT 'The login pins-pview already exists' AS Messages
END CATCH

------------------------------------------------------------
-- Initialise Azure Functions user
------------------------------------------------------------

BEGIN TRY
    CREATE LOGIN [pins-fnapp01-odw-{ENV}-uks] FROM EXTERNAL PROVIDER;
END TRY
BEGIN CATCH
    SELECT 'The login pins-fnapp01-odw-{ENV}-uks already exists' AS Messages
END CATCH
