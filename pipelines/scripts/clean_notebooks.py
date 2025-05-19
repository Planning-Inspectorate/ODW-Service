from pipelines.scripts.util import Util
import json
from typing import List, Dict, Any
import logging


"""
    Clean all notebooks in the local synapse workspace
    Run using `python3 pipelines/scripts/clean_notebooks.py`
    This can be used to cleanup any issues raised by `pipelines/scripts/check_notebooks_valid.py`
"""

logging.basicConfig(level=logging.INFO)


def clean_notebook(notebook: Dict[str, Any]) -> bool:
    """
        Clean the given synapse notebook

        :param notebook: The notebook json to clean
        :return: `True` if the notebook had any of its properties cleaned, `False` otherwise
    """
    modified_attribute = False
    for cell in notebook["properties"]["cell"]:
        if "execution_count" in cell:
            if cell["execution_count"] is not None:
                cell["execution_count"] = None
                modified_attribute = True
    return modified_attribute


def clean_notebooks(notebooks_to_clean: List[str]):
    """
        Clean all of the given notebooks

        :param notebooks_to_clean: The list of notebook paths to clean
    """
    for notebook_path in notebooks_to_clean:
        logging.info(f"Cleaning notebook '{notebook_path}'")
        notebook = json.load(open(notebook_path))
        cleaned_notebook = clean_notebook(notebook)
        if cleaned_notebook:
            logging.info("    Some properties of this notebook have been cleaned")
        with open(notebook_path, "w") as f:
            json.dump(notebook, f, indent="\t", ensure_ascii=False)


if __name__ == "__main__":
    clean_notebooks(Util.get_all_artifact_paths(["workspace/notebook"]))
