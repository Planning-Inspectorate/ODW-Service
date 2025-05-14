from pipelines.scripts.private_endpoint.synapse_private_endpoint_manager import SynapsePrivateEndpointManager
from pipelines.scripts.util import Util
import argparse
import logging


logging.basicConfig(level=logging.INFO)


def approve_private_endpoints(env: str):
    """
        Approve all ODW private endpoints
    """
    synapse_private_endpoint_manager = SynapsePrivateEndpointManager(Util.get_subsription_id(f"pins-odw-data-{env}-sub"))
    endpoints = synapse_private_endpoint_manager.get_all_names(
        workspace_name=f"pins-synw-odw-{env}-uks",
        resource_group_name=f"pins-rg-data-odw-{env}-uks"
    )
    for endpoint in endpoints:
        synapse_private_endpoint_manager.approve(
            endpoint,
            workspace_name=f"pins-synw-odw-{env}-uks",
            resource_group_name=f"pins-rg-data-odw-{env}-uks"
        )


if __name__ == "__main__":
    # Load command line arguments
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("-e", "--env", help="Environment to run against", required=True)
    args = parser.parse_args()
    env = args.env
    approve_private_endpoints(env)
