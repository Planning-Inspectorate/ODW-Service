from pydantic import BaseModel, ValidationError
import json
import pprint
from typing import List

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

    CaseReference: str
    AppealRefNumber: int | str
    ApplicationType: str
    AppealTypeReason: str = None # default value indicates optional
    # Contacts: list[Contact] = []
    Specialisms: list[Specialism] = []
    # GroundsForAppeal: list[GroundForAppeal] = []
    # EventTypes: list[EventType] = []
    # ChartStatuses: list[ChartStatus] = []
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

class ExternalDataModel(BaseModel):
    external_data: List[Cases]

external_data = [{
    'CaseReference': 123,
    'AppealRefNumber': 12345678,
    'ApplicationType': 'whatever',
    'AppealTypeReason': 'hello',
    'SpecialismID': 12345,
    'Specialism': 'MySpecialism'
    },
    {
    'CaseReference': 123,
    'AppealRefNumber': 12345678,
    'ApplicationType': 'whatever',
    'AppealTypeReason': 'hello',
    'SpecialismID': 67891,
    'Specialism': 'Generalist'
    },
    {
    'CaseReference': '987',
    'AppealRefNumber': 765487,
    'ApplicationType': 457,
    'AppealTypeReason': 'hi',
    'SpecialismID': 65438765,
    'Specialism': 'football'
    },
    {
    'CaseReference': '987',
    'AppealRefNumber': 765487,
    'ApplicationType': 457,
    'AppealTypeReason': 'hi',
    'SpecialismID': 8965487,
    'Specialism': 'running'
    }
]

# Preprocess the data to merge specialisms for the same CaseReference
merged_data = {}
for item in external_data:
    AppealRefNumber = item['AppealRefNumber']
    if AppealRefNumber not in merged_data:
        merged_data[AppealRefNumber] = {
            'CaseReference': item['CaseReference'],
            'AppealRefNumber': AppealRefNumber,
            'ApplicationType': item['ApplicationType'],
            'AppealTypeReason': item['AppealTypeReason'],
            'Specialisms': []
        }
    merged_data[AppealRefNumber]['Specialisms'].append({'SpecialismID': item['SpecialismID'], 'Specialism': item['Specialism']})

final_data = list(merged_data.values())

pprint.pprint(final_data)

# # Accessing the validated data
# print(external_data_model_instance.dict())

try:
    external_data_model_instance = ExternalDataModel(external_data=final_data)
    print("Success!")
except ValidationError as e:
    print(e)
    pprint.pprint(e.errors())

# print("Creating dictionary of model...")
# pprint.pprint(Cases.model_dump(self))

# case_instances = []
# for data in final_data:
#     try:
#         case_instance = Cases(**data)
#         case_instances.append(case_instance)
#         print("Success!!")
#     except ValidationError as e:
#         print(e)

# # print jaon schema from pydantic model above
# # print(json.dumps(Cases.model_json_schema(by_alias=False), indent=2))

# cases_dict = [Cases(**data) for data in external_data]
# pprint.pprint(cases_dict)
