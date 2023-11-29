from pydantic import BaseModel, ValidationError
import pprint
import csv
from collections import defaultdict
from model_funcs import convert_to_lower


class Contact(BaseModel):

    contactid: str
    title: str
    salutation: str
    firstname: str
    lastname: str
    typeofinvolvement: str


class Specialism(BaseModel):

    specialismid: int | str
    specialism: str


class GroundForAppeal(BaseModel):

    groundsforappeal: str
    groundletter: str
    groundforappealstartdate: str


class EventType(BaseModel):

    eventtype: str
    startdateofevent: str
    starttimeofevent: str
    enddateofevent: str
    dateeventrequested: str


class ChartStatus(BaseModel):

    chartstatus: str
    estpreptime: str
    estsittime: str
    estreptime: str
    actualduration: str


class Cases(BaseModel):

    casereference: str
    appealrefnumber: str
    contacts: list[Contact] = []
    specialisms: list[Specialism] = []
    groundsforappeal: list[GroundForAppeal] = []
    eventtypes: list[EventType] = []
    chartstatuses: list[ChartStatus] = []
    applicationtype: str
    appealtypereason: str
    appealtypegroup: str
    appealtype: str
    procedurename: str
    validity: str
    processingstate: str
    linkedappeal: str
    lastpublisheddate: str
    lpacode: str
    lpaname: str
    jurisdiction: str
    developmentorallegation: str
    caseprocess: str
    developmenttype: str
    relatedreferences: str
    appealsourceindicator: str
    level: str
    specialcircumstance: str
    appellantstatementsubmitted: str
    welshlanguage: str
    procedureappellant: str
    appealrecdate: str
    appealstartdate: str
    validto: str
    validitystatusdate: str
    callindate: str
    targetdate: str
    statementsdue: str
    thirdpartyrepsdue: str
    finalcommentsdue: str
    statementofcommongrounddue: str
    proofsdue: str
    consentdate: str
    ownershippermission: str
    modifydate: str
    lpadecisiondate: str
    outcomepublicsafety: str
    advertdetailsid: str
    reasonpublicsafety: str
    outcomeamenity: str
    reasonamenity: str
    advertinposition: str
    advertdescription: str
    lpaapplicationdate: str
    lpaapplicationreference: str
    section: str
    addressline1: str
    addressline2: str
    addresstown: str
    postcode: str
    easting: str
    northing: str
    inspectorneedtoentersite: str
    numberofresidences: str
    areaofsiteinhectares: str
    floorspaceinsquaremetres: str
    sitegreenbelt: str
    historicbuildinggrantmade: str
    agriculturalholding: str
    notificationofsv: str

class DartInstances (BaseModel):
    dart_data: list[Cases]


file_name = r"C:\Users\ChrisTopping\Downloads\dart_sample_ordered.csv"

data = []
with open(file_name, encoding="utf-8-sig") as csvfile:
    reader = csv.DictReader(csvfile)
    data.extend(reader)

merged_data = defaultdict(
    lambda: {
        "Contacts": [],
        "Specialisms": [],
        "GroundsForAppeal": [],
        "Events": [],
        "ChartStatus": [],
    }
)

for item in data:
    AppealRefNumber = item["AppealRefNumber"]
    case = merged_data["AppealRefNumber"]
    case.update({k.lower(): v for k, v in item.items() if k.lower() not in case or not isinstance(case[k.lower()], list)})

    contacts = case["Contacts"]
    new_contact = {
        "contactid": item["ContactID"],
        "title": item["Title"],
        "salutation": item["Salutation"],
        "firstname": item["FirstName"],
        "lastname": item["LastName"],
        "typeofinvolvement": item["TypeOfInvolvement"],
    }
    if new_contact not in contacts:
        contacts.append(new_contact)

    specialisms = case["Specialisms"]
    new_specialism = {
        "SpecialismID": item["SpecialismID"],
        "Specialism": item["Specialism"],
    }
    if new_specialism not in specialisms:
        specialisms.append(new_specialism)

    groundsforappeal = case["GroundsForAppeal"]
    new_groundsforappeal = {
        "GroundForAppeal": item["GroundForAppeal"],
        "GroundLetter": item["GroundLetter"],
        "GroundForAppealStartDate": item["GroundForAppealStartDate"],
    }
    if new_groundsforappeal not in groundsforappeal:
        groundsforappeal.append(new_groundsforappeal)

    events = case["Events"]
    new_events = {
        "EventType": item["EventType"],
        "StartDateOfEvent": item["StartDateOfEvent"],
        "StartTimeOfEvent": item["StartTimeOfEvent"],
        "EndDateOfEvent": item["EndDateOfEvent"],
        "DateEventRequested": item["DateEventRequested"],
    }
    if new_events not in events:
        events.append(new_events)

    chartstatus = case["ChartStatus"]
    new_chartstatus = {
        "ChartStatus": item["ChartStatus"],
        "EstPrepTime": item["EstPrepTime"],
        "EstSitTime": item["EstSitTime"],
        "EstRepTime": item["EstRepTime"],
        "ActualDuration": item["ActualDuration"],
    }
    if new_chartstatus not in chartstatus:
        chartstatus.append(new_chartstatus)

final_data = list(merged_data.values())

messages_lower = []
for message in final_data:
    message_lower = convert_to_lower(message)
    messages_lower.append(message_lower)

pprint.pprint(messages_lower)
# if not messages_lower:
#     print("NO MESSAGES TO PROCESS - VALIDATION OK")
# else:
#     try:    
#         DartInstances(dart_data=messages_lower)
#         print("VALIDATION SUCCEEDED!")
#         print(f'{len(data)} MESSAGES PROCESSED')
#     except ValidationError as e:
#         print(e)