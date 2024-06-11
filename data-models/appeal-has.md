#### ODW Data Model

##### entity: appeal-has

Data model for appeal-has entity showing Service Bus data flow from source to curated.

```mermaid

classDiagram

    direction LR

    namespace Sources {

        class ServiceBus_pins-sb-appeals-bo-dev-appeal-has {
            caseId: int
        }

    }
    
    namespace Standardised {

        class appeal_has_st {
            caseId: int
        }
    }

    namespace Harmonised {

        class appeals_has_hm {
            caseId: int
        }

    }

    namespace Curated {

        class appeal_has_cr {
            caseId: int
        }

    }

`ServiceBus_pins-sb-appeals-bo-dev-appeal-has` --> `appeal_has_st`
`appeal_has_st` --> `appeal_has_hm`
`appeal_has_hm` --> `appeal_has_cr`


```

