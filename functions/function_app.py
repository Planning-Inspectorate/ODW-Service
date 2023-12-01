"""
Azure Function code to read messages from Azure Service Bus and send them to Azure Storage
"""


import azure.functions as func
import logging
from servicebus_funcs import send_to_storage
import model_service_user, model_nsip
import config

_app = func.FunctionApp()


@_app.function_name("serviceuser")
@_app.route(route="serviceuser", methods=["get"], auth_level=func.AuthLevel.FUNCTION)
def serviceuser(req: func.HttpRequest) -> func.HttpResponse:
    """
    Azure Function endpoint for handling HTTP requests.

    Args:
        req: An instance of `func.HttpRequest` representing the HTTP request.

    Returns:
        An instance of `func.HttpResponse` representing the HTTP response.
    """

    logging.info("FUNCTION STARTED...")

    _UTC_TIMESTAMP = config.UTC_TIMESTAMP
    _FILENAME = f"messages_{config.SERVICE_USER_TOPIC}_{_UTC_TIMESTAMP}.json"

    try:
        send_to_storage(
            account_url=config.STORAGE,
            credential=config.CREDENTIAL,
            container=config.CONTAINER,
            filename=_FILENAME,
            data=model_service_user.model(),
        )

    except Exception as e:
        logging.error(f"Error occurred: {str(e)}")
        raise e

    return func.HttpResponse()


@_app.function_name("nsip")
@_app.route(route="nsip", methods=["get"], auth_level=func.AuthLevel.FUNCTION)
def nsip(req: func.HttpRequest) -> func.HttpResponse:
    """
    Azure Function endpoint for handling HTTP requests.

    Args:
        req: An instance of `func.HttpRequest` representing the HTTP request.

    Returns:
        An instance of `func.HttpResponse` representing the HTTP response.
    """

    logging.info("FUNCTION STARTED...")

    _UTC_TIMESTAMP = config.UTC_TIMESTAMP
    _FILENAME = f"messages_{config.NSIP_TOPIC}_{_UTC_TIMESTAMP}.json"

    try:
        send_to_storage(
            account_url=config.STORAGE,
            credential=config.CREDENTIAL,
            container=config.CONTAINER,
            filename=_FILENAME,
            data=model_nsip.model(),
        )

    except Exception as e:
        logging.error(f"Error occurred: {str(e)}")
        raise e

    return func.HttpResponse()
