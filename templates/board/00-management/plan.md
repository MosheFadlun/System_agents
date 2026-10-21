# <board> — systems engineering plan (lite SEMP)

Life-cycle model: V-model (ISO/IEC/IEEE 15288 technical processes), reviews SRR → PDR → CDR → TRR → SAR,
builds EVT → DVT → PVT (npi). Medical devices: design controls (ISO 13485 7.3 / 21 CFR 820) on top.

## Active disciplines (set by se-architecture, confirmed by the human)
| Discipline | In scope? | Why / elements | Design agent | Reviewer |
|---|---|---|---|---|
| Electronics | | | hw-parts, hw-schematic, hw-layout | hw-schematic-review, hw-layout-review |
| FPGA | | | fpga-design | design-review |
| MCU firmware | | | hw-firmware | design-review |
| Embedded Linux | | | sw-linux | design-review |
| Mechanics: plastic | | | mech-plastic | design-review, dfm |
| Mechanics: metal | | | mech-metal | design-review, dfm |
| Optics | | | optics | design-review |
| Medical regulation | | | med-regulatory | se-manager (review package) |
| Medical standards / risk | | | med-standards | se-manager |
| Clinical | | | clinical | se-manager |
| NPI / manufacturing / DFM | yes (any built product) | | npi, mfg-engineering, dfm | se-manager |

## Processes
| Process | Agent | Output | Ends at review |
|---|---|---|---|
| Stakeholder needs & requirements | se-stakeholder | 01-stakeholder/ | SRR |
| Regulatory strategy (medical) | med-regulatory | 10-regulatory/ | SRR (class), PDR (pathway) |
| Clinical evaluation (medical) | clinical | 11-clinical/ | PDR, SAR |
| Standards and risk management (medical) | med-standards | 10-regulatory/standards/ | PDR → SAR |
| System requirements | se-requirements | 02-requirements/ | SRR |
| Architecture definition | se-architecture | 03-architecture/ | PDR |
| System analysis | se-analysis | 04-analysis/ | PDR |
| Design definition per discipline | see table above | 05-design/<discipline>/ | CDR |
| Design verification (peer reviews) | hw-*-review, design-review | 08-verification/design-reviews/ | CDR |
| DFx review | dfm | 12-npi/dfm/ | CDR, each build |
| Manufacturing & test engineering | mfg-engineering | 12-npi/manufacturing/ | CDR → PVT |
| NPI builds and design transfer | npi | 12-npi/ | each build, transfer |
| Implementation (fab files) | hw-layout + discipline agents | 06-implementation/ | CDR |
| Integration (bring-up) | se-integration | 07-integration/ | TRR |
| Verification | se-verification | 08-verification/ | SAR |
| Validation | se-validation | 09-validation/ | SAR |
| Technical management | se-manager | 00-management/ | every review |

## Schedule / milestones
| Review / build | Planned date | Actual |
|---|---|---|
