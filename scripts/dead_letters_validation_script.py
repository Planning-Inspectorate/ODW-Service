import json  # Used to parse the JSON content from the 'body' column
import pandas as pd  # pandas is used to read and write Excel files
from jsonschema import (
    validate,
    ValidationError
  )  # For validating JSON against schema

# JSON Schema: Describes what each JSON body must contain
# Fields in "required" must exist and not be null
SCHEMA = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "$id": "nsip-document.schema.json",
    "title": "NSIP Document",
    "type": "object",
    "additionalProperties": True,
    "required": [
        "documentId", "caseId", "caseRef", "documentReference", "version",
        "examinationRefNo", "filename", "originalFilename", "size", "mime",
        "documentURI", "publishedDocumentURI", "path", "virusCheckStatus",
        "fileMD5", "dateCreated", "lastModified", "caseType", "redactedStatus",
        "publishedStatus", "datePublished", "documentType",
        "securityClassification", "sourceSystem", "origin", "owner", "author",
        "representative", "description", "documentCaseStage", "filter1",
        "filter2", "horizonFolderId", "transcriptId"
    ],
    "properties": {
        "documentId": {"type": "string"},
        "caseId": {"type": ["integer", "null"]},
        "caseRef": {"type": ["string", "null"]},
        "documentReference": {"type": ["string", "null"]},
        "version": {"type": "integer"},
        "examinationRefNo": {"type": ["string", "null"]},
        "filename": {"type": "string"},
        "originalFilename": {"type": "string"},
        "size": {"type": "integer"},
        "mime": {"type": ["string", "null"]},
        "documentURI": {"type": "string"},
        "publishedDocumentURI": {"type": ["string", "null"]},
        "path": {"type": ["string", "null"]},
        "virusCheckStatus": {"type": ["string", "null"]},
        "fileMD5": {"type": ["string", "null"]},
        "dateCreated": {"type": "string", "format": "date-time"},
        "lastModified": {"type": ["string", "null"], "format": "date-time"},
        "caseType": {"type": ["string", "null"]},
        "redactedStatus": {"type": ["string", "null"]},
        "publishedStatus": {"type": ["string", "null"]},
        "datePublished": {"type": ["string", "null"], "format": "date-time"},
        "documentType": {"type": ["string", "null"]},
        "securityClassification": {"type": ["string", "null"]},
        "sourceSystem": {"type": ["string", "null"]},
        "origin": {"type": ["string", "null"]},
        "owner": {"type": ["string", "null"]},
        "author": {"type": ["string", "null"]},
        "representative": {"type": ["string", "null"]},
        "description": {"type": ["string", "null"]},
        "documentCaseStage": {"type": ["string", "null"]},
        "filter1": {"type": ["string", "null"]},
        "filter2": {"type": ["string", "null"]},
        "horizonFolderId": {"type": ["string", "null"]},
        "transcriptId": {"type": ["string", "null"]}
    }
}


def validate_json_body(body_text: str, schema: dict,
                       required_fields: list[str]) -> tuple[str, str]:
    """
    Validate a single 'body' value (string) against the schema.

    Returns:
    - ("yes", "n/a") if valid
    - ("no", <reason>) if invalid (missing fields, invalid format, etc.)
    """
    try:
        # Attempt to parse the string into a Python dict
        data = json.loads(body_text)
    except json.JSONDecodeError:
        return "no", "Invalid JSON"

    # Check required fields are present and not null
    missing = [
        field for field in required_fields
        if field not in data or data[field] is None
    ]
    if missing:
        return "no", f"Missing/null (required): {', '.join(missing)}"

    try:
        # Try to validate JSON structure against the full schema
        validate(instance=data, schema=schema)
        return "yes", "n/a"
    except ValidationError as e:
        # Specific JSON schema validation failed
        return "no", f"Validation error: {e.message}"
    except Exception as e:
        # Catch-all for anything else that could go wrong
        return "no", f"Unexpected error: {str(e)}"


def validate_excel_file(
        input_path: str,
        output_path: str
          ) -> None:
    """
    Reads Excel, validates 'body' column row-by-row, writes result.

    Args:
    - input_path: path to the input Excel file
    - output_path: where the output (with new columns) will be written
    """
    # Read the Excel file into a pandas DataFrame
    df = pd.read_excel(input_path, engine='openpyxl')

    # Extract required fields list from the schema
    required_fields = SCHEMA.get("required", [])

    # Apply validation to every row's 'body' field
    results = df['body'].apply(
        lambda b: validate_json_body(b, SCHEMA, required_fields)
    )

    # Split result tuples into two new columns
    df[['schemaMatch?', 'schemaMismatchReason']] = pd.DataFrame(
        results.tolist(), index=df.index
    )

    # Save the updated DataFrame back to Excel
    df.to_excel(output_path, index=False, engine='openpyxl')

    # Print summary stats
    total = len(df)
    passes = (df['schemaMatch?'] == 'yes').sum()
    fails = total - passes
    print(f"PASSED: {passes}/{total}")
    print(f"FAILED: {fails}/{total}")
    print(f"PASS RATE: {round((passes / total) * 100, 2)}%")


# Select the corresponding input and output paths for files
if __name__ == "__main__":
    validate_excel_file(
        input_path="scripts/nsip-document-messages.xlsx",
        output_path="dead_letters_validated.xlsx"
    )
