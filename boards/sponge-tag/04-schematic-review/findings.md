# sponge-tag — schematic review, round 1

Reviewed: `03-schematic/sponge_tag.py` + `sponge_tag.net` (40 components), against `01-spec/` and the
nRF54L15 / SHT4x datasheets. Checks run: SKiDL ERC (0 errors / 0 warnings), `check_netlist.py`
(0 errors), plus the negative tests below.

> EXAMPLE of `hw-schematic-review` output, written to show the format. A real round reviews
> every IC pin by pin against downloaded datasheets.

| ID | Sev | Block | Finding | Evidence | Suggested fix | Status |
|---|---|---|---|---|---|---|
| R-01 | blocker | rf | Matching-network topology (L2/C6/L3/C9/L4) is a placeholder. Nordic's values are used, but the series/shunt order was not taken from the reference schematic. | `rf()` docstring; A03 "Limitation"; OQ-1 | Copy the topology from Nordic's QFN48 config 1 schematic / nRF54L15 DK design files | open |
| R-02 | blocker | mcu | Cap-to-pin assignment (C1 vs C2, which 100 nF sits at which VDD pin), FB1 position and the L1 DCC→DECD connection are inferred, not copied. | `mcu()` docstring; OQ-1 | Same source as R-01; also confirm DECD needs only C2 | open |
| R-03 | major | tooling | The netlist checker cannot check for unconnected power pins on SKiDL netlists (no libparts). | `check_netlist.py` warning | Mitigated: `unused()` now refuses to NC a non-GPIO pin. Negative test: removing the DECD connection stops the script ("U1 pin 45 (DECD) is not connected") | fixed |
| R-04 | major | mcu | Exposed-pad size of the QFN48 footprint not confirmed (EP 4.6 × 4.6 mm assumed). | OQ-2 | Read the package drawing; pick the matching KiCad footprint or make one | open |
| R-05 | minor | power | Q1 Vgs(th) max −0.9 V and RDS(on) at Vgs = −1.8 V must be confirmed for the 2.0 V end-of-life case. | A02 | Read the DMG2305UX datasheet; add the values to A02 | open |
| R-06 | minor | rf | Antenna pad 2 (`PCB_Trace`) is NC. Confirm the Johanson 2450AT18A100 pad 2 function (mechanical/NC vs. ground). | `rf()` | Check the antenna datasheet | open |
| R-07 | note | sensor | SHT40 powered straight from VDD. Idle 0.08 µA, so a switched supply isn't needed. | A01 | — | accepted |
| R-08 | note | debug | UART_TX/RX on P1.04/P1.05 match the nRF54L15 DK's UART20 pins, so the same firmware logs on both. | A04 | — | accepted |

**Summary:** 2 blockers, 2 majors (1 fixed), 2 minors, 2 notes. **Verdict: needs fixes.** R-01/R-02
need Nordic's reference schematic (a human can download the nRF54L15 DK design files, or the agent
can fetch them with permission).
