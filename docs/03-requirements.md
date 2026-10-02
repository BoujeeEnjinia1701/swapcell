---
doc_id: SWC-REQ-001
title: SwapCell requirements
project: SwapCell
doc_type: Requirements
version: "0.6"
status: Draft
date: '2026-10-02'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-09-24'
  author: Amish Chadha
  change: Initial scaffold
- version: "0.2"
  date: '2026-09-24'
  author: Amish Chadha
  change: First measurable requirements for TRL 2 (electrical, mechanical, interface, protection)
- version: "0.3"
  date: '2026-09-25'
  author: Amish Chadha
  change: TRL 3. Record Amish's 2026-09-25 decisions (SWC-DDR-001); add R13 to R15 for interface v0.3 (wake, charge-discharge mode, latch class V1) and R16 budget scope; status from SWC-CAL-001
- version: "0.4"
  date: '2026-09-25'
  author: Amish Chadha
  change: Recommendations accepted by Amish (DDR-002)
- version: "0.5"
  date: '2026-10-01'
  author: Amish Chadha
  change: Constructable design (SWC-DDR-003) mass and cost; budget treated as a value-engineering target
- version: "0.6"
  date: '2026-10-02'
  author: Amish Chadha
  change: "Interface v0.4 noted (decisions of 2026-10-02); no requirement target or status changed"
---

# SwapCell requirements

These are the requirements for the pack, the dock and the SwapCell interface between them (v0.4 since 2026-10-02: handle zone 84 x 43 mm, catch geometry published, LFP chemistry code and coding key reserved; no requirement target changed). Amish accepted the TRL 2 recommendations on 2026-09-25 (SWC-DDR-001), including three interface additions, now R13 to R15. Requirements R6, R10 and R12 to R15 define the open interface that other portfolio designs depend on, so changes to them need Amish's approval. On 2026-09-25 Amish also accepted the remaining recommendations (SWC-DDR-002): R3 is restated around temperature derating, and the values inside R13 and R15 are confirmed. The status column comes from SWC-CAL-001 v0.2; no requirement is shown to be not met, and two are at risk.

| ID | Requirement | Target | Verification | Status (SWC-CAL-001) |
| --- | --- | --- | --- | --- |
| R1 | Nominal voltage in the 48 V light-vehicle class | 46.8 V nominal; operating window 39.0 to 54.6 V (3.0 to 4.2 V per cell) | Cell configuration calculation; datasheet | Met |
| R2 | Usable capacity and energy | 10 Ah or more and 450 Wh or more at 0.2C, 25 °C | Calculation from cell datasheet; later capacity test. Applies to the standard 4.2 V charge; fleet mode (4.1 V) gives about 419 Wh by design | At risk: 9.7 Ah at the cell datasheet minimum |
| R3 | Discharge current, continuous and peak, with temperature derating | 20 A continuous for a full discharge with cells below 60 °C from 25 °C ambient in an open-air mount (back and lid faces open); 35 A peak for 10 s. In any other mount or ambient, PACK_LIMITS derates the allowed discharge current (full to 50 °C cell temperature, linear to 5 A at 60 °C) so cells stay below 60 °C | Thermal and cell-current calculation; later load test | Met on paper: 51 °C in open air (56 °C with higher resistance); derates to about 18.6 A enclosed and 14 A from 45 °C |
| R4 | Charge time at the standard dock | 3 h or less from empty to full at 5 A; 80 % in 2 h or less | CC-CV charge calculation | Met |
| R5 | Mass for one-hand carry and swap | 3.5 kg or less (7.7 lb) including handle and connector | Mass budget; later weighing | Met: 3.03 kg (SWC-DDR-003) |
| R6 | Mechanical envelope (interface) | Body 340 x 90 x 80 mm, +0 / -1.5 mm; overall length with handle and plug 400 mm or less | Massing model, then drawing sheet | Met: 393 mm overall |
| R7 | Swap time and effort | Pack out of a dock or vehicle and a charged pack seated and latched in 10 s or less, one hand, no tools; insertion force 50 N or less | Design review; later timed trial | Not verifiable at TRL 3 |
| R8 | Ingress protection | Pack IP65, including the unmated connector face; dock IP54 for sheltered outdoor mounting | Design review of seals and contacts | Not verifiable at TRL 3 |
| R9 | Cycle life and state-of-health tracking | 500 cycles or more to 80 % of rated capacity at 0.5C charge and discharge, 25 °C; SoH estimate within ±5 % | Cell datasheet review; later cycling data. The 4.1 V fleet charge mode (decided) is the main mitigation | At risk |
| R10 | Blind-mate connector (interface) | 5,000 mating cycles or more; self-aligns over ±3 mm lateral and ±2° angular misalignment; 40 A continuous per power contact; contact sequence PACK- first, INTERLOCK last | Connector datasheet; design review. Family decided: custom keyed shroud with commercial contacts (SWC-DDR-002) | Not verifiable at TRL 3 |
| R11 | Protections | Cell overvoltage and undervoltage, charge and discharge overcurrent, short-circuit trip within 500 µs, over-temperature, charge lockout below 0 °C, cell-level fusing, pre-charge, output dead when unmated | BMS specification review; later fault injection | Not verifiable at TRL 3 |
| R12 | Data interface and logging (interface) | CAN 2.0B at 250 kbit/s with a published message set; pack stores 2,000 or more cycle records; any conforming dock reads and exports them as CSV without a cloud account; bit layout as published in SWC-PRC-001 v0.3 | Message set review, bus-load calculation; later bench decode | Met on paper |
| R13 | Wake for hosts without CAN or a wake supply (interface v0.3 item W) | Pack wakes from sleep when a receiver closes INTERLOCK through a 10 kΩ coding resistor, drawing no supply from the host; also wakes on WAKE (5 to 15 V) or its manual button; rejects a shorted or open loop; sleep drain 1 % of capacity per month or less; legacy discharge-only mode at 15 A for hosts without CAN | Calculation; later bench check | Met on paper |
| R14 | Charge-while-discharging mode (interface v0.3 item C) | Dock, station and vehicle hosts may request mode 4 (charge-discharge); pack allows net current between the allowed charge and allowed discharge limits without interrupting its output, and on a charge-side fault stops charge only and keeps discharge | Message set review; calculation; later bench check | Met on paper |
| R15 | Latch vibration rating for vehicles (interface v0.3 item V) | Class V1 vehicle receivers and the pack latch: no latch release and no power-contact interruption of 1 ms or longer under the UN 38.3 test T3 sine profile (7 to 200 Hz, peak 8 g) in three axes and 25 g, 11 ms half-sine shocks; latch proof load 1.72 kN along the insertion axis; receiver preload 330 N or more with 50 N or less hand force. Class D (gravity docks) needs no rating | Calculation; later vibration test (TRL 4, on hold) | Not verifiable at TRL 3 |
| R16 | Prototype cost scope | Parts for one pack and one wall dock at the USD 700 value-engineering target or under (`budget_usd` in `project.yaml`, a hypothetical control target, not a limit). A SwapCell pack is priced once, here, and excluded from each dependent kit budget | Priced BOM | Under the target: USD 606, USD 94 under |

## Assumptions

- A 48 V class pack is 13 lithium-ion cells in series. The 3.0 V per cell lower limit is conservative for most NMC and NCA cells; the BMS enforces it regardless of the vehicle controller cutoff.
- 20 A continuous (about 940 W) covers a 750 W cargo-trike motor with margin. E-bikes at 250 to 500 W draw 5 to 11 A.
- A fleet vehicle swaps once or twice a day. Over five years that is about 3,650 mating cycles, so R10 at 5,000 cycles has about 37 % margin (SWC-CAL-001). Dock-side contacts see more cycles than pack-side ones and should be replaceable.
- R5 and R7 assume an adult lifting from a wall dock at 0.8 to 1.2 m height. A lower mounting height would need a review of R5.
- R9 depends on the cell chosen. High-energy 21700 cells often quote fewer cycles than high-power cells; see SWC-PRC-001.
- R13 to R15 were approved by Amish on 2026-09-25 as interface v0.3 additions. The specific values (10 kΩ coding, 100 µA sleep target, 25 g shock, 330 N preload) were engineering proposals inside those additions; Amish confirmed them on 2026-09-25 (SWC-DDR-002).
- R15 uses the UN 38.3 test T3 vibration profile because every pack must pass it for transport anyway; the 25 g shock is a proposed curb-strike level for rigid cargo vehicles.
- R16: the USD 700 value-engineering target covers the parts for one pack and one dock. A second pack for a real swap demonstration (about USD 436 more, about USD 1,042 in total with the constructable design) is a build budget, to be set before any build as Amish decided on 2026-09-25 (SWC-DDR-002); it is on hold with TRL 4.

> **Safety:** The pack is a 468 Wh lithium-ion battery at up to 54.6 V DC that can deliver about 500 A into a short. R11, R13 (reject a shorted INTERLOCK loop) and R14 (never charge below 0 °C, even in charge-discharge mode) are safety requirements, not conveniences.
