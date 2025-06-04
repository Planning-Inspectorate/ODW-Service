from pipelines.scripts.synapse_artifact.synapse_artifact_util import SynapseArtifactUtil
import pytest
from copy import deepcopy


@pytest.mark.parametrize(
    "test_case",
    [
        ("a", 1),
        ("b", 2),
        ("c", [3, 4]),
        ("c.0", 3),
        ("c.1", 4),
        ("d.0.0", 5),
        ("e.0.f", 6),
        ("g.h", 7),
        ("g.i.j", 8)
    ]
)
def test_synapse_artifact_util__extract_dictionary_value_by_attribute(test_case):
    artifact = {
        "a": 1,
        "b": 2,
        "c": [
            3,
            4
        ],
        "d": [
            [
                5
            ]
        ],
        "e": [
            {
                "f": 6
            }
        ],
        "g": {
            "h": 7,
            "i": {
                "j": 8
            }
        }
    }
    attribute_string = test_case[0]
    expected_value = test_case[1]
    assert SynapseArtifactUtil._extract_dictionary_value_by_attribute(artifact, attribute_string) == expected_value


@pytest.mark.parametrize(
    "test_case",
    [
        ("a", "Jean-Luc Picard", {"a": "Jean-Luc Picard"}),
        ("b", "James T Kirk", {"b": "James T Kirk"}),
        ("c", 42, {"c": 42}),
        ("c.0", 42, {"c": [42, 4]}),
        ("c.1", 42, {"c": [3, 42]}),
        ("d.0", 10, {"d": [10]}),
        ("e.0.f", "bob", {"e": [{"f": "bob"}]}),
        ("g.h", 66, {"g": {"h": 66, "i": {"j": 8}}}),
        ("g.i.j", None, {"g": {"h": 7, "i": {"j": None}}})
    ]
)
def test_synapse_artifact_util__set_dictionary_value_by_attribute(test_case):
    artifact = {
        "a": 1,
        "b": 2,
        "c": [
            3,
            4
        ],
        "d": [
            [
                5
            ]
        ],
        "e": [
            {
                "f": 6
            }
        ],
        "g": {
            "h": 7,
            "i": {
                "j": 8
            }
        }
    }
    attribute_string = test_case[0]
    new_value = test_case[1]
    new_artifact_properties = test_case[2]
    expected_artifact = {**artifact, **new_artifact_properties}
    artifact_copy = deepcopy(artifact)
    assert SynapseArtifactUtil._set_dictionary_value_by_attribute(artifact_copy, attribute_string, new_value) == expected_artifact
