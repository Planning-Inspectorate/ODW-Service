"""
Azure Function code to read messages from Azure Service Bus and send them to Azure Storage
"""


import azure.functions as func
import logging
import datetime
from azure.servicebus import ServiceBusClient
from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient
from servicebus_funcs import get_messages, send_to_storage

_NAMESPACE = "https://pins-sb-odw-dev-uks-b9rt9m.servicebus.windows.net"
_SUBSCRIPTION = "service-user"
_TOPIC = "service-user"
_MAX_MESSAGE_COUNT = 10
_STORAGE = "https://pinsstodwdevuks9h80mb.blob.core.windows.net"
_CONTAINER = "odw-raw/odt/test"
_CREDENTIAL = DefaultAzureCredential()

_app = func.FunctionApp()


@_app.function_name("serviceuser")
@_app.route(route="serviceuser", methods=["get"], auth_level=func.AuthLevel.FUNCTION)
def main(req: func.HttpRequest) -> func.HttpResponse:
    
    """
    Azure Function endpoint for handling HTTP requests.

    Args:
        req: An instance of `func.HttpRequest` representing the HTTP request.

    Returns:
        An instance of `func.HttpResponse` representing the HTTP response.
    """

    logging.info("FUNCTION STARTED...")

    _UTC_TIMESTAMP = (
        datetime.datetime.now(datetime.timezone.utc)
        .replace(tzinfo=datetime.timezone.utc)
        .isoformat()
    )
    _FILENAME = f"messages_{_TOPIC}_{_UTC_TIMESTAMP}.json"

    try:
        send_to_storage(
            account_url=_STORAGE,
            credential=_CREDENTIAL,
            container=_CONTAINER,
            filename=_FILENAME,
            data=get_messages(
                _NAMESPACE, _CREDENTIAL, _TOPIC, _SUBSCRIPTION, _MAX_MESSAGE_COUNT
            ),
        )

    except Exception as e:
        logging.error(f"Error occurred: {str(e)}")

    return func.HttpResponse()
