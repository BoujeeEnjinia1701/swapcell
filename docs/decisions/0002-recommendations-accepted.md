---
doc_id: SWC-DDR-002
title: SwapCell recommendations accepted
project: SwapCell
doc_type: Design decision record
version: "0.2"
status: Draft
date: '2026-10-02'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-09-25'
  author: Amish Chadha
  change: Record Amish's acceptance of all remaining recommendations and what changed in the repo
- version: "0.2"
  date: '2026-10-02'
  author: Amish Chadha
  change: "Table 2 items 14, 16 and 18 recorded as decided by Amish on 2026-10-02"
---

# 0002: Recommendations accepted

- **Date:** 2026-09-25
- **Status:** accepted

## Context

After SWC-DDR-001, seven items were still listed as "Proposed, awaiting Amish" (SWC-DDR-001 items 14 to 20, `docs/REVIEW.md` session 2026-09-25). On 2026-09-25 Amish wrote: "i accept all your recommendations, go with them across all repos." Every open item that carried a recommendation is therefore decided, with the recommended option as the decision. Items with no recommendation stay open. TRL 4 remains on hold by Amish's instruction, so decisions that need a build, a test or a purchase are recorded but not carried out.

## Options considered

The options for each item are in SWC-DDR-001 Table 2, SWC-PRC-001 v0.3 and SWC-CAL-001 v0.1. They are not repeated here.

## Decision

*Table 1. Newly decided items. Each is "Decided by Amish, 2026-09-25: go with recommendation".*

| # (DDR-001) | Item | Decision | What changed in the repo |
| --- | --- | --- | --- |
| 17 | Connector family | Custom printed keyed shroud around commercial high-current socket contacts and potted spring signal contacts | SWC-PRC-001 v0.4 components table, design choices and open questions; SWC-REQ-001 v0.4 R10 verification note; `bom/bom.csv` item 5 note; SWC-CAL-001 v0.2 R10 value; SWC-DWG-002 note added (Rev P1 to P2). No geometry change: the model already showed a keyed shroud. Contact part selection and R8 and R10 verification are TRL 4 work, on hold |
| 19 | Values inside interface v0.3 items W, C and V | Confirmed as proposed: 10 kΩ coded INTERLOCK, 100 µA sleep limit, 25 g shock, 330 N receiver preload, charge-FET fallback on a charge-side fault | SWC-PRC-001 v0.4 interface note; SWC-REQ-001 v0.4 assumptions; SWC-CAL-001 v0.2 inputs table. Numbers unchanged |
| 20 | R3 thermal rating | Keep 20 A continuous at 25 °C with temperature derating in PACK_LIMITS, rather than a 15 A label | R3 restated in SWC-REQ-001 v0.4 (20 A in an open-air mount from 25 °C; derating elsewhere). New derating rule in SWC-PRC-001 v0.4: full current to 50 °C cell temperature, linear to 5 A at 60 °C; 35 A peak only below 50 °C. `sizing.py` now also computes the current that holds 60 °C enclosed (about 18.5 A) beside the 45 °C ambient case (about 14.0 A). R3 status: at risk to met on paper. SWC-DWG-002 note added |
| 15 | Build budget for a second pack | Keep `budget_usd: 700` for TRL 3 and set the build budget (about $973 for two packs and one dock) before any build | No change to `project.yaml`. Decided but on hold: purchasing is TRL 4 work. SWC-REQ-001 v0.4 R16 assumption and `bom/bom-notes.md` updated |

### Items still open

*Table 2. Items that stayed Proposed, awaiting Amish (no recommendation to accept); all three decided by Amish on 2026-10-02 (SWC-DEC-001).*

| # (DDR-001) | Item | Why still open |
| --- | --- | --- |
| 14 | First co-design partner (repair workshop, delivery fleet or rural e-bike cooperative) | Portfolio rule: partners are chosen per area later; no choice to accept |
| 16 | LFP variant (16S) | No preference stated |
| 18 | EnergyBus gateway mapping | Needs the CiA 454 specification, which was not read; no recommendation to accept |

## Consequences

- Requirement status (SWC-CAL-001 v0.2): not met, none; at risk, 2 (R2, R9; was 3); not verifiable at TRL 3, 5 (R7, R8, R10, R11, R15); met, 9 (R1, R3, R4, R5, R6, R12, R13, R14, R16; four on paper only).
- `budget_usd` stays at $700; the priced BOM is $559.
- SwapCell interface stays at v0.3. The derating rule is pack behavior inside PACK_LIMITS and needs no change in any receiver; the confirmed values match what dependent repos already cite.
- No cross-repo edits are needed. Dependent repos may note that the v0.3 values are now confirmed and that vehicle receivers should still leave the back and lid faces open to air to keep the full 20 A.
- `trl: 3` and `trl_target: 3` are unchanged. No TRL 4 work was started.
