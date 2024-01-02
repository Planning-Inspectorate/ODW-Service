"""
Azure Function code to read messages from Azure Service Bus and send them to Azure Storage
"""

import azure.functions as func
import logging
from servicebus_funcs import get_messages_and_validate, send_to_storage
from set_environment import current_config, config
import var_funcs

_STORAGE = current_config["storage_account"]
_CONTAINER = current_config["storage_container"]
_CREDENTIAL = var_funcs.CREDENTIAL
_NAMESPACE = current_config["servicebus_namespace_odt"]
_MAX_MESSAGE_COUNT = config["global"]["max_message_count"]
_MAX_WAIT_TIME = config["global"]["max_wait_time"]

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

    import var_funcs
    from model_service_user import ServiceUser

    logging.info("FUNCTION STARTED...")

    _ENTITY = config["global"]["service-user-entity"]
    _CURRENT_DATE = var_funcs.CURRENT_DATE
    _UTC_TIMESTAMP = var_funcs.UTC_TIMESTAMP
    _FILENAME = f"{_ENTITY}/{_CURRENT_DATE}/{_ENTITY}_{_UTC_TIMESTAMP}.json"
    _MODEL = ServiceUser

    try:
        _data = get_messages_and_validate(
            namespace=_NAMESPACE,
            credential=_CREDENTIAL,
            topic=_ENTITY,
            subscription=_ENTITY,
            max_message_count=_MAX_MESSAGE_COUNT,
            max_wait_time=_MAX_WAIT_TIME,
            model=_MODEL,
        )
    except Exception as e:
        logging.error(f"Error occurred: {str(e)}")
        raise e

    try:
        send_to_storage(
            account_url=_STORAGE,
            credential=_CREDENTIAL,
            container=_CONTAINER,
            filename=_FILENAME,
            data=_data,
        )
    except Exception as e:
        logging.error(f"Error occurred: {str(e)}")
        raise e
    return func.HttpResponse()


@_app.function_name("nsipproject")
@_app.route(route="nsipproject", methods=["get"], auth_level=func.AuthLevel.FUNCTION)
def nsipproject(req: func.HttpRequest) -> func.HttpResponse:
    """
    Azure Function endpoint for handling HTTP requests.

    Args:
        req: An instance of `func.HttpRequest` representing the HTTP request.

    Returns:
        An instance of `func.HttpResponse` representing the HTTP response.
    """

    import var_funcs
    from model_nsip_project import NsipProject

    logging.info("FUNCTION STARTED...")

    _ENTITY = config["global"]["nsip-project-entity"]
    _CURRENT_DATE = var_funcs.CURRENT_DATE
    _UTC_TIMESTAMP = var_funcs.UTC_TIMESTAMP
    _FILENAME = f"{_ENTITY}/{_CURRENT_DATE}/{_ENTITY}_{_UTC_TIMESTAMP}.json"
    _MODEL = NsipProject

    try:
        _data = get_messages_and_validate(
            namespace=_NAMESPACE,
            credential=_CREDENTIAL,
            topic=_ENTITY,
            subscription=_ENTITY,
            max_message_count=_MAX_MESSAGE_COUNT,
            max_wait_time=_MAX_WAIT_TIME,
            model=_MODEL,
        )
    except Exception as e:
        logging.error(f"Error occurred: {str(e)}")
        raise e

    try:
        send_to_storage(
            account_url=_STORAGE,
            credential=_CREDENTIAL,
            container=_CONTAINER,
            filename=_FILENAME,
            data=_data,
        )
    except Exception as e:
        logging.error(f"Error occurred: {str(e)}")
        raise e
    return func.HttpResponse()
