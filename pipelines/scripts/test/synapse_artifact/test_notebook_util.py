from pipelines.scripts.synapse_artifact.synapse_notebook_util import SynapseNotebookUtil
import pytest
from copy import deepcopy


def test__synapse_notebook_util__replace_env_strings():
    source_env = "dev"
    target_env = "test"
    notebook = {
        "name": "test_notebook",
        "properties": {
            "metadata": {
                "a365ComputeOptions": {
                    "id": "/subscriptions/ff442a29-fc06-4a13-8e3e-65fd5da513b3/resourceGroups/pins-rg-data-odw-dev-uks/providers/Microsoft.Synapse/workspaces/pins-synw-odw-dev-uks/bigDataPools/pinssynspodw34",
                    "name": "pinssynspodw34",
                    "type": "Spark",
                    "endpoint": "https://pins-synw-odw-dev-uks.dev.azuresynapse.net/livyApi/versions/2019-11-01-preview/sparkPools/pinssynspodw34",
                    "auth": {
                        "type": "AAD",
                        "authResource": "https://dev.azuresynapse.net"
                    },
                    "sparkVersion": "3.4",
                    "nodeCount": 3,
                    "cores": 4,
                    "memory": 32,
                    "automaticScaleJobs": True
                },
                "sessionKeepAliveTimeout": 30
            },
            "cells": []
        }
    }
    expected_cleaned_notebook = {
        "name": "test_notebook",
        "properties": {
            "metadata": {
                "a365ComputeOptions": {
                    "id": f"/subscriptions/ff442a29-fc06-4a13-8e3e-65fd5da513b3/resourceGroups/pins-rg-data-odw-{target_env}-uks/providers/Microsoft.Synapse/workspaces/pins-synw-odw-{target_env}-uks/bigDataPools/pinssynspodw34",
                    "name": "pinssynspodw34",
                    "type": "Spark",
                    "endpoint": f"https://pins-synw-odw-{target_env}-uks.dev.azuresynapse.net/livyApi/versions/2019-11-01-preview/sparkPools/pinssynspodw34",
                    "auth": {
                        "type": "AAD",
                        "authResource": "https://dev.azuresynapse.net"
                    },
                    "sparkVersion": "3.4",
                    "nodeCount": 3,
                    "cores": 4,
                    "memory": 32,
                    "automaticScaleJobs": True
                },
                "sessionKeepAliveTimeout": 30
            },
            "cells": []
        }
    }
    cleaned_notebook = SynapseNotebookUtil("some_workspace").replace_env_strings(deepcopy(notebook), source_env, target_env)
    assert cleaned_notebook == expected_cleaned_notebook


def test__synapse_notebook_util__compare__match():
    notebook = {
        "name": "test_notebook",
        "properties": {
            "nbformat": 4,
            "nbformat_minor": 2,
            "bigDataPool": {
                "referenceName": "pinssynspodw34",
                "type": "BigDataPoolReference"
            },
            "sessionProperties": {
                "driverMemory": "28g",
                "driverCores": 4,
                "executorMemory": "28g",
                "executorCores": 4,
                "numExecutors": 6,
                "runAsWorkspaceSystemIdentity": False,
                "conf": {
                    "spark.dynamicAllocation.enabled": "false",
                    "spark.dynamicAllocation.minExecutors": "6",
                    "spark.dynamicAllocation.maxExecutors": "6",
                    "spark.autotune.trackingId": "8cf39d03-133b-4711-a415-1dd8f7505f69"
                }
            },
            "metadata": {
                "saveOutput": True,
                "enableDebugMode": False,
                "kernelspec": {
                    "name": "synapse_pyspark",
                    "display_name": "Synapse PySpark"
                },
                "language_info": {
                    "name": "python"
                },
                "a365ComputeOptions": {
                    "id": "/subscriptions/ff442a29-fc06-4a13-8e3e-65fd5da513b3/resourceGroups/pins-rg-data-odw-dev-uks/providers/Microsoft.Synapse/workspaces/pins-synw-odw-dev-uks/bigDataPools/pinssynspodw34",
                    "name": "pinssynspodw34",
                    "type": "Spark",
                    "endpoint": "https://pins-synw-odw-dev-uks.dev.azuresynapse.net/livyApi/versions/2019-11-01-preview/sparkPools/pinssynspodw34",
                    "auth": {
                        "type": "AAD",
                        "authResource": "https://dev.azuresynapse.net"
                    },
                    "sparkVersion": "3.4",
                    "nodeCount": 3,
                    "cores": 4,
                    "memory": 32,
                    "automaticScaleJobs": True
                },
                "sessionKeepAliveTimeout": 30
            },
            "cells": [
                {
                    "cell_type": "code",
                    "source": [
                        "from notebookutils import mssparkutils\r\n",
                        "\r\n",
                        "timeout_in_seconds = 60 * 30\r\n",
                        "\r\n",
                    ],
                    "execution_count": None
                }
            ]
        }
    }
    notebook_copy = deepcopy(notebook)
    assert SynapseNotebookUtil("some_workspace").compare(notebook, notebook_copy)


def test__synapse_notebook_util__compare__mismatch():
    notebook = {
        "name": "test_notebook",
        "properties": {
            "nbformat": 4,
            "nbformat_minor": 2,
            "bigDataPool": {
                "referenceName": "pinssynspodw34",
                "type": "BigDataPoolReference"
            },
            "sessionProperties": {
                "driverMemory": "28g",
                "driverCores": 4,
                "executorMemory": "28g",
                "executorCores": 4,
                "numExecutors": 6,
                "runAsWorkspaceSystemIdentity": False,
                "conf": {
                    "spark.dynamicAllocation.enabled": "false",
                    "spark.dynamicAllocation.minExecutors": "6",
                    "spark.dynamicAllocation.maxExecutors": "6",
                    "spark.autotune.trackingId": "8cf39d03-133b-4711-a415-1dd8f7505f69"
                }
            },
            "metadata": {
                "saveOutput": True,
                "enableDebugMode": False,
                "kernelspec": {
                    "name": "synapse_pyspark",
                    "display_name": "Synapse PySpark"
                },
                "language_info": {
                    "name": "python"
                },
                "a365ComputeOptions": {
                    "id": "/subscriptions/ff442a29-fc06-4a13-8e3e-65fd5da513b3/resourceGroups/pins-rg-data-odw-dev-uks/providers/Microsoft.Synapse/workspaces/pins-synw-odw-dev-uks/bigDataPools/pinssynspodw34",
                    "name": "pinssynspodw34",
                    "type": "Spark",
                    "endpoint": "https://pins-synw-odw-dev-uks.dev.azuresynapse.net/livyApi/versions/2019-11-01-preview/sparkPools/pinssynspodw34",
                    "auth": {
                        "type": "AAD",
                        "authResource": "https://dev.azuresynapse.net"
                    },
                    "sparkVersion": "3.4",
                    "nodeCount": 3,
                    "cores": 4,
                    "memory": 32,
                    "automaticScaleJobs": True
                },
                "sessionKeepAliveTimeout": 30
            },
            "cells": [
                {
                    "cell_type": "code",
                    "source": [
                        "from notebookutils import mssparkutils\r\n",
                        "\r\n",
                        "timeout_in_seconds = 60 * 30\r\n",
                        "\r\n",
                    ],
                    "execution_count": None
                }
            ]
        }
    }
    different_attributes = {
        "properties": {
            "cells": {
                "cell_type": "code",
                    "source": [],  # Deleted the code in that cell
                    "execution_count": None
            }
        }
    }
    notebook_copy = {**notebook, **different_attributes}
    assert not SynapseNotebookUtil("some_workspace").compare(notebook, notebook_copy)
