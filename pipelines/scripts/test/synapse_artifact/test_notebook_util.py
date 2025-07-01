from pipelines.scripts.synapse_artifact.synapse_artifact_util import SynapseArtifactUtil
from pipelines.scripts.synapse_artifact.synapse_notebook_util import SynapseNotebookUtil
from copy import deepcopy
import mock
from typing import Tuple
import pytest


def test__synapse_notebook_util__replace_env_strings():
    source_env = "dev"
    target_env = "test"
    artifact = {
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
    expected_cleaned_artifact = {
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
    cleaned_artifact = SynapseNotebookUtil("some_workspace").replace_env_strings(deepcopy(artifact), source_env, target_env)
    assert cleaned_artifact == expected_cleaned_artifact


def test__synapse_notebook_util__compare__match():
    artifact = {
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
    # Delete an optional property, which should not affect the comparison if not present
    del artifact["properties"]["metadata"]["a365ComputeOptions"]["automaticScaleJobs"]
    artifact_copy = deepcopy(artifact)
    assert SynapseNotebookUtil("some_workspace").compare(artifact, artifact_copy)


def test__synapse_notebook_util__compare__mismatch():
    artifact = {
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
            "metadata": dict(),
            "cells": {
                "cell_type": "code",
                    "source": [],  # Deleted the code in that cell
                    "execution_count": None
            }
        }
    }
    artifact_copy = {**artifact, **different_attributes}
    assert not SynapseNotebookUtil("some_workspace").compare(artifact, artifact_copy)


def test__synapse_notebook_util__convert_to_python():
    test_notebook = {
        "name": "test_notebook",
        "properties": {
            "cells": [
                {
                    "cell_type": "code",
                    "source": [
                        "%%pyspark"
                    ]
                },
                {
                    "cell_type": "code",
                    "source": [
                        "%run utils/py_utils_get_storage_account"
                    ]
                },
                {
                    "cell_type": "code",
                    "source": [
                        "%run \"utils/py_utils_get_storage_account\""
                    ]
                },
                {
                    "cell_type": "code",
                    "source": [
                        "%run 'utils/py_utils_get_storage_account'"
                    ]
                },
                {
                    "cell_type": "code",
                    "source": [
                        "%run `utils/py_utils_get_storage_account`"
                    ]
                },
                {
                    "cell_type": "markdown",
                    "source": [
                        "Some markdonw text which should be dropped"
                    ]
                },
                {
                    "cell_type": "code",
                    "source": [
                        "from notebookutils import mssparkutils\n",
                        "import re\n",
                        "storage_account=re.search('url=https://(.+?);', mssparkutils.credentials.getFullConnectionString('ls_storage')).group(1)\n",
                        "mssparkutils.notebook.exit(storage_account)"
                    ]
                },
                {
                    "cell_type": "code",
                    "source": [
                        "mssparkutils.notebook.run(\"utils/py_utils_get_storage_account\")"
                    ]
                }
            ]
        }
    }
    expected_python = "\n".join(
        [
            "# %%pyspark",
            "mssparkutils.notebook.run(\"utils/py_utils_get_storage_account\")",
            "mssparkutils.notebook.run(\"utils/py_utils_get_storage_account\")",
            "mssparkutils.notebook.run('utils/py_utils_get_storage_account')",
            "mssparkutils.notebook.run(`utils/py_utils_get_storage_account`)",
            "from notebookutils import mssparkutils",
            "import re",
            "storage_account=re.search('url=https://(.+?);', mssparkutils.credentials.getFullConnectionString('ls_storage')).group(1)",
            "mssparkutils.notebook.exit(storage_account)",
            'mssparkutils.notebook.run("utils/py_utils_get_storage_account")'
        ]
    )
    assert expected_python == SynapseNotebookUtil.convert_to_python(test_notebook)


def test__synapse_notebook_util__get_dependencies_in_notebook_code():
    notebook_code = "\n".join(
        [
            "mssparkutils.notebook.run(\"utils/py_utils_get_storage_account\")",
            "from notebookutils import mssparkutils",
            "import re",
            "storage_account=re.search('url=https://(.+?);', mssparkutils.credentials.getFullConnectionString('ls_storage')).group(1)",
            "mssparkutils.notebook.exit(storage_account)",
            'mssparkutils.notebook.run("utils/py_utils_get_storage_account")',
            "run(\"something\")"  # This is not associated with the mssparkutils run function, so should not be picked up as a dependency
        ]
    )
    dependencies = SynapseNotebookUtil.get_dependencies_in_notebook_code(notebook_code)
    expected_dependencies = {"notebook/py_utils_get_storage_account.json", "linkedService/ls_storage.json"}
    assert expected_dependencies == dependencies


def test__synapse_notebook_util__dependent_artifacts():
    some_artifact = {
        "name": "some_notebook"
    }
    with mock.patch.object(SynapseNotebookUtil, "get_dependencies_in_notebook_code", return_value={"some_notebook_code_dependency"}):
        with mock.patch.object(SynapseNotebookUtil, "convert_to_python", return_value="some notebook code"):
            with mock.patch.object(SynapseArtifactUtil, "dependent_artifacts", return_value={"some_notebook_dependency"}):
                expected_return_value = {"some_notebook_code_dependency", "some_notebook_dependency"}
                actual_return_value = SynapseNotebookUtil.dependent_artifacts(some_artifact)
                assert expected_return_value == actual_return_value
                SynapseNotebookUtil.get_dependencies_in_notebook_code.assert_called_once_with("some notebook code")
