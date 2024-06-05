#### ODW Data Model

##### entity: appeal-document

Data model for appeal-document entity showing data flow from source to curated.

```mermaid

classDiagram

    direction LR

    namespace Sources {

        class appeal_document_sb_src {
            documentId: int
        }

        class Horizon_ODW_vw_DocumentMetadataAppeals_src {
            DocumentId: int
        }

        class AIE_Extracts_std_src {
            documentId: int
        }

    }
    
    namespace Standardised {

        class appeal_document_sb {
            documentId: int
        }

        class horizon_appeals_document_metadata {
            DocumentId: int
        }

        class aie_document_data_std {
            documentId: int
        }
    }

    namespace Harmonised {

        class aie_document_data_hrm {
            documentId: int
        }

        class appeals_document_metadata {
            appeal_document_sb
            appeals_document_metadata
        }
    }

    namespace Curated {

        class appeal_document {
            documentId: int
        }
    }

`appeal_document_sb_src` --> `appeal_document_sb`
`Horizon_ODW_vw_DocumentMetadataAppeals_src` --> `horizon_appeals_document_metadata`
`AIE_Extracts_std_src` --> `aie_document_data_std`
`appeal_document_sb` --> `appeals_document_metadata`
`horizon_appeals_document_metadata` --> `appeals_document_metadata`
`aie_document_data_std` --> `aie_document_data_hrm`
`aie_document_data_hrm` --> `appeals_document_metadata`
`appeals_document_metadata` --> `appeal_document`


```