# <board> — systems engineering plan (lite SEMP)

Life-cycle model: V-model (ISO/IEC/IEEE 15288 technical processes), reviews SRR → PDR → CDR → TRR → SAR.

| Process | Agent | Output | Ends at review |
|---|---|---|---|
| Stakeholder needs & requirements | se-stakeholder | 01-stakeholder/ | SRR |
| System requirements | se-requirements | 02-requirements/ | SRR |
| Architecture definition | se-architecture | 03-architecture/ | PDR |
| System analysis | se-analysis | 04-analysis/ | PDR |
| Design definition: parts | hw-parts | 05-design/parts/ | PDR |
| Design definition: schematic | hw-schematic | 05-design/schematic/ | CDR |
| Design definition: layout + implementation (fab) | hw-layout | 05-design/layout/, 06-implementation/fab/ | CDR |
| Design definition: firmware | hw-firmware | 05-design/firmware/ | CDR |
| Design verification (reviews) | hw-schematic-review, hw-layout-review | 08-verification/design-reviews/ | CDR |
| Integration (bring-up) | se-integration | 07-integration/ | TRR |
| Verification | se-verification | 08-verification/ | SAR |
| Validation | se-validation | 09-validation/ | SAR |
| Technical management | se-manager | 00-management/ | every review |

## Schedule / milestones
| Review | Planned date | Actual |
|---|---|---|
