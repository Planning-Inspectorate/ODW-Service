#### ODW Data Model

##### entity: appeal-event

Data model for appeal-event entity showing data flow from source to curated.

```mermaid

classDiagram

    direction LR

    namespace Sources {

        class Horizon_ODW_vw_Event {
            caseNumber: varchar
            ,eventId: int
        }

        class Service_bus_appeal_event  {
            eventId: int
        }
    }

    namespace Standardised {

        class odw_standardised_db.Horizon_appeals_event {
            caseNumber: varchar
            ,eventId: int
        }

        class appeals_event  {
            eventId: int
        }
    }

    namespace Harmonised {

        class Horizon_appeals_event_hrm {
            caseNumber: varchar
            ,eventId: int
        }

        class appeals_event  {
            eventId: int
        }
    }

`Horizon_ODW_vw_Event` --> `Horizon_appeals_event`
`Service_bus_appeal_event` --> `appeals_event`

```