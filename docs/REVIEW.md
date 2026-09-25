# Review note: SwapCell

## Session 2026-09-24: /populate to a strong TRL 2

### What was done

- `docs/01-problem.md` (SWC-PRB-001 v0.2): problem, users and context (fleets, rural users, repair shops, builders, portfolio integrators), constraints, out of scope, prior work described without links.
- `docs/03-requirements.md` (SWC-REQ-001 v0.2): 12 measurable requirements (R1 to R12) with targets and planned verification. R6, R10 and R12 are the interface requirements.
- `docs/02-concept.md` (SWC-PRC-001 v0.2): how it works, components table, first-order numbers with assumptions, interface definition (mechanical envelope, 8-contact pinout, CAN message set outline and behavior rules), design choices, safety, open questions.
- `cad/src/concept_media.py`: massing model of the pack (tray, 26-cell block, BMS, lid, plug, handle, latch) seated in the wall dock (cradle, receptacle, charger, controller), with a wall and hand for scale.
- `media/`: hero, blueprint sheet SWC-DWG-001 (PNG, PDF, SVG), cutaway, exploded view with BOM callouts 1 to 11, energy flow diagram with estimates, `model.glb` and `viewer.html`.
- `bom/bom.csv`: 13 lines with indicative prices, numbered to match the exploded view; `bom/bom-notes.md`.
- `README.md`: hero image and media links above "Problem".
- `docs/pdf/`: branded PDFs of the three controlled documents.

### Key results (estimates, to be checked at TRL 3)

| Quantity | Estimate | Requirement |
| --- | --- | --- |
| Configuration | 13S2P, 26 x 21700 at 5.0 Ah | |
| Voltage and energy | 46.8 V nominal, 10 Ah, about 468 Wh | R1, R2 met |
| Cell current | 10 A continuous, 17.5 A peak per cell (rated 25 A) | R3 electrically met |
| Temperature at 20 A full discharge | about 61 °C from 25 °C (adiabatic, 44 W) | R3 **at risk** |
| Mass | about 2.8 kg | R5 met |
| Body | 340 x 90 x 80 mm; about 393 mm overall | R6 met |
| Charge time at 5 A | about 2.3 h full, 1.2 h for 20 to 80 % | R4 met |
| Energy per cycle | about 550 Wh in, 454 Wh at pack terminals | |
| Parts cost | about $370 per pack, $145 per dock, $515 total | Within $700 |

Requirements not met or at risk:

- **R3 (thermal):** 20 A continuous for a full discharge reaches about 61 °C in the adiabatic worst case, just over the 60 °C target, and would fail from 45 °C ambient. Either derate to about 15 A continuous or show heat loss through the aluminium tray at TRL 3.
- **R9 (cycle life):** typical 5 Ah 21700 cells give about 300 to 500 cycles to 80 %, so 500 cycles is at risk without a 4.1 V fleet charge mode or a longer-life cell.
- **R7, R8, R10:** cannot be judged until a connector family and seals are chosen; no known conflict.

### Proposed, awaiting Amish

1. Cell configuration: 13S2P of 5 Ah 21700 cells (recommended). Alternatives: 13S3P of 18650 cells, or 13S4P of 21700 (about 5 kg) as a later "double" variant.
2. Housing: aluminium tray with a printed flame-retardant lid (recommended), or all-printed.
3. Interface v0.2 as written in SWC-PRC-001: envelope 340 x 90 x 80 mm, 2 power plus 6 signal contacts with a last-mate interlock, CAN 2.0B at 250 kbit/s with 11-bit IDs.
4. Message set: an open SwapCell profile now with an EnergyBus (CiA 454) gateway study at TRL 3 (recommended), or adopt EnergyBus directly.
5. Legacy mode for non-CAN vehicles: discharge only at 15 A (recommended), or CAN always required.
6. State-of-health log stored in the pack and read by any dock; no cloud dependency.
7. Dock switches a certified 5 A charger; no custom mains electronics.
8. Fleet charge mode at 4.1 V per cell, selectable by the dock.
9. Interface governance: a versioned interface section in this repo, changes approved by Amish, which SunSpoke, PowerBox, FieldCell and WaterWalker build to.
10. First co-design partner: a repair workshop (recommended), a delivery fleet or a rural e-bike cooperative.
11. Budget: $700 in `project.yaml` is kept and covers one pack and one dock. A second pack for a real swap demonstration would raise the parts total to about $885. Proposed: keep $700 for TRL 3 (paper work only) and decide on about $900 before any build. Awaiting Amish.

### Safety concerns

- 470 Wh lithium-ion pack: thermal runaway and propagation between cells is the main hazard. Cell spacing, barriers, venting and a flame-retardant liner are listed but not yet designed.
- Exposed connector contacts at up to 54.6 V DC with very high short-circuit current: the dead-output-until-interlock rule is essential and must survive the TRL 3 BMS specification.
- Sudden loss of power while riding: the warn-then-derate rule must be kept.
- Transport: the pack is above 100 Wh, so it is Class 9 dangerous goods (UN 3480 or 3481) and needs UN 38.3 testing before commercial shipping.
- Any future build and test must happen inside a fireproof enclosure, never unattended. No build work was started in this session.

### Recommended next step

Review this note, the interface section of SWC-PRC-001 and the media. If approved, run `/advance-trl3` to do the thermal model for R3, the cell selection for R9, the connector family selection for R10, the full CAN bit layout, and the parametric model and drawing sheet of the envelope. Share the interface section with the SunSpoke, PowerBox, FieldCell and WaterWalker repos only after Amish approves it.

## Session 2026-09-25: TRL 3

Amish's instruction for this session (2026-09-25): "proceed with all of your recommendations across all batches. Make sure we don't proceed to TRL 4 on any of them." He also approved three SwapCell interface additions (wake for hosts without CAN, charge-while-discharging mode, latch vibration rating for vehicles) and the rule that shared SwapCell packs are priced once. TRL 4 is on hold by his instruction.

### What was done

- `docs/decisions/0001-trl2-review-decisions.md` (SWC-DDR-001 v0.1): every decided item, the three v0.3 additions, and the items still open.
- `docs/02-concept.md` (SWC-PRC-001 v0.3): issues **SwapCell interface v0.3** (items W wake, C charge-discharge, V latch classes D and V1, L full CAN bit layout); decisions recorded; key numbers replaced with checked values; safety updated.
- `docs/03-requirements.md` (SWC-REQ-001 v0.3): status column; new R13 (wake), R14 (charge-discharge), R15 (latch class V1), R16 (budget scope and shared-pack pricing).
- `docs/01-problem.md` (SWC-PRB-001 v0.3): dependents and their needs, budget scope, open questions.
- `docs/04-calcs/01-sizing.md` (SWC-CAL-001 v0.1) with `docs/04-calcs/sizing.py` and `results.csv`: electrical, mass, lumped thermal with heat loss, charging and energy chain, wake and sleep, charge-discharge, latch, connector, CAN load and log, cost, and the full requirement table.
- `cad/src/model.py`: parametric build123d model (interface dimensions as parameters) exporting `cad/step/swapcell-{pack,dock,assembly}.step` and matching STL files.
- `cad/src/sheets.py` and `cad/drawings/SWC-DWG-002.{svg,pdf,png}`: general arrangement at Rev P1, "CONCEPT, NOT FOR FABRICATION" and "PRELIMINARY, NOT FOR FABRICATION".
- `bom/bom.csv` (14 lines, all priced, with supplier types) and `bom/bom-notes.md`.
- `cad/src/concept_media.py` now builds from `model.py`; all media regenerated and checked by eye (hero, cutaway, exploded, flow, blueprint SWC-DWG-001, `model.glb`, `viewer.html`).
- `project.yaml`: `trl: 3`, `trl_target: 3`, evidence listed. `README.md`: TRL 3, key components, links.

### Requirements (SWC-CAL-001)

Not met: **none**. At risk: 3. Not verifiable at TRL 3: 5. Met: 8 (three of them on paper only).

| ID | Status | Value |
| --- | --- | --- |
| R3 | **At risk** | 51 °C open air at 20 A from 25 °C (56 °C with higher resistance); 63 °C enclosed; 71 °C from 45 °C ambient. About 14 A holds 60 °C from 45 °C |
| R9 | **At risk** | 300 to 500 cycles typical for the cell class; 4.1 V fleet mode is the mitigation |
| R2 | **At risk** | 10.0 Ah, 466 Wh nominal; 9.7 Ah, 452 Wh at the 4.85 Ah cell minimum |
| R7, R8, R10, R11, R15 | Not verifiable at TRL 3 | Insertion about 41 N (assumed contact forces); IP65 by design only; connector family not chosen; short-circuit 496 A, pre-charge 460 ms; latch proof 1.72 kN |
| R1, R4, R5, R6, R16 | Met | 46.8 V; 2.3 h full, 1.6 h to 80 %; 2.85 kg; 393 mm overall; $559 of $700 |
| R12, R13, R14 | Met on paper | CAN load 1.8 %; sleep drain 0.72 % per month; 3.8 A net charge in the PowerBox case |

Corrections to TRL 2 numbers: mass 2.8 to 2.85 kg, pack parts $370 to $414 (cell price $4.50 to $5.50, wake button added), energy chain 550/454 to 547/457 Wh, 0 to 80 % charge 1.6 h.

### Decisions recorded (SWC-DDR-001)

Decided by Amish, 2026-09-25, go with recommendation: 13S2P 21700 cells; aluminium tray with printed lid; interface v0.2 as written (superseded by v0.3); SwapCell message profile with an EnergyBus gateway study; legacy discharge-only mode at 15 A; SoH log in the pack; dock switches a certified 5 A charger; 4.1 V fleet mode; interface governance in this repo; `budget_usd` kept at $700 for one pack and one dock; solar DC dock variant later. Cross-cutting approvals: interface v0.3 items W, C and V, and shared packs priced once here.

### Still awaiting Amish

1. First co-design partner (left open by the portfolio rule).
2. Build budget of about $973 for two packs and one dock, only when TRL 4 is lifted.
3. LFP variant (no preference stated).
4. Connector family: recommended custom keyed shroud with commercial contacts.
5. Values chosen inside the approved additions: 10 kΩ coded INTERLOCK, 100 µA sleep, 25 g shock, 330 N receiver preload, charge-FET fallback.
6. R3: keep 20 A at 25 °C with temperature derating (recommended), or label 15 A.
7. EnergyBus mapping needs the CiA 454 specification, which was not read.

### For dependent repos

PowerBox, SunSpoke, StepGen, WaterWalker, CargoMule, FieldCell and others should cite "SwapCell interface v0.3" items W, C and V. The one change for any v0.2 receiver: fit a 10 kΩ coding resistor in the INTERLOCK loop instead of a direct link to SGND. Vehicle receivers must meet latch class V1 and leave the back and lid faces of the pack open to air (R3).

### Safety concerns

- 468 Wh lithium-ion pack; about 500 A available into a short. Thermal runaway and propagation are still not analyzed and can only be shown by test.
- R3: a pack enclosed tightly in a vehicle can exceed 60 °C at 20 A; derating in PACK_LIMITS is essential.
- The coded interlock stops a coin or wet debris from enabling the output, including in legacy mode. It must survive into any BMS firmware.
- Charge-discharge mode makes the host a charger; the pack must refuse charge below 0 °C and above 45 °C.
- A pack that leaves a vehicle mount is a heavy projectile with live contacts; latch class V1 is a safety item.
- Transport as Class 9 dangerous goods with UN 38.3 before any shipping. No build work was started.

### Notes against the standard

- The TRL change is recorded here and in SWC-DDR-001, not in `build-log/`, because new build-log entries would read as TRL 4 evidence.
- No TRL 4 material was found in the repo. `build-log/README.md` and the empty `electronics/` and `firmware/` folders were left untouched.
- No unchecked citations were listed, so no web verification was needed. BOM prices are estimates, not quotes.

### Recommended next step

Amish reviews SWC-DDR-001 items 14 to 20 and the interface v0.3 section of SWC-PRC-001, then approves v0.3 for circulation to the dependent repos. **TRL 4 is on hold by Amish's instruction.** For the record only, TRL 4 would need: a chosen cell model and connector family, a BMS configuration that implements the v0.3 wake, charge-discharge and interlock rules, a pack built and charged in a fireproof enclosure, lab test reports (TST, `environment: lab`) for capacity, temperature at 20 A, protections and latch class V1, build-log entries, and a build budget decision.
