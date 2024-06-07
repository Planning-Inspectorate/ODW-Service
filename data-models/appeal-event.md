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

        class Service bus: appeal-event  {
            eventId: int
        }
    }


```