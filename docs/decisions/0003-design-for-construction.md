---
doc_id: SWC-DDR-003
title: SwapCell design for construction
project: SwapCell
doc_type: Design decision record
version: "0.2"
status: Draft
date: '2026-10-02'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-10-01'
  author: Amish Chadha
  change: Changes that make the concept physically buildable, with the reason for each; made under Amish's 2026-09-30 instruction to make the design physically buildable; open for his review
- version: "0.2"
  date: '2026-10-02'
  author: Amish Chadha
  change: "Accepted by Amish on 2026-10-02, including the recommendations for A1 to A4 (A3 changes the printed-lid decision for the prototype)"
---

# 0003: Design for construction

- **Date:** 2026-10-01
- **Status:** accepted. Amish, 2026-10-02: "i approve your recommendations for all 555 open decisions." This covers every change in Tables 1 and 2 and the recommendations for A1 to A4 in Table 3, which are now decided as recommended and recorded in the design decisions register (SWC-DEC-001). A3 changes the printed-lid decision of 2026-09-25 for the prototype.

## Context

On 2026-09-30 Amish asked for every repo to get an illustrated prototype build plan and wrote: "If you are realising that the design cannot be built as per concept - fix the design assumptions to match and be physically feasible as you draw the illustrations." The TRL 3 model of SwapCell (`cad/src/model.py` before this record) was a massing model: it showed what the pack and dock do and fixed the published interface, but most parts had no fixing, and some could not work as drawn. Checking it with build123d found the problems in Table 1. The worst was the latch: the catch on the dock sat 2 mm below the pawl instead of above it, so it could never stop the pack being lifted out, and the spring-loaded pawl had neither room to retract nor a release.

The changes keep what the product does and what the interface publishes: the 340 x 90 x 80 mm body, the 393 mm overall length, the connector position and pinout, the guide faces, the latch position (36 mm wide on the back face, 45 mm below the top end) and its class V1 proof load, the handle zone, the flush wake button, the cells, the BMS, the charger and the controller. Nothing here changes the pitch or the safety case. Every change is in `cad/src/model.py`, which now builds each component as it is made or bought, with its fixings, and runs 71 constructability checks (`python cad/src/model.py --check`): parts that must touch do touch, parts that must not touch are apart by at least the stated clearance, the pawl hooks 4 mm under the catch and clears it by 1 mm when retracted, and the body stays inside the envelope. All 71 pass.

## Decision

*Table 1. Changes made to the model, the BOM and the calculations.*

| # | Problem in the concept | Change made | Why this way |
| --- | --- | --- | --- |
| P1 | The dock catch sat 2 mm below the pawl, so it only stopped downward movement (the shelf's job) and never held the pack in; the pawl's outer face rubbed on the back plate. | The catch, now a separate 50 x 12 x 8 mm steel bar on two M5 screws, sits 1 mm above the pawl's top face and reaches 8 mm out from the plate, 2 mm clear of the pack. The pawl stands 6 mm proud (was 10), hooks 4 mm under the catch and is 4 mm clear of the plate. | A pawl must pass the catch on the way in and hook under it, as in any spring latch. The 4 mm engagement and the tooth size are those of the class V1 sizing in SWC-CAL-001, so the proof load result stands. |
| P2 | The spring-loaded pawl had no mechanism: to pass the catch it needed to retract about 10 mm, but the cells sat 7 mm behind the back wall; there was no release under the handle. | The pawl is a steel block that slides through a 37 x 25 mm slot in the back wall, in a folded 1.5 mm steel housing riveted inside the wall with six countersunk blind rivets (the latch doubler). A shoulder on the pawl rests on the wall as its out stop; two springs push it out. A steel release slider runs down the inside of the wall; its 45 degree ramp wedges against a matching ramp on the shoulder, so pressing the printed thumb button on top of the slider 5 mm pulls the pawl in 5 mm, 1 mm clear of the catch. A lead-in on the tooth lets the catch push the pawl in as the pack drops. The cell block moves 8 mm toward the lid to make room. | A wedge needs no pivots, pins or small parts and can be filed by hand. The housing doubles as the doubler that the latch sizing already assumed, with the same six 4 mm rivets. The thumb button sits just behind the grip, where a hand that lifts the pack presses it naturally, matching the "thumb release under the handle" of the precis and the renders. |
| P3 | The 3 mm lid sat on the 1.5 mm edges of the tray with no fixing and no gasket seat; screws cannot go into a 1.5 mm edge. | 8 mm flanges folded inward round the open front of the tray; eight M3 press-in nuts in the flanges; eight M3 countersunk screws through the lid; a 1 mm flat gasket between lid and flanges. The tray is 1 mm shallower (76 mm) so tray, gasket and lid still make exactly 80 mm. | Press-in nuts in folded flanges are the usual way to close a sheet-metal box; the flat gasket gives the sealing face R8 needs. The envelope is unchanged. |
| P4 | The plug shroud was drawn against the connector face with no fixing and no way for its wires into the pack. | Four M3 screws from inside the tray into heat-set inserts in the shroud; a 42 x 22 mm lead opening in the connector face, sealed with a bead of sealant; the contact holes go through the shroud so contacts are fitted from the top with their wires. | Screws from inside leave the connector face clean and can be reached with the lid off. |
| P5 | The carry handle had no fixing. | Two M5 screws from inside the tray up into heat-set inserts in the handle's legs. | Same reasoning as P4; nothing protrudes from the top end. |
| P6 | The cells floated in the tray; the cell holders in the BOM were not modelled. | Two printed holder frames, one near each end of the cells, with 26 pockets each; their back edges rest on the tray back wall, two M2.5 countersunk screws each from outside. The right frame is notched to clear the latch housing. | Frames that bear on the wall locate the 1.8 kg block in every direction; countersunk screws keep the back face flat. |
| P7 | The BMS board floated beside the cells. | Four 2 mm standoffs and M2.5 countersunk screws through the right side wall; the board is 2.5 mm clear of the cell ends. | Countersunk heads keep the guide face flat. |
| P8 | The receptacle was drawn inside the solid shelf (25,000 mm³ overlap) with no float, although R10 asks for ±3 mm. | The shelf has a 72 x 50 mm cavity under the plug pocket. The printed receptacle has a flange that the pocket's 6 mm ledge captures from above, with 3 mm to float each way; a 15 mm foam pad and a 3 mm aluminium retainer plate on four M3 screws hold it up. The key post moves to the receptacle and the pins are modelled with the INTERLOCK pin shortest. | A captured, sprung receptacle is the simplest floating mount. The foam also lets it tilt the 2 degrees of R10. |
| P9 | The side guides stood 10 mm in front of the back plate, fixed to nothing. | Guides run back to the plate (70 mm deep), two M5 countersunk screws each from behind into heat-set inserts; the 10 mm lead-in of the interface is now modelled. | Bolting to the plate carries the knocks of a careless swap. |
| P10 | The shelf, catch and plate were one fused solid with no fixings. | Shelf on four M5 countersunk screws from behind the plate into inserts; catch on two M5 countersunk screws. | Each part can be made and replaced on its own. |
| P11 | The controller box hung 10 mm off the plate and 35 mm past its edge. | It sits on the plate between the charger and the shelf, on two M4 screws. | Inside the plate, close to the receptacle wiring. |
| P12 | The charger had no fixing. | Two folded 20 x 1.5 mm aluminium straps over it, each on two M5 screws into tapped holes; the plate grows from 520 to 580 mm (bottom edge 170 mm below the dock datum, top edge 10 mm above the pack's top end) to carry the straps and the catch. | Works with any brick charger of about the same size, without drilling it. |

*Table 2. Knock-on changes.*

| Item | Change | Reason |
| --- | --- | --- |
| Mass | Pack 3.03 kg (was 2.85 kg) [SWC-CAL-001 v0.3, section 3]: latch housing, slider, button and springs 0.11 kg; pawl and handle from model volumes 0.13 kg (was 0.10); fixings 0.10 kg (was 0.08); tray flanges 0.03 kg. R5 (3.5 kg) is still met with 0.47 kg margin. Energy density 154 Wh/kg (was 164). | Parts added for construction. |
| Thermal | Heat capacity 2.29 kJ/K (was 2.26), time constant 33 min (was 32); hot spots unchanged at 51, 63 and 71 °C; enclosed derating current about 18.6 A (was 18.5). R3 stays met on paper. | Heavier tray. The cells no longer touch the back wall (P2); the lumped model's 0.10 K/W core-to-tray assumption is listed as proposed item A4. |
| Cost | BOM lines 1, 4 to 9 and 11 to 13 updated, lines 15 (latch housing, slider and springs), 16 (cell holder frames, moved from line 12) and 17 (dock mounting parts) added. Pack USD 436, dock USD 170, total USD 606 against the USD 700 value-engineering target (`budget_usd`, unchanged), USD 94 under. | Parts added for construction. |
| Drawings | SWC-DWG-002 Rev P3; making sketches SWC-DWG-101 to 115 added. | Follow the model. |
| Documents | SWC-CAL-001 v0.3, SWC-REQ-001 v0.5, SWC-PRC-001 v0.5: mass, cost, thermal and latch description updated. No requirement changed status. | Follow the model. |
| Interface | No published value changed. Two clarifications are proposed (A1, A2). | |

*Table 3. Proposed, then accepted by Amish as recommended on 2026-10-02.*

| # | Question | Options | Recommendation |
| --- | --- | --- | --- |
| A1 | The thumb button sits 3 to 19 mm behind the published handle zone (84 x 22 mm), so a receiver built to the letter of interface v0.3 could put structure over it. | (a) widen the handle zone in interface v0.4 to the full depth behind the handle (84 x 43 mm, from the zone's front edge to the back face); (b) move the release forward under the grip, which needs a lever. | (a): no change to the pack, one line in the interface. Accepted 2026-10-02. |
| A2 | The catch geometry that makes the latch work (latching face 1 mm above the pawl, reach 8 mm from a plate 10 mm behind the pack, 4 mm engagement, 1 mm clear when retracted) is not published, but every receiver needs it. | (a) add it to interface v0.4 with the pawl's 6 mm projection and 5 mm travel; (b) leave it to each receiver design. | (a), so vehicle receivers in PowerBox, CargoMule and others latch the same way. Accepted 2026-10-02. |
| A3 | A 90 x 340 mm lid needs a printer with a bed of at least 350 mm; Amish's 2026-09-25 decision was a printed lid. | (a) print it on a large-format printer; (b) cut it from 3 mm UL 94 V-0 polycarbonate sheet, same shape and holes. | (b) for the prototype: easier to source and flatter; the drawing allows either. Accepted 2026-10-02, changing the printed-lid decision of 2026-09-25 for the prototype. |
| A4 | Moving the cells 8 mm toward the lid (P2) leaves them clear of the back wall, so heat reaches the tray through the holder frames and air rather than through pads on the wall. The lumped thermal model keeps its 0.10 K/W core-to-tray assumption. | (a) keep the assumption and check it in the TRL 4 load test, relying on the PACK_LIMITS derating meanwhile; (b) add a thermal pad between the rear row of cells and the latch housing area now. | (a): the derating rule already holds cells under 60 °C whatever the path, and the test measures it. Accepted 2026-10-02, with the battery board's temperature sensor on the rear row of cells, now furthest from the tray. |

## Consequences

- `design_state: constructable` in `project.yaml`. The build plan SWC-BLD-001 shows every component and step in pictures generated from the model (`cad/src/build_plan_media.py`); open items are in the design decisions register SWC-DEC-001.
- Requirement status is unchanged: none not met, 2 at risk (R2, R9), 5 not verifiable at TRL 3, 8 met (four on paper only), and R16 under the value-engineering target (SWC-CAL-001 v0.3).
- The photoreal renders (`media/render-*.png`), `media/card.png` and `media/social-preview.png` still show the concept: six lid screws instead of eight, a 10 mm pawl, guides standing off the back plate, a shorter back plate and no charger straps. They need regenerating on Amish's Mac, where Blender is. The appearance model `cad/src/product_model.py` reads its sizes from the model and was not edited.
- With A1 and A2 accepted, the SwapCell interface is issued as v0.4 in SWC-PRC-001 (handle zone 84 x 43 mm; catch geometry published). With A3, the prototype lid is cut from 3 mm UL 94 V-0 polycarbonate sheet. With A4, the battery board's temperature sensor goes on the rear row of cells.
- TRL 4 remains on hold by Amish's instruction. Nothing was built or bought.
