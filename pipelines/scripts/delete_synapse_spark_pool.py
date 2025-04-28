from pipelines.scripts.synapse_artifact.synapse_spark_pool_util import SynapseSparkPoolUtil
import argparse


if __name__ == "__main__":
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("-sw", "--synapse_workspace", help="The synapse workspace to check against")
    parser.add_argument("-pn", "--pool_name", help="The name of the pool to delete")
    args = parser.parse_args()
    synapse_workspace = args.synapse_workspace
    pool_name = args.pool_name
    SynapseSparkPoolUtil(synapse_workspace).delete(pool_name)
