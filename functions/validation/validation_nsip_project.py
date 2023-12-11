import sys
from pathlib import Path
current_file = Path(__file__).resolve()
functions_folder = current_file.parent.parent
sys.path.append(str(functions_folder))

from models import nsip_project

from pydantic import BaseModel, ValidationError
from servicebus_funcs import get_messages
import config

_NAMESPACE = config.ODT_NAMESPACE
_SUBSCRIPTION = config.NSIP_PROJECT_SUBSCRIPTION
_TOPIC = config.NSIP_PROJECT_TOPIC
_MAX_MESSAGE_COUNT = config.MAX_MESSAGE_COUNT
_CREDENTIAL = config.CREDENTIAL
_MESSAGES = nsip_project.NsipProject

def validate():
    class MessageInstances(BaseModel):

        """
        Represents a pydantic model for a list of ServiceUser instances.

        Args:
            messagedata (list[ServiceUser]): The list of ServiceUser instances.

        Attributes:
            messagedata (list[ServiceUser]): The list of ServiceUser instances.
        """

        messagedata: list[_MESSAGES]

    _data = get_messages(
        _NAMESPACE, _CREDENTIAL, _TOPIC, _SUBSCRIPTION, _MAX_MESSAGE_COUNT
    )

    try:
        MessageInstances(messagedata=_data)
        print("VALIDATION SUCCEEDED!")
        print(f"{len(_data)} MESSAGES PROCESSED")
    except ValidationError as e:
        print(e)
        raise e