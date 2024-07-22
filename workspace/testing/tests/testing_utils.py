import json
from pyspark.sql.types import *
from pyspark.sql import DataFrame
import pprint

storage_account: str = mssparkutils.notebook.run('/utils/py_utils_get_storage_account')
path_to_orchestration_file: str = "abfss://odw-config@"+storage_account+"orchestration/orchestration.json"

def get_incremental_key(entity_name: str, storage_account: str, path_to_orchestration_file: str) -> str:
    # getting the incremental key from the odw-config/orchestration
    df: DataFrame = spark.read.option("multiline","true").json(path_to_orchestration_file)
    definitions: list = json.loads(df.toJSON().first())['definitions']
    definition: dict = next((d for d in definitions if entity_name == d['Source_Filename_Start']), None)
    return definition['Harmonised_Incremental_Key'] if definition and 'Harmonised_Incremental_Key' in definition else None

def create_spark_schema(db_name: str, entity_name: str) -> StructType:
    incremental_key: str = get_incremental_key(entity_name, storage_account, path_to_orchestration_file) if db_name == 'odw_harmonised_db' else None
    schema = mssparkutils.notebook.run("/py_create_spark_schema", 30, {"db_name": db_name, "entity_name": entity_name, "incremental_key": incremental_key})
    spark_schema = StructType.fromJson(json.loads(schema))
    return spark_schema

def create_spark_dataframe() -> DataFrame:
    spark_dataframe: DataFrame = spark.createDataFrame([], schema=create_spark_schema(db_name, entity_name))
    return spark_dataframe

def extract_schema_structure(schema: StructType) -> dict:
    def extract_field(field):
        if isinstance(field.dataType, StructType):
            return {field.name: {subfield.name: str(subfield.dataType) for subfield in field.dataType.fields}}
        elif isinstance(field.dataType, ArrayType):
            element_type = field.dataType.elementType
            if isinstance(element_type, StructType):
                return {field.name: {subfield.name: str(subfield.dataType) for subfield in element_type.fields}}
            else:
                return {field.name: f'array<{str(element_type)}>'}
        else:
            return {field.name: str(field.dataType)}
    
    result = {}
    for field in schema.fields:
        result.update(extract_field(field))
    return result

def test_compare_schemas(schema1: StructType, schema2: StructType) -> bool:
    structure1: dict = extract_schema_structure(schema1)
    structure2: dict = extract_schema_structure(schema2)
    
    differences: list[tuple] = []
    
    all_fields: set = set(structure1.keys()).union(set(structure2.keys()))
    
    for field in all_fields:
        if field not in structure1:
            differences.append((field, "Field not in schema1", structure2[field]))
        elif field not in structure2:
            differences.append((field, structure1[field], "Field not in schema2"))
        else:
            if structure1[field] != structure2[field]:
                if isinstance(structure1[field], dict) and isinstance(structure2[field], dict):
                    subfields: set = set(structure1[field].keys()).union(set(structure2[field].keys()))
                    for subfield in subfields:
                        if subfield not in structure1[field]:
                            differences.append((f"{field}.{subfield}", "Field not in schema1", structure2[field][subfield]))
                        elif subfield not in structure2[field]:
                            differences.append((f"{field}.{subfield}", structure1[field][subfield], "Field not in schema2"))
                        elif structure1[field][subfield] != structure2[field][subfield]:
                            differences.append((f"{field}.{subfield}", structure1[field][subfield], structure2[field][subfield]))
                else:
                    differences.append((field, structure1[field], structure2[field]))
    
    if differences:
        # Create a Spark DataFrame to display the differences
        differences_df: DataFrame = spark.createDataFrame(differences, ["Field", "Schema 1", "Schema 2"])
        display(differences_df)
        return False
    else:
        return True
    
def test_std_same_rows_hrm(std_table: str, hrm_table: str) -> tuple[int, int, bool]:
    std_table_full: str = f"{std_db_name}.{std_table}"
    hrm_table_full: str = f"{hrm_db_name}.{hrm_table}"
    std_count: int = spark.table(std_table_full).count()
    hrm_count: int = spark.table(hrm_table_full).count()
    return (std_count, hrm_count, std_count == hrm_count)

def test_curated_row_count(hrm_table_final: str, curated_table: str) -> tuple[int, int, bool]:
    hrm_table_full: str = f"{hrm_db_name}.{hrm_table_final}"
    curated_table_full: str = f"{curated_db_name}.{curated_table_name}"
    hrm_count: int = spark.sql(f"select * from {hrm_table_full} where IsActive = 'Y'").count()
    curated_count: int = spark.table(curated_table_full).count()
    return (hrm_count, curated_count, hrm_count == curated_count)