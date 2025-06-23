from pipelines.scripts.util import Util
import argparse
import logging
from dotenv import load_dotenv
import os


load_dotenv(verbose=True)

logging.basicConfig(level=logging.INFO)


SQL_SCRIPTS_TO_RUN = [
    "initialiseMasterDBRoles",
    "initialiseConfigDB",
    "initialiseStandardisedDB",
    "initialiseHarmonisedDB",
    "initialiseCuratedDB"
]

CONFIG = {
    "ENV": os.environ.get("ENV", None)
}


def load_sql_script(sql_script_path: str) -> str:
    with open(sql_script_path, "r") as f:
        sql = f.read()
    for k, v in CONFIG.items():
        sql = sql.replace("{" + k + "}", v)
    return sql


def initialise(env: str):
    for script in SQL_SCRIPTS_TO_RUN:
        sql_script_path = f"pipelines/scripts/sql_scripts/{script}.sql"
        sql_query = load_sql_script(sql_script_path)
        logging.info(f"Running sql script '{sql_script_path}'")
        connection = Util.get_synapse_sql_pool_connection(env)
        Util.submit_sql(connection, sql_query)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("-e", "--env", help="The environment to initialise")
    args = parser.parse_args()
    env = args.env
    initialise(env)
