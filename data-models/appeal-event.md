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

        class Service_bus_appeal-event  {
            eventId: int
        }
    }

    namespace Standardised {

        class Horizon_appeals_event {
            caseNumber: varchar
            ,eventId: int
        }

        class appeals_event  {
            eventId: int
        }
    }

`Horizon_ODW_vw_Event` --> `Horizon_appeals_event`
`Service_bus_appeal` --> `appeals_event`

```