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
