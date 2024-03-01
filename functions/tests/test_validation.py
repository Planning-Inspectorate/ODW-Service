from set_environment import config
import pprint
from azure.servicebus import ServiceBusClient
from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient
import json
from var_funcs import CREDENTIAL
from pins_data_model import load_schemas
import pytest

_CREDENTIAL = CREDENTIAL
_NAMESPACE = config['dev']["servicebus_namespace_odt"]
_MAX_MESSAGE_COUNT = config["global"]["max_message_count"]
_SCHEMAS = load_schemas.load_all_schemas()["schemas"]
_SCHEMA = _SCHEMAS["nsip-subscription.schema.json"]
_TOPIC = config["global"]["entities"]["nsip-subscription"]["topic"]
_SUBSCRIPTION = config["global"]["entities"]["nsip-subscription"]["subscription"]

def list_topics():
    topics = {k: v for k, v in config['global']['entities'].items()}
    return topics

def read_messages(namespace: str,
    credential: DefaultAzureCredential,
    topic: str,
    subscription: str,
    max_message_count: int,
) -> list:

    messages = []

    servicebus_client = ServiceBusClient(
    fully_qualified_namespace=namespace, credential=credential
)
    
    with servicebus_client:
        subscription_receiver = servicebus_client.get_subscription_receiver(
            topic_name=topic, 
            subscription_name=subscription,
        )

        print("Reading messages...")

        with subscription_receiver:
            received_msgs = subscription_receiver.peek_messages(
                max_message_count
            )

            for message in received_msgs:
                message_body = json.loads(str(message))
                messages.append(message_body)

    return messages

# pprint.pprint(read_messages(_NAMESPACE, _CREDENTIAL, _TOPIC, _SUBSCRIPTION, _MAX_MESSAGE_COUNT))

# def test_read_messages():
#     result = read_messages(_NAMESPACE, _CREDENTIAL, _TOPIC, _SUBSCRIPTION, _MAX_MESSAGE_COUNT)
#     assert len(result) >= 1

pprint.pprint(list_topics())