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

        
        
        
    class eventDescription (BaseModel):
        
        #model_config = ConfigDict(validate_assignment=True, extra="forbid")
        
        eventlineitemdescription : str = Field(max_length=100)
        
        
        
    class AllEventItems (BaseModel):
        
        eventid : int
        type : str
        eventtitle : str
        description : str
        eventdeadlinestartdate : str
        date : str
        eventlineitems : list[eventDescription]
        
        
    class Case (BaseModel):
        
        events : list[AllEventItems]
        casereference : str

        
    class CaseList (BaseModel):
        
        case_data : list[Case]
        
        
        

    
    
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