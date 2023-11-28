from pydantic import BaseModel, ValidationError
import json
import pprint
import csv
from collections import defaultdict
from model_funcs import convert_to_lower


class Contact(BaseModel):
    ContactID: str
    Title: str
    Salutation: str
    Firstname: str
    LastName: str
    TypeOfInvolvement: str


class Specialism(BaseModel):
    SpecialismID: int | str
    Specialism: str


class GroundForAppeal(BaseModel):
    GroundsForAppeal: str
    GroundLetter: str
    GroundForAppealStartDate: str


class EventType(BaseModel):
    EventType: str
    StartDateOfEvent: str
    StartTimeOfEvent: str
    EndDateOfEvent: str
    DateEventRequested: str


class ChartStatus(BaseModel):
    ChartStatus: str
    EstPrepTime: str
    EstSitTime: str
    EstRepTime: str
    ActualDuration: str


class Cases(BaseModel):
    # CaseReference: str
    AppealRefNumber: int | str
    ApplicationType: str
    AppealTypeReason: str
    Contacts: list[Contact] = []
    Specialisms: list[Specialism] = []
    GroundsForAppeal: list[GroundForAppeal] = []
    EventTypes: list[EventType] = []
    ChartStatuses: list[ChartStatus] = []
    # AppealTypeGroup: str
    # AppealType: str
    # ProcedureName: str
    # validity: str
    # ProcessingState: str
    # LinkedAppeal: str
    # LastPublishedDate: str
    # LPACode: str
    # LPAName: str
    # Jurisdiction: str
    # DevelopmentOrAllegation: str
    # CaseProcess: str
    # DevelopmentType: str
    # RelatedReferences: str
    # AppealSourceIndicator: str
    # Level: str
    # Specialisms: str
    # SpecialCircumstance: str
    # AppellantStatementSubmitted: str
    # WelshLanguage: str
    # ProcedureAppellant: str
    # AppealRecDate: str
    # AppealStartDate: str
    # ValidTo: str
    # ValidityStatusDate: str
    # CallInDate: str
    # TargetDate: str
    # StatementsDue: str
    # ThirdPartyRepsDue: str
    # FinalCommentsDue: str
    # StatementOfCommonGroundDue: str
    # ProofsDue: str
    # ConsentDate: str
    # OwnershipPermission: str
    # ModifyDate: str
    # LpaDecisionDate: str
    # OutcomePublicSafety: str
    # AdvertDetailsID: str
    # ReasonPublicSafety: str
    # OutcomeAmenity: str
    # ReasonAmenity: str
    # AdvertInPosition: str
    # AdvertDescription: str
    # LPAApplicationDate: str
    # LPAApplicationReference: str
    # Section: str
    # ContactIDs: str
    # AddressLine1: str
    # AddressLine2: str
    # AddressTown: str
    # PostCode: str
    # Easting: str
    # Northing: str
    # InspectorNeedToEnterSite: str
    # NumberOfResidences: str
    # AreaOfSiteInHectares: str
    # FloorSpaceInSquareMetres: str
    # SiteGreenBelt: str
    # HistoricBuildingGrantMade: str
    # AgriculturalHolding: str
    # GroundsForAppeal: str
    # GroundForAppealStartDate: str
    # EventTypes: str
    # EstPrepTime: str
    # EstSitTime: str
    # EstRepTime: str
    # ChartStatuses: str
    # StartDatesOfEvent: str
    # StartTimesOfEvent: str
    # EndDateOfEvent: str
    # NotificationOfSV: str
    # DateEventRequested: str
    # ActualDuration: str


class DartInstances (BaseModel):
    dart_data: list[Cases]


file_name = r"C:\Users\ChrisTopping\Downloads\dart_sample_ordered.csv"

data = []
with open(file_name, encoding="utf-8") as csvfile:
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
    case = merged_data[AppealRefNumber]
    case.update({k: v for k, v in item.items() if k not in case})

    contacts = case["Contacts"]
    new_contact = {
        "ContactID": item["ContactID"],
        "Title": item["Title"],
        "Salutation": item["Salutation"],
        "FirstName": item["FirstName"],
        "LastName": item["LastName"],
        "TypeOfInvolvement": item["TypeOfInvolvement"],
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

pprint.pprint(DartInstances(dart_data=messages_lower).model_dump(warnings=False))
# if not messages_lower:
#     print("NO MESSAGES TO PROCESS - VALIDATION OK")
# else:
#     try:    
#         DartInstances(dart_data=messages_lower)
#         print("VALIDATION SUCCEEDED!")
#         print(f'{len(data)} MESSAGES PROCESSED')
#     except ValidationError as e:
#         print(e)