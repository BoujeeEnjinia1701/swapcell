---
doc_id: SWC-DDR-001
title: SwapCell TRL 2 review decisions and interface v0.3
project: SwapCell
doc_type: Design decision record
version: "0.3"
status: Draft
date: '2026-10-02'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-09-25'
  author: Amish Chadha
  change: Record Amish's 2026-09-25 decisions on the TRL 2 review and issue SwapCell interface v0.3
- version: "0.2"
  date: '2026-09-25'
  author: Amish Chadha
  change: Recommendations accepted by Amish (DDR-002)
- version: "0.3"
  date: '2026-10-02'
  author: Amish Chadha
  change: "Items 14, 16 and 18 decided by Amish on 2026-10-02"
---

# 0001: TRL 2 review decisions and interface v0.3

- **Date:** 2026-09-25
- **Status:** accepted (items 1 to 13; items 15, 17, 19 and 20 accepted later on 2026-09-25 in SWC-DDR-002); items 14, 16 and 18 decided by Amish on 2026-10-02 (SWC-DEC-001)

## Context

The TRL 2 review note (`docs/REVIEW.md`, session 2026-09-24) listed eleven items as "Proposed, awaiting Amish", most with a recommendation. On 2026-09-25 Amish reviewed the review points for every portfolio repo and wrote: "proceed with all of your recommendations across all batches. Make sure we don't proceed to TRL 4 on any of them." He also approved three cross-cutting additions to the SwapCell interface, raised by the PowerBox, StepGen, SunSpoke, WaterWalker and CargoMule designs, and a portfolio pricing rule for shared packs.

This record lists what that instruction decides, and what it leaves open because there was no recommendation to accept. TRL 4 is on hold by Amish's instruction.

## Options considered

The options for each item are in `docs/REVIEW.md` (2026-09-24) and SWC-PRC-001 v0.2. They are not repeated here.

## Decision

Table 1 lists the decided items. Each is "Decided by Amish, 2026-09-25: go with recommendation" unless the row says otherwise.

*Table 1. Decided items.*

| # | Item | Decision | Where it now lives |
| --- | --- | --- | --- |
| 1 | Cell configuration | Decided by Amish, 2026-09-25: go with recommendation. 13S2P of 5 Ah 21700 cells as the reference pack; 13S4P "double" pack only as a later variant in a longer envelope | SWC-PRC-001 v0.3, SWC-REQ-001 v0.3 |
| 2 | Housing | Decided by Amish, 2026-09-25: go with recommendation. Folded aluminium tray with a printed flame-retardant lid and caps | SWC-PRC-001 v0.3, SWC-DWG-002 |
| 3 | Interface v0.2 as written | Decided by Amish, 2026-09-25: go with recommendation. Envelope, 2 power plus 6 signal contacts with a last-mate interlock, CAN 2.0B at 250 kbit/s with 11-bit IDs. Superseded in the same session by v0.3 (items 11 to 13), which keeps every v0.2 feature | SWC-PRC-001 v0.3, interface section |
| 4 | Message set | Decided by Amish, 2026-09-25: go with recommendation. Open SwapCell profile now, with an EnergyBus (CiA 454) gateway study | SWC-PRC-001 v0.3. The gateway study is not complete; see item 18 |
| 5 | Legacy mode for non-CAN vehicles | Decided by Amish, 2026-09-25: go with recommendation. Discharge only, fixed at 15 A, never charge | SWC-PRC-001 v0.3 behavior rules, SWC-REQ-001 R13 |
| 6 | State-of-health log | Decided by Amish, 2026-09-25: go with recommendation. Log stored in the pack and read by any dock; no cloud dependency | SWC-REQ-001 R12 |
| 7 | Dock charger | Decided by Amish, 2026-09-25: go with recommendation. Dock switches a certified 5 A charger; no custom mains electronics | SWC-PRC-001 v0.3 |
| 8 | Fleet charge mode | Decided by Amish, 2026-09-25: go with recommendation. 4.1 V per cell (53.3 V) mode, selected by the dock | SWC-PRC-001 v0.3, SWC-REQ-001 R9 |
| 9 | Interface governance | Decided by Amish, 2026-09-25: go with recommendation. A versioned interface section in this repo; changes approved by Amish; dependent designs build to it and flag conflicts to this repo | SWC-PRC-001 v0.3 |
| 10 | Budget | Decided by Amish, 2026-09-25: go with recommendation. Keep `budget_usd: 700` for TRL 3; it covers one pack and one dock | `project.yaml`, SWC-REQ-001 R16 |
| 11 | Interface addition W: wake for hosts without CAN or a wake supply | Decided by Amish, 2026-09-25 (cross-cutting approval): add a wake method. Implemented in v0.3 as wake on a coded INTERLOCK loop, with a manual wake button; the WAKE pin stays optional | SWC-PRC-001 v0.3, SWC-REQ-001 R13 |
| 12 | Interface addition C: charge-while-discharging mode | Decided by Amish, 2026-09-25 (cross-cutting approval): add the mode. Implemented in v0.3 as requested mode 4 (charge-discharge) for dock, station and vehicle hosts | SWC-PRC-001 v0.3, SWC-REQ-001 R14 |
| 13 | Interface addition V: latch vibration rating for vehicles | Decided by Amish, 2026-09-25 (cross-cutting approval): add a rating. Implemented in v0.3 as latch class V1 for vehicle receivers and class D for gravity docks | SWC-PRC-001 v0.3, SWC-REQ-001 R15 |

Two further approvals from the same instruction are recorded here:

- **Shared packs are priced once.** Decided by Amish, 2026-09-25 (cross-cutting): a SwapCell pack is priced in this repo only and excluded from each dependent kit budget. Recorded in SWC-REQ-001 R16 and `bom/bom-notes.md`.
- **Solar DC dock variant.** Decided by Amish, 2026-09-25: go with recommendation (SWC-PRC-001 v0.2 open questions). A second dock variant with a 48 V DC solar input, via PowerBox, follows the mains dock. It is not designed at TRL 3.

### Items that remain open

These had no recommendation, or the recommendation was to decide later, so they stayed **Proposed, awaiting Amish** in v0.1. On 2026-09-25 Amish accepted all remaining recommendations (SWC-DDR-002); the status column below is updated. Items with no recommendation stay open.

*Table 2. Open items.*

| # | Item | Status |
| --- | --- | --- |
| 14 | First co-design partner (repair workshop, delivery fleet or rural e-bike cooperative) | Decided by Amish, 2026-10-02: kept open under the portfolio rule, but an urban cargo-bike or e-bike delivery fleet is approached first, with a repair workshop second |
| 15 | Build budget for a second pack before any build (about $900 at TRL 2; about $973 for two packs and one dock with the TRL 3 prices) | Decided by Amish, 2026-09-25: go with recommendation. Keep $700 for TRL 3 and set the build budget before any build. On hold: TRL 4 is on hold (SWC-DDR-002) |
| 16 | LFP variant (16S) sharing the envelope and message set | Decided by Amish, 2026-10-02: not added now; a chemistry code and a coding key are reserved so an LFP pack can never take an NMC charge or the reverse |
| 17 | Connector family | Decided by Amish, 2026-09-25: go with recommendation. Custom keyed shroud with commercial high-current socket contacts and potted signal contacts (SWC-DDR-002) |
| 18 | EnergyBus gateway detail | Decided by Amish, 2026-10-02: deferred; the native SwapCell profile stays the reference and CiA 454 is read only when a partner needs EnergyBus. Previously: The message-by-message mapping needs the CiA 454 specification, which is distributed through a membership organization and was not read in this session |
| 19 | Values chosen inside the approved additions W, C and V (10 kΩ coded interlock, 100 µA sleep limit, 25 g shock level, 330 N receiver preload, charge-FET fallback rule) | Decided by Amish, 2026-09-25: go with recommendation. Values confirmed as proposed (SWC-DDR-002) |
| 20 | R3 thermal rating: keep 20 A continuous with temperature derating, or derate the label to 15 A | Decided by Amish, 2026-09-25: go with recommendation. Keep 20 A at 25 °C with the PACK_LIMITS derating; R3 restated (SWC-DDR-002) |

## Consequences

- SwapCell interface **v0.3** is issued in SWC-PRC-001 v0.3. It keeps every v0.2 signal, message and rule, so a v0.2 host that drives WAKE and sends a heartbeat needs only the change in the next point; v0.3 hosts can also wake a pack with no supply of their own.
- Every v0.3 receiver must fit a 10 kΩ coding resistor in its INTERLOCK loop (a direct link to SGND is no longer valid). This is the one change a v0.2 receiver design must make.
- Dependent designs (PowerBox, SunSpoke, StepGen, WaterWalker, CargoMule and others) cite these as "SwapCell interface v0.3" items W, C and V.
- SWC-PRB-001, SWC-PRC-001 and SWC-REQ-001 move to v0.3. TRL is set to 3. No TRL 4 work is started.
