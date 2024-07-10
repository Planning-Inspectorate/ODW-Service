#### ODW Data Model

##### entity: appeal-document

Data model for appeal-document entity showing data flow from source to curated.

```mermaid

classDiagram

    direction LR

    namespace Sources {

        class Horizon_ODW_vw_RelevantReps {
            documentId: int
        }

        class nsip_representation {
            DocumentId: int
        }
    }

    namespace Standardised {

        class Horizon_nsip_relevant_representation {
            documentId: int
        }

        class sb_nsip_representation-std {
            DocumentId: int
        }
    }

    namespace Harmonised {

        class sb_nsip_relevant_representation-hrm {
            DocumentId: int
        }

        class nsip_relevant_representation-hrm {
            DocumentId: int
        }
    }

    namespace Curated {

        class relevant_representation {
            DocumentId: int
        }
    }

    

`nsip_representation` --> `sb_nsip_representation-std`
`sb_nsip_representation-std` --> `sb_nsip_relevant_representation-hrm`
`sb_nsip_relevant_representation-hrm` --> `nsip_relevant_representation-hrm`


`Horizon_ODW_vw_RelevantReps` --> `Horizon_nsip_relevant_representation`
`Horizon_nsip_relevant_representation` --> `nsip_relevant_representation-hrm`
`nsip_relevant_representation-hrm` --> `relevant_representation`

```