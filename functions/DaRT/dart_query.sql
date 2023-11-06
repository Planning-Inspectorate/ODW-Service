/****************************************************************************

DaRT query to retrieve case data and related information.

There are 3 columns where multiple rows per case are possible, i.e.

Specialism
ContactID
GroundForAppeal

It could be best to split those out so we have 4 tables / queries instead
of one flat table

****************************************************************************/

USE ODW_HARMONISED_DB;

WITH SAMPLE_CASES AS 
(
SELECT      
                    
                    t1.CaseReference,
                    t1.AppealRefNumber,
                    t6.ApplicationType,
                    t6.AppealTypeReason,
                    t6.AppealTypeGroup,
                    t6.AppealType,
                    t12.ProcedureName,
                    t1.validity,
                    t5.ProcessingState,
                    t6.LinkedAppeal,
                    t21.LastPublishedDate,
                    t7.LPACode,
                    t7.LPAName,
                    t6.Jurisdiction,
                    t5.DevelopmentOrAllegation,
                    t5.CaseProcess,
                    t6.DevelopmentType,
                    t5.AppealSourceIndicator,
                    t5.Level,
                    t8.Specialism, -- a case can have multiple specialisms so more then 1 row per case is OK here
                    t9.SpecialCircumstance,
                    t5.ProcedureAppellant,
                    t6.AppealRecDate,
                    t6.AppealStartDate,
                    t1.ValidTo,
                    t10.ValidityStatusDate,
                    t5.CallInDate,
                    t5.TargetDate,
                    t5.StatementsDue,
                    t5.ThirdPartyRepsDue,
                    t5.FinalCommentsDue,
                    t5.StatementOfCommonGroundDue,
                    t5.ProofsDue,
                    t11.ModifyDate,
                    t12.LpaDecisionDate,
                    t13.OutcomePublicSafety,
                    t13.OutcomeAmenity,
                    t13.IsActive as AdvertInPosition,
                    t13.SignDescription as AdvertDescription,
                    t5.LPAApplicationDate,
                    t5.LPAApplicationReference,
                    t14.ContactID, -- multiple contacts per case so more than 1 row per case here as well
                    t14.Title,
                    t14.Salutation,
                    t14.FirstName,
                    t14.LastName,
                    t14.TypeOfInvolvement,
                    t15.AddressLine1,
                    t15.AddressLine2,
                    t15.AddressTown,
                    t15.PostCode,
                    t15.Easting,
                    t15.Northing,
                    t5.InspectorNeedToEnterSite,
                    t5.NumberOfResidences,
                    t5.AreaOfSiteInHectares,
                    t5.FloorSpaceInSquareMetres,
                    t5.SiteGreenBelt,
                    t5.HistoricBuildingGrantMade,
                    t12.OwnershipPermission,
                    t5.AgriculturalHolding,
                    t16.GroundForAppeal, -- multiple grounds per case
                    t16.GroundLetter,
                    t16.GroundForAppealStartDate,
                    t18.EventType,
                    t17.EstPrepTime,
                    t17.EstSitTime,
                    t17.EstRepTime,
                    t17.ChartStatus,
                    t18.StartDateOfEvent,
                    t18.StartTimeOfEvent,
                    t18.EndDateOfEvent,
                    t19.NotificationOfSV,
                    t18.DateEventRequested,
                    t17.ActualDuration

FROM                casework_case_info_dim t1

LEFT OUTER JOIN     casework_all_appeals_additional_data_dim t5
ON                  t1.AppealRefNumber = t5.AppealRefNumber
AND                 t1.IsActive = 'Y'
AND                 t5.IsActive = 'Y'

LEFT OUTER JOIN     casework_all_appeals_dim t6
ON                  t1.AppealRefNumber = t6.AppealRefNumber
AND                 t1.IsActive = 'Y'
AND                 t6.IsActive = 'Y'

LEFT OUTER JOIN     casework_local_planning_authority_dim t7
ON                  t6.LPAID = t7.LPAID
AND                 t6.IsActive = 'Y'
AND                 t7.IsActive = 'Y'

LEFT OUTER JOIN     casework_specialism_dim t8
ON                  t1.AppealRefNumber = t8.AppealRefNumber
AND                 t1.IsActive = 'Y'
AND                 t8.IsActive = 'Y'

LEFT OUTER JOIN     casework_special_circumstance_dim t9
ON                  t1.AppealRefNumber = t9.AppealRefNumber
AND                 t1.IsActive = 'Y'
AND                 t9.IsActive = 'Y'

LEFT OUTER JOIN     casework_case_dates_dim t10
ON                  t1.AppealRefNumber = t10.AppealRefNumber
AND                 t1.IsActive = 'Y'
AND                 t10.IsActive = 'Y'

LEFT OUTER JOIN     casework_specialist_modifications_dim t11
ON                  t1.AppealRefNumber = t11.AppealRefNumber
AND                 t1.IsActive = 'Y'
AND                 t11.IsActive = 'Y'

LEFT OUTER JOIN     casework_picaso_dim t12
ON                  t1.AppealRefNumber = t12.AppealRefNumber
AND                 t1.IsActive = 'Y'
AND                 t12.IsActive = 'Y'

LEFT OUTER JOIN     casework_advert_details_dim t13
ON                  t1.AppealRefNumber = t13.AppealRefNumber
AND                 t1.IsActive = 'Y'
AND                 t13.IsActive = 'Y'

LEFT OUTER JOIN     casework_contact_information_dim t14
ON                  t1.AppealRefNumber = t14.CaseNumber
AND                 t1.IsActive = 'Y'
AND                 t14.IsActive = 'Y'

LEFT OUTER JOIN     casework_nsip_project_info_internal_dim t15
ON                  t1.CaseReference = t15.CaseReference
AND                 t1.IsActive = 'Y'
AND                 t15.IsActive = 'Y'

LEFT OUTER JOIN     casework_enforcement_grounds_dim t16
ON                  t1.AppealRefNumber = t16.AppealRefNumber
AND                 t1.IsActive = 'Y'
AND                 t16.IsActive = 'Y'

LEFT OUTER JOIN     casework_event_dim t17
ON                  t1.AppealRefNumber = t17.AppealRefNumber
AND                 t1.IsActive = 'Y'
AND                 t17.IsActive = 'Y'

LEFT OUTER JOIN     casework_event_fact t18
ON                  t17.EventID = t18.EventID
AND                 t17.IsActive = 'Y'
AND                 t18.IsActive = 'Y'

LEFT OUTER JOIN     casework_specialist_environment_dim t19
ON                  t1.AppealRefNumber = t19.AppealRefNumber
AND                 t1.IsActive = 'Y'
AND                 t19.IsActive = 'Y'

LEFT OUTER JOIN     casework_nsip_advice_dim t21 
ON                  t1.CaseReference = t21.CaseReference
AND                 t1.IsActive = 'Y'
AND                 t21.IsActive = 'Y'

WHERE               t6.AppealRecDate > '2023-06-01'
AND                 t1.AppealRefNumber = '3222143'
)

SELECT * 
FROM SAMPLE_CASES