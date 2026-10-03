---
doc_id: SWC-DEC-001
title: SwapCell design decisions register
project: SwapCell
doc_type: Design decisions register
version: "0.3"
status: Draft
date: '2026-10-02'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-10-01'
  author: Amish Chadha
  change: Register opened with the open items of SWC-DDR-001 to 003, the 2026-09-26 render review and the build plan work
- version: "0.2"
  date: '2026-10-02'
  author: Amish Chadha
  change: "Amish approved the recommendations for all open decisions 1 to 13 on 2026-10-02 (SWC-DDR-003 accepted; interface v0.4 handle zone and catch geometry; polycarbonate sheet lid; LFP code reserved; EnergyBus deferred); moved to decisions made"
- version: "0.3"
  date: '2026-10-02'
  author: Amish Chadha
  change: "Cost line updated for the polycarbonate sheet lid (USD 619, USD 81 under the target)"
---

# SwapCell design decisions register

Every design decision still to be made, and every decision made, in one place. Each decision is argued in full in its decision record under `docs/decisions/` or in the review note (`docs/REVIEW.md`); this register is the index Amish works from. The build plan (`docs/05-build-plan.md`) describes the design as it stands and does not list open decisions.

## Open decisions

None. All open decisions were decided on 2026-10-02.

## To confirm when parts are bought

| # | What to confirm | Why it matters | Source |
| --- | --- | --- | --- |
| 1 | The power and signal contact parts, their diameters and lengths | They set the hole sizes in the plug and receptacle shrouds and the mating order; R8 and R10 depend on them | SWC-DDR-002, SWC-DDR-003 |
| 2 | The cell model: diameter 21.0 to 21.2 mm, datasheet cycle life | The holder pockets are 21.2 mm; R9 stays at risk until a cell is named | SWC-DDR-001, SWC-CAL-001 |
| 3 | The battery management board's size (about 230 x 58 mm, 10 mm or less thick) and mounting holes | They set the four holes in the right side wall | SWC-DDR-003 |
| 4 | The wake button's depth behind the panel, 15 mm or less | The cells are 2.7 mm behind the modelled switch body | SWC-DDR-003 |
| 5 | The charger's size (modelled 150 x 64 x 110 mm) | The straps and their tapped holes are sized to it | SWC-DDR-003 |
| 6 | The controller box size (modelled 50 x 50 x 30 mm) | It must fit between the charger and the shelf retainer | SWC-DDR-003 |
| 7 | M3 press-in nuts rated for 1.5 mm 5052 aluminium | The lid's eight screws go into them | SWC-DDR-003 |

## Value engineering

Value-engineering target: USD 700 (a hypothetical control target, not a limit). Estimated cost of the constructable design: USD 619 (USD 81 under the target): USD 449 for the pack and USD 170 for the dock. Main cost drivers and savings worth trying:

- The largest lines are the 26 cells (USD 143), the battery management board (USD 120), the charger (USD 60), the plug and receptacle with their contacts (USD 60 together), the dock cradle (USD 40) and the fuses and wiring (USD 36).
- Making the design constructable added USD 47 (SWC-DDR-003): the latch housing, slider and springs (USD 10), the cell holder frames (USD 6, moved from the wiring line, which fell by USD 4), the dock mounting parts (USD 15), the longer back plate (USD 10), the tray flanges (USD 5) and more fixings (USD 5).
- Savings worth trying: a 6 mm back plate instead of 12 mm (about USD 10 and 1.5 kg less; the loads are small); cells and boards bought for several packs at once; printing the shelf and guides at lower infill; a stock enclosure-style charger with mounting ears, which would drop the straps.

## Decisions made

| Date | Decision | Decided by | Record |
| --- | --- | --- | --- |
| 2026-09-25 | TRL 2 review items 1 to 10: 13S2P of 5 Ah 21700 cells; aluminium tray with a printed flame-retardant lid; interface v0.2; SwapCell message profile with an EnergyBus gateway study; legacy discharge-only mode at 15 A; health log in the pack; dock switches a certified 5 A charger; 4.1 V fleet mode; interface governance in this repo; `budget_usd` kept at 700 | Amish: "proceed with all of your recommendations across all batches. Make sure we don't proceed to TRL 4 on any of them." | SWC-DDR-001 |
| 2026-09-25 | Interface v0.3 additions: wake for hosts without CAN (W), charge-while-discharging mode (C), latch vibration rating for vehicles (V); shared packs priced once, here | Amish, cross-cutting approval | SWC-DDR-001, items 11 to 13 |
| 2026-09-25 | Connector family (custom keyed shroud with commercial contacts); values inside W, C and V confirmed (10 kΩ coding, 100 µA sleep, 25 g shock, 330 N preload, charge-FET fallback); R3 kept at 20 A with temperature derating; build budget for a second pack set before any build | Amish: "i accept all your recommendations, go with them across all repos." | SWC-DDR-002 |
| 2026-09-25 | TRL 4 on hold for every repo | Amish: "Make sure we don't proceed to TRL 4 on any of them." | SWC-DDR-001, `docs/REVIEW.md` |
| 2026-09-30 | Make the design physically buildable while drawing the build plan | Amish: "If you are realising that the design cannot be built as per concept - fix the design assumptions to match and be physically feasible as you draw the illustrations." | SWC-DDR-003 (accepted on 2026-10-02, below) |
| 2026-09-30 | Open decisions are kept in this register, not in the build plan | Amish: "don't log outstanding decisions in this build plan - that is not the place for it. that should be in a separate design document logged and named as such" | This register |
| 2026-10-01 | `budget_usd` is a value-engineering target, not a limit | Amish: "the budgets are a hypothethical control target to ensure we are thinking along a value engineering lens. its ok to ensure wording reflects that the hypothesis budget was x - the real cost being accrued is y" | SWC-CAL-001 v0.3, this register |
| 2026-10-02 | Design for construction accepted: the changes P1 to P12 of SWC-DDR-003 and their knock-on changes, as made | Amish: "i approve your recommendations for all 555 open decisions." | SWC-DDR-003, Tables 1 and 2 |
| 2026-10-02 | Handle zone (option a): widened in interface v0.4 to 84 x 43 mm, from the zone's front edge to the back face, so receivers leave the thumb button clear | Amish: "i approve your recommendations for all 555 open decisions." | SWC-DDR-003, A1 |
| 2026-10-02 | Catch geometry (option a): published in interface v0.4 (latching face 1 mm above the pawl, 8 mm reach, 4 mm engagement, 6 mm pawl projection, 5 mm travel), so every receiver latches the same way | Amish: "i approve your recommendations for all 555 open decisions." | SWC-DDR-003, A2 |
| 2026-10-02 | Lid (option b) for the prototype: cut from 3 mm UL 94 V-0 polycarbonate sheet. This changes the printed-lid decision of 2026-09-25 (SWC-DDR-001, item 2) for the prototype; the drawing allows either | Amish: "i approve your recommendations for all 555 open decisions." | SWC-DDR-003, A3; SWC-DDR-001 |
| 2026-10-02 | Thermal path (option a): the 0.10 K/W core-to-tray assumption is kept and checked in the TRL 4 load test, with the battery board's temperature sensor placed on the rear row of cells, now furthest from the tray | Amish: "i approve your recommendations for all 555 open decisions." | SWC-DDR-003, A4 |
| 2026-10-02 | First co-design partner: kept open under the portfolio rule, but an urban cargo-bike or e-bike delivery fleet is approached first, with a repair workshop second | Amish: "i approve your recommendations for all 555 open decisions." | SWC-DDR-001, item 14 |
| 2026-10-02 | LFP variant: not added now; a chemistry code in the message set and a coding key are reserved so an LFP pack can never take an NMC charge or the reverse | Amish: "i approve your recommendations for all 555 open decisions." | SWC-DDR-001, item 16 |
| 2026-10-02 | EnergyBus gateway: deferred; the native SwapCell profile stays the reference, and CiA 454 is read only when a partner needs EnergyBus | Amish: "i approve your recommendations for all 555 open decisions." | SWC-DDR-001, item 18 |
| 2026-10-02 | Render pose: the lifted pose is kept for the hero render | Amish: "i approve your recommendations for all 555 open decisions." | `docs/REVIEW.md`, 2026-09-26, item 1 |
| 2026-10-02 | State-of-charge light bar accepted as an optional pack feature under line 14, outside the interface | Amish: "i approve your recommendations for all 555 open decisions." | `docs/REVIEW.md`, 2026-09-26, item 2 |
| 2026-10-02 | Dock status light accepted under line 11 | Amish: "i approve your recommendations for all 555 open decisions." | `docs/REVIEW.md`, 2026-09-26, item 3 |
| 2026-10-02 | Thumb release behind the handle accepted; it follows from decision 2 above | Amish: "i approve your recommendations for all 555 open decisions." | `docs/REVIEW.md`, 2026-09-26, item 4 |
| 2026-10-02 | Finish and colours (slate tray, light grey lid, graphite handle, teal accents) accepted as the reference look | Amish: "i approve your recommendations for all 555 open decisions." | `docs/REVIEW.md`, 2026-09-26, item 5 |
