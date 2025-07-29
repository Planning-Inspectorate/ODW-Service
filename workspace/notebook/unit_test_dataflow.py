import json
from pyspark.sql import SparkSession
from pyspark.sql.types import StructType
from pyspark.sql import DataFrame

spark = SparkSession.builder.appName("UnitTestDF").getOrCreate()

class TestRunner:
    def __init__(self, configs):
        self.configs = configs

    def run_tests(self):
        for config in self.configs:
            table_name = config['table_name']
            expected_schema = self.get_schema_from_json(config['schema_path'])

            actual_df = spark.table(table_name)
            actual_schema = actual_df.schema

            schema_correct = self.compare_schemas(expected_schema, actual_schema)
            print(f"Schema for {table_name} is {'correct' if schema_correct else 'incorrect'}.")

            for query in config['queries']:
                result = self.run_query(query)
                print(f"Query `{query}` returned {result.count()} rows.")

    @staticmethod
    def get_schema_from_json(path) -> StructType:
        with open(path, 'r') as file:
            schema_dict = json.load(file)
        return StructType.fromJson(schema_dict)

    @staticmethod
    def compare_schemas(expected_schema: StructType, actual_schema: StructType) -> bool:
        return expected_schema == actual_schema

    @staticmethod
    def run_query(sql_query) -> DataFrame:
        return spark.sql(sql_query)


def main():
    configs = [
        {
            "table_name": "odw_harmonised_db.appeal_document",
            "schema_path": "./schemas/appeal_document_schema.json",
            "queries": [
                "SELECT * FROM odw_harmonised_db.appeal_document WHERE IsActive = 'Y'",
                "SELECT COUNT(*) FROM odw_harmonised_db.appeal_document"
            ]
        },
        # Additional configuration for other tables and tests
    ]

    test_runner = TestRunner(configs)
    test_runner.run_tests()


if __name__ == "__main__":
    main()
