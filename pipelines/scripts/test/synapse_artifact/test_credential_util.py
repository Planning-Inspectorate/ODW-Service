from pipelines.scripts.synapse_artifact.synapse_credential_util import SynapseCredentialUtil
from copy import deepcopy


def test__synapse_credential_util__compare__match():
    credential = {
        "name": "WorkspaceSystemIdentity",
        "properties": {
            "type": "ManagedIdentity"
        }
    }
    credential_copy = deepcopy(credential)
    assert SynapseCredentialUtil("some_workspace").compare(credential, credential_copy)


def test__synapse_credential_util__compare__mismatch():
    credential = {
        "name": "WorkspaceSystemIdentity",
        "properties": {
            "type": "ManagedIdentity"
        }
    }
    different_attributes = {
        "properties": {
            "description": "some description"
        }
    }
    credential_copy = {**credential, **different_attributes}
    assert not SynapseCredentialUtil("some_workspace").compare(credential, credential_copy)
