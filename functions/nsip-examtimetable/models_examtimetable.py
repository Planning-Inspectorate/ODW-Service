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


def model() -> None:

    """
    The 'model' function defines a class 'ServiceUser' and performs some operations on test data.

    Returns:
        None
    """

        
    class descriptionInstance (BaseModel):
        
        #model_config = ConfigDict(validate_assignment=True, extra="forbid")
        
        description: str = Field(max_length=100)
        
        
    class descriptionInstances (BaseModel):
        
        description_data : list[descriptionInstance]
        
        
    class eventDescription (BaseModel):
        
        #model_config = ConfigDict(validate_assignment=True, extra="forbid")
        
        eventlineitemdescription : str = Field(max_length=100)
        
    class EventItems (BaseModel):
        
        #eventid : int
        #type : str
        #eventtitle : str
        #description : str
        #eventdeadlinestartdate : str
        #date : str
        eventlineitems : list[eventDescription]
        
        
    class AllEventItems (BaseModel):
        
        eventid : int
        type : str
        eventtitle : str
        description : str
        eventdeadlinestartdate : str
        date : str
        eventlineitems : list[eventDescription]
        
    class EventItemsList (BaseModel):
        
        event_data : list[AllEventItems]
        
        
    class EventData (BaseModel):
        
        eventid : int
        type : str
        eventtitle : str
        description : str
        eventdeadlinestartdate : str
        date : str
        #event_data : list(EventItems)
        
    
    class EventDataList (BaseModel):
        
        event_details : list[EventData]
        
        
    class Case (BaseModel):
        
        events : list[AllEventItems]
        casereference : str

        
    class CaseList (BaseModel):
        
        case_data : list[Case]
        
        
        
    test_desc = [{"description": " item 1\r\n"},{"description": " item 2"}]
    
    test_event_data = [{"eventId": "1"  ,
              "type": "Preliminary Meeting",
              "eventTitle": "Example Preliminary Meeting",
              "description": "A preliminary meeting will be held to discuss the examination process.",
              "eventDeadlineStartDate": "2023-06-10",
              "date": "2023-06-10" }]
    
    
    test_desc_list = [               {
                        "eventLineItemDescription": "Item 1 Preliminary Description"
                    },
                    {
                        "eventLineItemDescription": "Item 2 Preliminary Description"
                    } ]
    
    test_event = [{ "eventId": "1"  ,
              "type": "Preliminary Meeting",
              "eventTitle": "Example Preliminary Meeting",
              "description": "A preliminary meeting will be held to discuss the examination process.",
              "eventDeadlineStartDate": "2023-06-10",
              "date": "2023-06-10" ,
                 "eventLineitems": [
                {
                    "eventlineitemdescription": "Item 1 Preliminary Description"
                },
                {
                    "eventlineitemdescription": "Item 2 Preliminary Description"
                }] }] #}]
    
    
    test_case = [{
    "casereference": "BC0110004",
    "events": [
        {
            "eventid": 1,
            "type": "Preliminary Meeting",
            "eventtitle": "Example Preliminary Meeting",
            "description": "A preliminary meeting will be held to discuss the examination process.",
            "eventdeadlinestartdate": "2023-06-10",
            "date": "2023-06-10",
            "eventlineitems": [
                {
                    "eventlineitemdescription": "Item 1 Preliminary Description"
                },
                {
                    "eventlineitemdescription": "Item 2 Preliminary Description"
                }
            ]
        } ] }]



    #convert input data dictionary keys to lowercase for comparison with model
    messages_lower = []
    for message in test_desc:
        message_lower = convert_to_lower(message)
        messages_lower.append(message_lower)
        
    print(messages_lower)
    try:    
          ServiceUserInstances = descriptionInstances(description_data=messages_lower)
          print("VALIDATION SUCCEEDED!")
    except ValidationError as e:
          print(e)
          pprint.pprint(e.errors())
          
          
    messages_lower = []
    for message in test_desc_list:
        message_lower = convert_to_lower(message)
        messages_lower.append(message_lower)
        
    print(messages_lower)
    try:    
          ServiceUserInstances = EventItems(eventlineitems=messages_lower)
          print("VALIDATION SUCCEEDED!")
    except ValidationError as e:
          print(e)
          pprint.pprint(e.errors())
          

          
    messages_lower = []
    for message in test_event_data:
        message_lower = convert_to_lower(message)
        messages_lower.append(message_lower)
        
    print(messages_lower)
    try:    
          ServiceUserInstances = EventDataList(event_details=messages_lower)
          print("VALIDATION SUCCEEDED!")
    except ValidationError as e:
          print(e)
          pprint.pprint(e.errors())
          
    messages_lower = []
    for message in test_event:
        message_lower = convert_to_lower(message)
        messages_lower.append(message_lower)
        
    print(messages_lower)
    try:    
          ServiceUserInstances = EventItemsList(event_data=messages_lower)
          print("VALIDATION SUCCEEDED!")
    except ValidationError as e:
          print(e)
          pprint.pprint(e.errors())
          
    messages_lower = []
    for message in test_case:
        message_lower = convert_to_lower(message)
        messages_lower.append(message_lower)
        
    print(messages_lower)
    try:    
          ServiceUserInstances = CaseList(case_data=messages_lower)
          print("VALIDATION SUCCEEDED!")
    except ValidationError as e:
          print(e)
          pprint.pprint(e.errors())
          
model()