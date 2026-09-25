---
doc_id: SWC-REQ-001
title: SwapCell requirements
project: SwapCell
doc_type: Requirements
version: "0.2"
status: Draft
date: '2026-09-24'
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
---

# SwapCell requirements

These are first-pass requirements for the pack, the dock and the interface between them. Targets are proposals for review and will be checked by calculation at TRL 3. Requirements R10 and R12 define the open interface that other portfolio designs depend on, so changes to them need Amish's approval.

| ID | Requirement | Target | Verification (TRL 3 or later) |
| --- | --- | --- | --- |
| R1 | Nominal voltage in the 48 V light-vehicle class | 46.8 V nominal; operating window 39.0 to 54.6 V (3.0 to 4.2 V per cell) | Cell configuration calculation; datasheet |
| R2 | Usable capacity and energy | 10 Ah or more and 450 Wh or more at 0.2C, 25 °C | Calculation from cell datasheet; later capacity test |
| R3 | Discharge current, continuous and peak | 20 A continuous for a full discharge with cells below 60 °C from 25 °C ambient; 35 A peak for 10 s | Thermal and cell-current calculation; later load test |
| R4 | Charge time at the standard dock | 3 h or less from empty to full at 5 A; 80 % in 2 h or less | CC-CV charge calculation |
| R5 | Mass for one-hand carry and swap | 3.5 kg or less (7.7 lb) including handle and connector | Mass budget; later weighing |
| R6 | Mechanical envelope (interface) | Body 340 x 90 x 80 mm, +0 / -1.5 mm; overall length with handle and plug 400 mm or less | Massing model, then drawing sheet |
| R7 | Swap time and effort | Pack out of a dock or vehicle and a charged pack seated and latched in 10 s or less, one hand, no tools; insertion force 50 N or less | Design review; later timed trial |
| R8 | Ingress protection | Pack IP65, including the unmated connector face; dock IP54 for sheltered outdoor mounting | Design review of seals and contacts |
| R9 | Cycle life and state-of-health tracking | 500 cycles or more to 80 % of rated capacity at 0.5C charge and discharge, 25 °C; SoH estimate within ±5 % | Cell datasheet review; later cycling data |
| R10 | Blind-mate connector (interface) | 5,000 mating cycles or more; self-aligns over ±3 mm lateral and ±2° angular misalignment; 40 A continuous per power contact; contact sequence PACK- first, INTERLOCK last | Connector datasheet; design review |
| R11 | Protections | Cell overvoltage and undervoltage, charge and discharge overcurrent, short-circuit trip within 500 µs, over-temperature, charge lockout below 0 °C, cell-level fusing, pre-charge, output dead when unmated | BMS specification review; later fault injection |
| R12 | Data interface and logging (interface) | CAN 2.0B at 250 kbit/s with a published message set; pack stores 2,000 or more cycle records; any conforming dock reads and exports them as CSV without a cloud account | Message set review; later bench decode |

## Assumptions

- A 48 V class pack is 13 lithium-ion cells in series. The 3.0 V per cell lower limit is conservative for most NMC and NCA cells; the BMS enforces it regardless of the vehicle controller cutoff.
- 20 A continuous (about 940 W) covers a 750 W cargo-trike motor with margin. E-bikes at 250 to 500 W draw 5 to 11 A.
- A fleet vehicle swaps once or twice a day. Over five years that is about 3,650 mating cycles, so R10 at 5,000 cycles has about 35 % margin. Dock-side contacts see more cycles than pack-side ones and should be replaceable.
- R5 and R7 assume an adult lifting from a wall dock at 0.8 to 1.2 m height. A lower mounting height would need a review of R5.
- R9 depends on the cell chosen. High-energy 21700 cells often quote fewer cycles than high-power cells; see SWC-PRC-001.
