"""
Service bus triggered functions to validate messages consumed by ODT and write them to the data lake raw layer.
"""

import logging
import json
import jsonschema
import azure.functions as func

_app = func.FunctionApp()

# nsip-document
@_app.function_name(name="nsip-document")
@_app.service_bus_topic_trigger(arg_name="message", 
                               topic_name="nsip-document", 
                               connection="ServiceBusConnection", 
                               subscription_name="nsip-document")
def process_nsip_document(message: func.ServiceBusMessage):
    process_message(message, "nsip-document")


# nsip-exam-timetable
@_app.function_name(name="nsip-exam-timetable")
@_app.service_bus_topic_trigger(arg_name="message", 
                               topic_name="nsip-exam-timetable", 
                               connection="ServiceBusConnection", 
                               subscription_name="nsip-exam-timetable")
def process_nsip_exam_timetable(message: func.ServiceBusMessage):
    process_message(message, "nsip-exam-timetable")


# nsip-project-update
@_app.function_name(name="nsip-project-update")
@_app.service_bus_topic_trigger(arg_name="message", 
                               topic_name="nsip-project-update", 
                               connection="ServiceBusConnection", 
                               subscription_name="nsip-project-update")
def process_nsip_project_update(message: func.ServiceBusMessage):
    process_message(message, "nsip-project-update")


# nsip-representation
@_app.function_name(name="nsip-representation")
@_app.service_bus_topic_trigger(arg_name="message", 
                               topic_name="nsip-representation", 
                               connection="ServiceBusConnection", 
                               subscription_name="nsip-representation")
def process_nsip_representation(message: func.ServiceBusMessage):
    process_message(message, "nsip-representation")


# nsip-subscription
@_app.function_name(name="nsip-subscription")
@_app.service_bus_topic_trigger(arg_name="message", 
                               topic_name="nsip-subscription", 
                               connection="ServiceBusConnection", 
                               subscription_name="nsip-subscription")
def process_nsip_subscription(message: func.ServiceBusMessage):
    process_message(message, "nsip-subscription")


# s51-advice
@_app.function_name(name="s51-advice")
@_app.service_bus_topic_trigger(arg_name="message", 
                               topic_name="s51-advice", 
                               connection="ServiceBusConnection", 
                               subscription_name="s51-advice")
def process_s51_advice(message: func.ServiceBusMessage):
    process_message(message, "s51-advice")


def process_message(message: func.ServiceBusMessage, schema_name: str):
    try:
        message_body = message.get_body().decode("utf-8")
        
        logging.info("Running validation for message " + message_body + " against schema " + schema_name)

        body_json = json.loads(message_body)
        
        schema = schemas[schema_name]

        jsonschema.validate(instance=body_json, schema=schema)

        logging.info("Schema validated successfully")

        # TODO: Write to storage
    except jsonschema.exceptions.ValidationError as e:
        logging.error("Validation failed: " + str(e))
    except Exception as e:
        logging.error("Unknown error " + str(e))
        

def load_schema(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)
    

schemas = {
    "nsip-document": load_schema("schemas/nsip-document.schema.json"),
    "nsip-exam-timetable": load_schema("schemas/nsip-exam-timetable.schema.json"),
    "nsip-project-update": load_schema("schemas/nsip-project-update.schema.json"),
    "nsip-project": load_schema("schemas/nsip-project.schema.json"),
    "nsip-representation": load_schema("schemas/nsip-representation.schema.json"),
    "nsip-subscription": load_schema("schemas/nsip-subscription.schema.json"),
    "s51-advice": load_schema("schemas/s51-advice.schema.json"),
    "service-user": load_schema("schemas/service-user.schema.json")
}