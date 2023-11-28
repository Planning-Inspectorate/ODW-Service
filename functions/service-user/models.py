"""
This module defines a pydantic model to be used for data validation. 
It defines the fields we expect to receive from the ODT Service Bus messages. 
The model does not accept extra fields and all fields are mandatory. 
Expected data types and constraints are also defined for each field.
"""

from pydantic import BaseModel, ValidationError, ConfigDict, Field
from uuid import UUID
import pprint
from model_funcs import convert_to_lower
from servicebus_funcs import get_messages
from azure.identity import DefaultAzureCredential

_NAMESPACE = "https://pins-sb-odw-dev-uks-b9rt9m.servicebus.windows.net"
_SUBSCRIPTION = "service-user"
_TOPIC = "service-user"
_MAX_MESSAGE_COUNT = 10
_CREDENTIAL = DefaultAzureCredential()

def model() -> list[dict]:
    
    """
    The 'model' function defines a class 'ServiceUser' and performs some operations on test data.

    Returns:
        data - a list of dictionaries containng Service Bus message data
    """

    class ServiceUser(BaseModel):

        """
        The 'ServiceUser' class represents a pydantic model for service users.

        Args:
            ID (int): The ID of the service user.
            SourceSystemID (UUID): The source system ID of the service user.
            salutation (str): The salutation of the service user.
            firstName (str): The first name of the service user.
            lastName (str): The last name of the service user.
            addressLine1 (str): The first line of the address of the service user.
            addressLine2 (str): The second line of the address of the service user.
            addressTown (str): The town of the address of the service user.
            addressCounty (str): The county of the address of the service user.
            postcode (str): The postcode of the address of the service user.
            organisation (str): The organization of the service user.
            organisationType (str): The organization type of the service user.
            telephoneNumber (str): The telephone number of the service user.
            otherPhoneNumber (str): The other phone number of the service user.
            faxNumber (str): The fax number of the service user.
            emailAddress (str): The email address of the service user.
            serviceUserType (str): The type of the service user.
            caseReference (str): The case reference of the service user.
        """

        model_config = ConfigDict(validate_assignment=True, extra="forbid")

        id: int = Field(le=99999999)
        sourcesystemid: UUID
        salutation: str = Field(max_length=10)
        firstname: str = Field(max_length=256)
        lastname: str = Field(max_length=256)
        addressline1: str = Field(max_length=256)
        addressline2: str = Field(max_length=256)
        addresstown: str = Field(max_length=256)
        addresscounty: str = Field(max_length=256)
        postcode: str = Field(max_length=8)
        organisation: str = Field(max_length=256)
        organisationtype: str = Field(max_length=256)
        telephonenumber: str = Field(max_length=11)
        otherphonenumber: str = Field(max_length=11)
        faxnumber: str = Field(max_length=11)
        emailaddress: str = Field(max_length=256)
        serviceusertype: str = Field(max_length=150)
        casereference: str = Field(max_length=256)

    class MessageInstances (BaseModel):

        """
        Represents a pydantic model for a list of ServiceUser instances.

        Args:
            messagedata (list[ServiceUser]): The list of ServiceUser instances.

        Attributes:
            messagedata (list[ServiceUser]): The list of ServiceUser instances.
        """
         
        messagedata: list[ServiceUser]

    test_data = [
        {
        "ID": 123,
        "SourceSystemID": "20f5484b88ae49b08af03a389b4917dd",
        "salutation": "teststring",
        "firstName": "teststring",
        "lastName": "teststring",
        "addressLine1": "teststring",
        "addressLine2": "teststring",
        "addressTown": "teststring",
        "addressCounty": "teststring",
        "postcode": "mycode",
        "organisation": "teststring",
        "organisationType": "teststring",
        "telephoneNumber": "teststring",
        "otherPhoneNumber": "teststring",
        "faxNumber": "teststring",
        "emailAddress": "teststring",
        "serviceUserType": "teststring",
        "caseReference": "teststring"
    },
        {
        "ID": 1234,
        "SourceSystemID": "20f5484b88ae49b08af03a389b4917dd",
        "salutation": "teststring",
        "firstName": "teststring",
        "lastName": "teststring",
        "addressLine1": "teststring",
        "addressLine2": "teststring",
        "addressTown": "teststring",
        "addressCounty": "teststring",
        "postcode": "mycode",
        "organisation": "teststring",
        "organisationType": "teststring",
        "telephoneNumber": "teststring",
        "otherPhoneNumber": "teststring",
        "faxNumber": "teststring",
        "emailAddress": "teststring",
        "serviceUserType": "teststring",
        "caseReference": "teststring"
    }
    ]

    # data=get_messages(
    #     _NAMESPACE, _CREDENTIAL, _TOPIC, _SUBSCRIPTION, _MAX_MESSAGE_COUNT
    # )
    data = test_data
    # convert input data dictionary keys to lowercase for comparison with model
    messages_lower = []
    for message in data:
        message_lower = convert_to_lower(message)
        messages_lower.append(message_lower)
    if not messages_lower:
        print("NO MESSAGES TO PROCESS - VALIDATION OK")
        return data
    else:
        try:    
            ServiceUserInstances = MessageInstances(messagedata=messages_lower)
            print("VALIDATION SUCCEEDED!")
            print(f'{len(data)} MESSAGES PROCESSED')
            return data
        except ValidationError as e:
            print(e)
            pprint.pprint(e.errors())
model()