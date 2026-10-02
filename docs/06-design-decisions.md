---
doc_id: SWC-DEC-001
title: SwapCell design decisions register
project: SwapCell
doc_type: Design decisions register
version: "0.1"
status: Draft
date: '2026-10-01'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-10-01'
  author: Amish Chadha
  change: Register opened with the open items of SWC-DDR-001 to 003, the 2026-09-26 render review and the build plan work
---

# SwapCell design decisions register

Every design decision still to be made, and every decision made, in one place. Each decision is argued in full in its decision record under `docs/decisions/` or in the review note (`docs/REVIEW.md`); this register is the index Amish works from. The build plan (`docs/05-build-plan.md`) describes the design as it stands and does not list open decisions.

## Open decisions

| # | Decision needed | Options | Recommendation | Affects in the build | Source |
| --- | --- | --- | --- | --- | --- |
| 1 | Accept the design-for-construction changes P1 to P12 (latch catch above the pawl, sliding pawl with a wedge release, cells moved 8 mm toward the lid, lid flanges and gasket, fixings throughout, floating receptacle, longer dock plate) | Accept; accept in part; revise | Accept | The whole build plan follows them | SWC-DDR-003, Table 1 |
| 2 | Thumb button outside the published handle zone (interface v0.3) | (a) widen the handle zone in interface v0.4 to 84 x 43 mm, back to the back face; (b) move the release forward under the grip with a lever | (a) | Release slider and button (build plan 3.4); every receiver must leave the space clear | SWC-DDR-003, A1 |
| 3 | Publish the catch geometry (latching face 1 mm above the pawl, 8 mm reach, 4 mm engagement, 6 mm pawl projection, 5 mm travel) | (a) add it to interface v0.4; (b) leave it to each receiver | (a) | Latch catch (3.12); vehicle receivers in PowerBox, CargoMule and others | SWC-DDR-003, A2 |
| 4 | Lid process: Amish decided a printed lid on 2026-09-25, but 340 mm needs a large-format printer | (a) print on a printer with a 350 mm bed; (b) cut from 3 mm UL 94 V-0 polycarbonate sheet | (b) for the prototype | Pack lid (3.8) | SWC-DDR-003, A3 |
| 5 | Thermal path with the cells clear of the back wall | (a) keep the 0.10 K/W core-to-tray assumption and check it in the TRL 4 load test, with the derating rule as protection; (b) add a thermal pad now | (a) | Cell block (3.6) | SWC-DDR-003, A4 |
| 6 | First co-design partner | Repair workshop, delivery fleet, rural e-bike cooperative | None (portfolio rule: partners are chosen per area later) | Not part of the TRL 3 build | SWC-DDR-001, item 14 |
| 7 | LFP variant (16S, about 51 V) sharing the envelope and message set | Add as a variant; do not add | None stated | Not part of the TRL 3 build | SWC-DDR-001, item 16 |
| 8 | EnergyBus gateway mapping | Map message by message once the CiA 454 specification is read | None until the specification is read | Dock controller firmware, later | SWC-DDR-001, item 18 |
| 9 | Render pose: pack shown lifted 110 mm, part way through a swap | Keep the lifted pose; show it seated | Keep the lifted pose for the hero | Renders only | `docs/REVIEW.md`, 2026-09-26, item 1 |
| 10 | State-of-charge light bar shown in the renders, not in the interface or the BOM | Accept as an optional pack feature under line 14, outside the interface; remove from the renders | Accept as optional | Not in the prototype build | `docs/REVIEW.md`, 2026-09-26, item 2 |
| 11 | Dock status light shown in the renders | Accept under line 11; remove from the renders | Accept under line 11 | Controller box (bought), later | `docs/REVIEW.md`, 2026-09-26, item 3 |
| 12 | Thumb release shown as a tab behind the handle | Accept the position | Accept: the constructable design puts the button there | Release slider and button (3.4) | `docs/REVIEW.md`, 2026-09-26, item 4 |
| 13 | Finish and colours (slate tray, light grey lid, graphite handle, teal accents) | Accept as the reference look; change | Accept | None at TRL 3 | `docs/REVIEW.md`, 2026-09-26, item 5 |

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

Value-engineering target: USD 700 (a hypothetical control target, not a limit). Estimated cost of the constructable design: USD 606 (USD 94 under the target): USD 436 for the pack and USD 170 for the dock. Main cost drivers and savings worth trying:

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
| 2026-09-30 | Make the design physically buildable while drawing the build plan | Amish: "If you are realising that the design cannot be built as per concept - fix the design assumptions to match and be physically feasible as you draw the illustrations." | SWC-DDR-003 (Draft, open for review) |
| 2026-09-30 | Open decisions are kept in this register, not in the build plan | Amish: "don't log outstanding decisions in this build plan - that is not the place for it. that should be in a separate design document logged and named as such" | This register |
| 2026-10-01 | `budget_usd` is a value-engineering target, not a limit | Amish: "the budgets are a hypothethical control target to ensure we are thinking along a value engineering lens. its ok to ensure wording reflects that the hypothesis budget was x - the real cost being accrued is y" | SWC-CAL-001 v0.3, this register |
