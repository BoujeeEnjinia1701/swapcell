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

## Session 2026-09-25: recommendations accepted

Amish's instruction (2026-09-25, in chat): "i accept all your recommendations, go with them across all repos." Every open item with a recommendation is now **Decided by Amish, 2026-09-25: go with recommendation**, recorded in `docs/decisions/0002-recommendations-accepted.md` (SWC-DDR-002 v0.1). TRL 4 remains on hold.

### Decisions applied and what changed

| Item (SWC-DDR-001 #) | Decision | Before | After |
| --- | --- | --- | --- |
| 20, R3 thermal rating | Keep 20 A at 25 °C with PACK_LIMITS temperature derating | R3 "20 A from 25 °C ambient", **at risk** (51 °C open air, 63 °C enclosed) | R3 restated: 20 A in an open-air mount from 25 °C; elsewhere derate (full to 50 °C cell temperature, linear to 5 A at 60 °C). Sustained current about 18.5 A enclosed, 14.0 A from 45 °C. **Met on paper** |
| 17, connector family | Custom keyed shroud with commercial contacts | "Proposed, awaiting Amish" | Decided; contact parts chosen at supplier selection (TRL 4, on hold). No geometry change |
| 19, values inside W, C, V | Confirmed as proposed | 10 kΩ, 100 µA, 25 g, 330 N, charge-FET fallback awaiting confirmation | Same values, confirmed |
| 15, build budget | Keep $700 at TRL 3; set the build budget (about $973) before any build | Open | Decided, on hold with TRL 4. `budget_usd` unchanged at $700 |

Files changed: SWC-PRC-001 v0.3 to v0.4 (derating rule, connector decision, confirmed values, open questions); SWC-REQ-001 v0.3 to v0.4 (R3 restated, R10 note, assumptions); SWC-CAL-001 v0.1 to v0.2 and `docs/04-calcs/sizing.py` (new enclosed derating current, R3 status, R10 value; `results.csv` regenerated); SWC-DDR-001 v0.1 to v0.2 (items 15, 17, 19 and 20 marked decided); `bom/bom.csv` item 5 note; `bom/bom-notes.md`; SWC-DWG-002 Rev P1 to P2 (notes for connector and R3 derating; geometry unchanged); `project.yaml` evidence list; `README.md` new sections "Concept rationale", "Burning platform", "Where it could be used" and "What sparked the idea". STEP, STL, drawing, concept media and all PDFs regenerated, with designmolecule.com in the footers.

### Requirement status (SWC-CAL-001 v0.2)

Not met: **none**. At risk: 2 (was 3). Not verifiable at TRL 3: 5. Met: 9 (four on paper only).

| ID | Status | Value |
| --- | --- | --- |
| R2 | **At risk** | 10.0 Ah, 466 Wh nominal; 9.7 Ah, 452 Wh at the cell minimum |
| R9 | **At risk** | 300 to 500 cycles typical; 4.1 V fleet mode is the mitigation |
| R7, R8, R10, R11, R15 | Not verifiable at TRL 3 | Need hardware and test (TRL 4, on hold) |
| R1, R4, R5, R6, R16 | Met | Unchanged; $559 of $700 |
| R3, R12, R13, R14 | Met on paper | R3 51 °C open air (56 °C with higher resistance), derating elsewhere |

### Still awaiting Amish

1. First co-design partner (no recommendation; portfolio rule).
2. LFP variant (no preference stated).
3. EnergyBus gateway mapping (needs the CiA 454 specification; no recommendation).

### Cross-repo actions

None required. The interface stays v0.3 and the confirmed values match what dependent repos cite. For information only: PowerBox, SunSpoke, StepGen, WaterWalker, CargoMule and FieldCell vehicle or station receivers keep the full 20 A only if they leave the back and lid faces of the pack open to air; in an enclosed mount the pack now derates itself to about 18.5 A.

### TRL

`trl: 3` and `trl_target: 3` unchanged. **TRL 4 remains on hold by Amish's instruction.** No build, test, purchase, PCB or firmware work was started.

## Session 2026-09-26: product appearance model and photoreal renders

Amish chose this repo for the first batch of product renders on 2026-09-26. This session added a product appearance model for photoreal renders; the massing model, BOM and documents are unchanged.

### What was done

- New `cad/src/product_model.py`: `product_parts()` (53 parts in the groups shell, internal and context), `TITLE` and `RENDER_VIEWS` (hero, exploded and a detail view without the wall). All main dimensions and interfaces come from `PARAMS` in `cad/src/model.py`.
- Pack: folded tray with 6 mm bend radii and rounded ends, lid with a parting-line groove and six M3 screws, flush teal wake button with a ring mark, interface label and wordmark, rating label on the side, latch doubler rivets, carry handle with a ribbed rubber grip, steel latch pawl with a teal thumb release, keyed plug shroud with visible power and signal contacts.
- Pack internals: 26 cells with wraps and end caps, cell holders, nickel strips, BMS board with FETs, heatsink, connectors, capacitors and main fuse, and the two power leads to the plug.
- Dock: brushed back plate with wall screws, cradle shelf with a wordmark, side guides with lead-in chamfers, steel latch catch, receptacle with mating contacts in the pocket, finned charger with a status light, cable gland and mains cord, controller box with a parting line, status light and microSD slot.
- Context: a compact painted wall section and a cord grommet.
- `README.md`: hero image now points to `media/render-hero.png`, with a link to `media/render-exploded.png`. The render files are produced separately.

### Differences from model.py (appearance only)

1. **Render pose.** The pack is shown lifted 110 mm above its seated position, still between the guides, to show a swap in progress; model.py shows it seated. Proposed, awaiting Amish. Recommendation: keep the lifted pose for the hero, since it shows the receptacle and the guides.
2. **State-of-charge light bar.** A five-segment light bar behind a clear lens below the wake button, lit by the wake button press. It is not in interface v0.3 or the BOM. Proposed, awaiting Amish. Recommendation: accept as an optional pack feature under BOM item 14, outside the interface, or remove it from the renders.
3. **Dock status light.** A light strip on the front of the cradle shelf, driven by the dock controller; not in the BOM. Proposed, awaiting Amish. Recommendation: accept under BOM item 11.
4. **Thumb release.** Shown as a small ribbed tab on the pack top behind the handle; the precis says only "thumb release under the handle". Proposed, awaiting Amish. Recommendation: accept the position for the renders; the mechanism stays undefined at TRL 3.
5. **Finish and colours.** Tray painted slate grey, lid light grey, handle graphite with a black rubber grip, teal accents, printed labels and wordmarks. Proposed, awaiting Amish. Recommendation: accept as the reference look.

### TRL

This is an appearance model only: no tolerances, fabrication detail, PCB layouts or build work. `trl: 3` is unchanged and **TRL 4 remains on hold by Amish's instruction.**

## Session 2026-09-27: kit 1.5.0 and image quality

- Kit 1.5.0 synced: STANDARDS v1.5 (sections 12 to 15: product renders, storefront images and image quality, public release, authorship and signing), `.kit/cards.py`, `.kit/image_qc.py`, `.kit/release_gate.py`, issue templates, and the `/render-product` and `/release` commands. `CLAUDE.md` now matches `.kit/CLAUDE.md`.
- Every `media/render-*.png` recaptioned from its original render with the new layout: the title, concept label and repository sit in a band above the render and the view note in a band below it, each line wrapped to the image width, so no text overlaps other text or the render or runs off the image. `media/card.png` and `media/social-preview.png` regenerated with the same rules.
- `python .kit/image_qc.py` and `python .kit/release_gate.py` pass. trl stays 3.

## Session 2026-10-01: constructable design and prototype build plan (kit 1.7.0)

Amish's instructions: approve the build plan format and extend it to every repo (2026-09-30), keep open decisions out of the build plan and in a separate register (2026-09-30), make the design physically buildable while drawing the illustrations (2026-09-30), and treat `budget_usd` as a value-engineering target (2026-10-01). TRL stays 3; TRL 4 remains on hold. Nothing was built or bought.

### What was done

- Kit 1.7.0 installed (`.kit/`, `.claude/commands/`); `CLAUDE.md` replaced by `.kit/CLAUDE.md`.
- Constructability review of `cad/src/model.py` with build123d: the old model had the receptacle inside the solid shelf (25,000 mm³ overlap), the guides and controller box floating off the back plate, the controller 35 mm past the plate's edge, the latch catch below the pawl, and no fixing for the lid, plug, handle, cells, BMS, charger, shelf or guides.
- `cad/src/model.py` rewritten: every component built as made or bought, with its fixings; `python cad/src/model.py --check` runs 71 constructability checks, all passing. STEP and STL regenerated.
- New decision record `docs/decisions/0003-design-for-construction.md` (SWC-DDR-003, Draft, open for Amish's review).
- `bom/bom.csv`: lines 1, 4 to 9 and 11 to 13 updated; lines 15 (latch housing, release slider and springs), 16 (cell holder frames) and 17 (dock mounting parts) added. `bom/bom-notes.md` updated.
- Calculations re-run (`docs/04-calcs/sizing.py`, `results.csv`): SWC-CAL-001 v0.3, SWC-REQ-001 v0.5, SWC-PRC-001 v0.5 updated for mass, thermal, cost and the latch.
- General arrangement SWC-DWG-002 Rev P3; concept media regenerated (`media/hero.png`, `cutaway.png`, `exploded.png`, `flow.png`, `concept-blueprint.*`, `model.glb`, `viewer.html`).
- `cad/src/build_plan_media.py` (uses `.kit/build_views.py`): overview, 15 making sketches (`cad/drawings/SWC-DWG-101` to `115`), 9 joint close-ups, 17 assembly step pictures and a block wiring diagram in `docs/05-build-plan/`.
- `docs/05-build-plan.md` (SWC-BLD-001 v0.1) and `docs/06-design-decisions.md` (SWC-DEC-001 v0.1) written; both added to `trl_evidence`; `design_state: constructable` in `project.yaml`; README links line and "Building the prototype" section added.

### Design changes made for construction (SWC-DDR-003)

1. Latch catch moved from 2 mm below the pawl to 1 mm above it, as a separate steel bar on two M5 screws, so the pawl hooks 4 mm under it.
2. Pawl redesigned: 6 mm proud (was 10), sliding in a riveted 1.5 mm steel housing (the latch doubler), pushed out by two springs and pulled in 5 mm by a ramped release slider under a thumb button just behind the grip.
3. Cell block moved 8 mm toward the lid to make room for the latch, held in two printed holder frames on the back wall.
4. Tray given 8 mm inward front flanges with eight M3 press-in nuts; lid on a 1 mm flat gasket with eight countersunk screws; tray 1 mm shallower so the body stays 80 mm deep.
5. Plug shroud fixed by four M3 screws from inside, with a 42 x 22 mm lead opening; contacts fitted through it.
6. Handle fixed by two M5 screws from inside into heat-set inserts.
7. BMS on four standoffs with countersunk screws through the right side wall.
8. Receptacle moved out of the solid shelf into a cavity under the pocket, captured by its flange on a foam pad and retainer plate, floating 3 mm each way; key post moved to the receptacle.
9. Side guides extended back to the plate and screwed from behind; 10 mm lead-in modelled.
10. Shelf and catch screwed from behind the plate.
11. Controller box moved onto the plate between the charger and the shelf.
12. Charger held by two folded straps; back plate lengthened from 520 to 580 mm.

### Key results

- Constructability checks: 71 of 71 pass.
- Pack mass 3.03 kg (was 2.85 kg); R5 (3.5 kg) still met. Energy density 154 Wh/kg.
- Thermal: hot spots unchanged (51, 63, 71 °C); enclosed derating current 18.6 A (was 18.5 A).
- Cost: value-engineering target USD 700; estimated cost of the constructable design USD 606 (USD 94 under the target); pack USD 436, dock USD 170.
- Requirement status unchanged: none not met; R2 and R9 at risk; R7, R8, R10, R11 and R15 not verifiable at TRL 3.
- Published interface values unchanged.

### Proposed, awaiting Amish

All listed in `docs/06-design-decisions.md`: acceptance of SWC-DDR-003; widening the handle zone to cover the thumb button (interface v0.4); publishing the catch geometry (interface v0.4); lid cut from V-0 sheet instead of printed; keeping the thermal assumption with the cells off the back wall; and the items carried over (co-design partner, LFP variant, EnergyBus mapping, the five render appearance items of 2026-09-26).

### Stale, to regenerate on Amish's Mac

`media/render-hero.png`, `media/render-exploded.png`, `media/render-detail.png`, `media/card.png` and `media/social-preview.png` still show the concept (six lid screws, a 10 mm pawl, guides off the plate, a shorter back plate, no charger straps). `cad/src/product_model.py` reads its sizes from the model and was not edited; it renders the 6 mm pawl from the new parameters.

### Safety concerns

- Unchanged hazards: 468 Wh lithium-ion pack, about 500 A into a short; thermal runaway not analyzed. The build plan carries seven safety stops, including building, charging and testing only inside a fireproof enclosure, never unattended.
- The latch now retains the pack in the dock (class D). Class V1 vehicle retention still needs the TRL 4 vibration test.
- Every screw and rivet head on the pack's published faces is countersunk, so nothing can snag a receiver or short against it.

### Recommended next step

Amish reviews SWC-DDR-003 and the register items 1 to 5. If accepted, issue interface v0.4 with the handle-zone and catch clarifications and tell the dependent repos. TRL 4 remains on hold.

## Session 2026-10-02: open decisions decided

On 2026-10-02 Amish approved the recommendations for every open decision: "i approve your recommendations for all 555 open decisions." The 13 open decisions of the design decisions register are now in its Decisions made table, dated 2026-10-02.

SWC-DDR-003 (design for construction) is accepted, with A1 to A4 decided as recommended. The SwapCell interface is issued as v0.4 in SWC-PRC-001: the handle zone is 84 x 43 mm, the catch geometry is published, and a chemistry code and coding key are reserved for a future LFP variant. A3 changes Amish's printed-lid decision of 2026-09-25 for the prototype (review flag 2): the lid is cut from 3 mm UL 94 V-0 polycarbonate sheet. Items 14, 16 and 18 of SWC-DDR-001 are recorded as decided. Item 12 was decided with item 2 (review flag 1).

### Documents changed

- `docs/06-design-decisions.md` (SWC-DEC-001 v0.2)
- `docs/decisions/0003-design-for-construction.md` (SWC-DDR-003 v0.2)
- `docs/decisions/0001-trl2-review-decisions.md` (SWC-DDR-001 v0.3)
- `docs/decisions/0002-recommendations-accepted.md` (SWC-DDR-002 v0.2)
- `docs/01-problem.md` (SWC-PRB-001 v0.4)
- `docs/02-concept.md` (SWC-PRC-001 v0.6)
- `docs/03-requirements.md` (SWC-REQ-001 v0.6)
- `docs/05-build-plan.md` (SWC-BLD-001 v0.2)
- `bom/bom-notes.md` (not a controlled document)
- `README.md` (not a controlled document)

### Follow-up actions to carry approved decisions into the design

1. Decision 2: Drawings: show the 84 x 43 mm handle zone on the interface drawing and on SWC-DWG-001.
2. Decision 3: Drawings: add the catch geometry (latching face, reach, engagement, pawl projection and travel) to the interface drawing and the dock catch making sketch.
3. Decision 2: Ask the repos that build to the interface to move from v0.3 to v0.4 and check their receivers leave the wider handle zone clear and use the published catch geometry (cargomule, cellguard, coldpod, culvertcrawl, dewdrive, dockhub, dustrunner, fieldcell, flattrike, lumaflow, motioncore, powerbox, stepclimber, stepgen, sunspoke, wastewise-scan, waterwalker, waterwatch, zeerbox).
4. Decision 2: Firmware: report interface minor version 4 in PACK_STATUS when the firmware is written or next changed.
5. Decision 4: BOM: change line 4 to 3 mm UL 94 V-0 polycarbonate sheet, with a sheet supplier and price; drop the large-format printer note.
6. Decision 4: Drawings: make SWC-DWG-108 name polycarbonate sheet as the prototype material.
7. Decision 5: Model and build plan pictures: show the battery board's temperature sensor on the rear row of cells in the wiring figure.
8. Decision 7: Calculations and message set: assign the reserved LFP chemistry code value and the connector coding key geometry when an LFP variant is designed; add the key to the model then.
9. Decision 1: Renders: regenerate the photoreal renders, `media/card.png` and `media/social-preview.png` on Amish's Mac to show the accepted design (eight lid screws, 6 mm pawl, longer back plate, charger straps); items 9 to 13 follow with them.

### Points found in the review

1. Item 12 duplicates item 2: if item 2 is approved as (a), item 12 is decided with it.
2. Item 4 reverses a decision Amish already made (printed lid, 2026-09-25); the register should say so rather than treat it as new.

No CAD model, BOM quantity or price, calculation result or picture was changed. TRL stays at 3; TRL 4 remains on hold.

## Session 2026-10-02: approved follow-ups carried out

Amish approved on 2026-10-02 that every follow-up action from the open-decision sign-off be carried out ("APPROVED CHANGES, COMPLETE THESE"). Status of the nine follow-ups listed above:

1. Handle zone on the interface drawing and SWC-DWG-001: done. The general arrangement SWC-DWG-002 (Rev P4) now carries Detail A, the 84 x 43 mm handle zone on the top end with the handle and thumb button inside it, and its interface notes are headed v0.4. The concept blueprint SWC-DWG-001 key figures name interface v0.4 and the 84 x 43 mm zone. The model has a check that the handle, thumb button and screws above the top end lie inside the zone.
2. Catch geometry on the interface drawing and the catch making sketch: done. SWC-DWG-002 Rev P4 Detail B shows the latching face 1 mm above the pawl, 8 mm reach, 4 mm engagement, 6 mm pawl projection and 5 mm travel; SWC-DWG-112 Rev P2 lists the same sizes; the build plan's catch section states them. Three model checks hold the published values.
3. Ask the receiver repos to move to v0.4: not done here; outreach and work in other repos (listed under Cross-repo actions below).
4. Firmware to report interface minor version 4 in PACK_STATUS: not done; firmware is TRL 4 work and none is written yet.
5. BOM line 4: done. 3 mm UL 94 V-0 polycarbonate sheet cut to size by a plastics distributor, USD 25 (estimate: one cut piece of about 0.03 m² with a one-off cutting charge; was USD 12 of filament); the large-format printer note is dropped.
6. SWC-DWG-108 names polycarbonate sheet: done (Rev P2).
7. Board temperature sensor on the rear row of cells in the model and the wiring figure: done. The model has the sensor on the middle cell of the rear row, with three new checks (on the cell, clear of the tray and latch housing by 3 mm or more, on the rear row); the wiring figure (Figure 12) shows it as "T".
8. LFP chemistry code and coding key geometry: not done; the decision assigns them only when an LFP variant is designed.
9. Photoreal renders, `media/card.png` and `media/social-preview.png`: not done here; they are made on Amish's Mac. The appearance model and the render scenes are ready for them (below).

### Results

- Constructability checks: 78 of 78 pass (71 before, plus 3 for the sensor, 3 for the catch geometry and 1 for the handle zone). STEP and STL regenerated.
- Cost: Value-engineering target: USD 700. Estimated cost of the constructable design: USD 619 (USD 81 under the target). Pack USD 449, dock USD 170. `budget_usd` unchanged.
- Mass: unchanged at about 3.03 kg; the polycarbonate sheet has the density the calculation already used (1.20 g/cm³), and the sensor is part of line 12.
- Requirement status: no change. R16 stays under the target (USD 619).
- Appearance model (`cad/src/product_model.py`) brought into line with the constructable design: eight flush countersunk lid screws, polycarbonate sheet lid, 6 mm pawl and the thumb button behind the grip, rivets and holder screws on the back face, cells at the model's rows with the sensor, the 580 mm back plate at its model height, guides and catch at model positions, the two charger straps, the controller box on the plate between charger and shelf, wall screws at the model's wall holes, labels reading interface v0.4. RENDER_VIEWS unchanged (hero, exploded, detail). Render scenes exported to `/home/claude/renders/swapcell`.

### Documents changed

- `cad/src/model.py`, `cad/step/*.step`, `cad/stl/*.stl`
- `cad/src/sheets.py`, `cad/drawings/SWC-DWG-002.*` (Rev P3 to P4)
- `cad/src/build_plan_media.py`, `cad/drawings/SWC-DWG-108.*` and `SWC-DWG-112.*` (Rev P1 to P2), `docs/05-build-plan/wiring.png`
- `cad/src/concept_media.py`, `media/` concept set (hero, cutaway, exploded, flow, blueprint SWC-DWG-001, `model.glb`, `viewer.html`)
- `cad/src/product_model.py`
- `bom/bom.csv` (line 4, line 3 note), `bom/bom-notes.md`
- `docs/04-calcs/sizing.py`, `docs/04-calcs/results.csv`, `docs/04-calcs/01-sizing.md` (SWC-CAL-001 v0.3 to v0.4)
- `docs/02-concept.md` (SWC-PRC-001 v0.6 to v0.7), `docs/03-requirements.md` (SWC-REQ-001 v0.6 to v0.7), `docs/05-build-plan.md` (SWC-BLD-001 v0.2 to v0.3), `docs/06-design-decisions.md` (SWC-DEC-001 v0.2 to v0.3), `README.md`
- All PDFs re-rendered.

### Cross-repo actions

- Move to interface v0.4 and check that receivers leave the 84 x 43 mm handle zone clear and use the published catch geometry: cargomule, cellguard, coldpod, culvertcrawl, dewdrive, dockhub, dustrunner, fieldcell, flattrike, lumaflow, motioncore, powerbox, stepclimber, stepgen, sunspoke, wastewise-scan, waterwalker, waterwatch, zeerbox. Their SwapCell cost citation also changes from USD 436 to USD 449 per pack.

No decision was made in this session beyond those Amish approved. TRL stays at 3; TRL 4 remains on hold.

## 2026-10-02: photoreal renders redone on the constructable design

Rendered with Blender Cycles on Amish's Mac from the updated appearance model; captioned with `.kit/photo_caption.py`; `media/card.png` and `media/social-preview.png` regenerated with `.kit/cards.py`. Views: hero, exploded, detail. image_qc passes. Appearance deviations are those logged above as proposed, awaiting Amish.
