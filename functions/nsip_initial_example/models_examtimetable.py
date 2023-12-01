from pydantic import BaseModel, ValidationError, ConfigDict
import json
import pprint
from datetime import datetime
from model_funcs import fill_nonexistent_properties, remove_undefined_properties, convert_to_lower

def model():

  class description (BaseModel):

      model_config = ConfigDict(
          validate_assignment=True,
          extra='forbid'
      )

      description : str

  class eventItems (BaseModel):
      
      model_config = ConfigDict(
         validate_assignment=True,
         extra='forbid'
     )

      eventLineItems : list(description)    

  test_data =  [{'description': ' item 1\r\n'},{'description': ' item 2'}] 

  # convert input data dicionary keys to lowercase for comparison with model
  test_data_lower = convert_to_lower(test_data)

  # pprint.pprint(test_data_lower)
  # print("*"*20)

  # define json schema for model
  json_schema = eventLineItems.model_json_schema(by_alias=False)

  # pprint.pprint(json_schema)
  # print("*"*20)
  # output_dict = fill_nonexistent_properties(test_data_lower, json_schema)

  # pprint.pprint(output_dict)

  # nsip.model_rebuild()

  try:
      print(eventLineItems(**test_data_lower).model_dump())
      print("Success!")
  except ValidationError as e:
      print(e)

model()