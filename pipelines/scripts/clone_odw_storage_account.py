from pipelines.scripts.storage_util import StorageUtil
import argparse


PATHS_TO_IGNORE = {
    "synapse/synapse"
}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("-s", "--source", help="The source storage account to copy from")
    parser.add_argument("-t", "--target", help="The source storage account to copy to")
    args = parser.parse_args()
    source = args.source
    target = args.target
    storage_util = StorageUtil().migrate_between_storage_accounts(source, target, PATHS_TO_IGNORE)
