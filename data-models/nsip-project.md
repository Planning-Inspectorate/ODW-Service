#### ODW Data Model

##### entity: nsip-project

Data model for nsip-project entity showing data flow from source to curated.

```mermaid

classDiagram

    direction LR

    namespace Sources {

        class HZN_NSIP_Data_Copy {
            CaseID:int
        }

        class nsip-project {
            CaseID
        }


    }
    
    namespace Standardised {

        class horizon_nsip_data {
             casenodeid:int
        }

        class sb_nsip_project-std {
            CaseID
        }

    }

    namespace Harmonised {

        class sb_nsip_project-hrm{
            CaseID
        }

        class nsip_project-hrm {
            CaseID
        }

    }

    namespace Curated {

        class nsip_data {
            CaseID: int
        }
    }


`HZN_NSIP_Data_Copy` --> `horizon_nsip_data`
`nsip-project` -->`sb_nsip_project-std`
`sb_nsip_project-std` -->`sb_nsip_project-hrm`
`sb_nsip_project-hrm` -->`nsip_project-hrm`

`horizon_nsip_data` -->`nsip_project-hrm`
`nsip_project-hrm` -->`nsip_data`


```