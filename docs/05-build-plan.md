---
doc_id: SWC-BLD-001
title: SwapCell prototype build plan
project: SwapCell
doc_type: Build plan
version: "0.2"
status: Draft
date: '2026-10-02'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
  - version: "0.1"
    date: '2026-10-01'
    author: Amish Chadha
    change: First build plan, with pictures by component and step; design made constructable (SWC-DDR-003)
  - version: "0.2"
    date: '2026-10-02'
    author: Amish Chadha
    change: "Decisions of 2026-10-02: lid cut from 3 mm UL 94 V-0 polycarbonate sheet; board temperature sensor on the rear row of cells. Pictures unchanged"
---

# SwapCell prototype build plan

**Plan, not yet built.** How to build the first proof-of-concept prototype, one pack and one wall dock, component by component. Building and testing to it is TRL 4 work. Decisions still to be made are kept in the design decisions register ([docs/06-design-decisions.md](06-design-decisions.md)), not here.

## 1. What you are building

![Figure 1. Every component, pulled apart and numbered in build order](05-build-plan/overview.png)

*Figure 1. Every component pulled apart and numbered in build order: the pack (1 to 11) up and to the left, the wall dock (12 to 20) on the right.*

The prototype is one SwapCell pack and one wall dock. The pack is a folded aluminium box, 340 x 90 x 80 mm, holding 26 lithium-ion cells in two printed frames and a battery management board, closed by a lid on a gasket, with a carry handle on top, a keyed plug underneath and a spring latch on its back. The dock is a 12 mm aluminium plate on the wall carrying a printed shelf and two printed guides that the pack drops between, a floating receptacle in the shelf, a steel catch for the latch, a controller box and a bought, certified charger. Figure 1 shows the 20 components in the order you make or fit them. Fourteen are made in a small workshop: the tray, latch housing, latch pawl, release slider and button, plug shroud, cell holder frames, handle and lid of the pack; the back plate, shelf, guides, catch, receptacle shroud, retainer plate and charger straps of the dock. The cells, the battery management board, the contacts, the charger, the controller and the fixings are bought. The work is folding and drilling aluminium sheet, cutting and drilling plate and steel bar, filing, 3D printing, fitting heat-set inserts, spot welding nickel strip, and wiring at block level. The parts cost about USD 606 from the bill of materials.

> **Safety:** The pack stores about 468 Wh in lithium-ion cells at up to 54.6 V and can deliver about 500 A into a short. A cell in thermal runaway vents flammable, toxic gas and can set its neighbours alight. Build, charge and test the pack only inside a fireproof enclosure on a non-combustible surface, with a lithium-rated or Class D extinguisher and a bucket of sand at hand, and never leave it unattended. Use insulated tools, keep the battery management board unplugged until section 6 says otherwise, and stop at every safety stop in section 6. The dock charger plugs into a mains socket; no mains wiring is part of this build.

## 2. What changed to make it buildable

The concept showed what SwapCell does and fixed its published interface; many of its parts had no fixing, and the latch could not work as drawn. Each change below keeps what the pack and dock do and keeps every published interface size. All of them are recorded in decision record SWC-DDR-003, open for Amish's review.

*Table 1. Changes from the concept.*

| Component | The concept had | The buildable design has | Why |
| --- | --- | --- | --- |
| Latch catch | A catch 2 mm below the pawl, which could never stop the pack being lifted out | A steel catch 1 mm above the pawl, which the pawl hooks 4 mm under (Figure 21) | A spring latch must pass the catch on the way in and hook under it |
| Latch pawl | A block 10 mm proud with no room to retract and no release | A pawl 6 mm proud that slides in a riveted steel housing, pushed out by two springs and pulled in 5 mm by a ramped slider under a thumb button (Figure 5) | Nothing to pivot or pin; the housing is the doubler the latch sizing assumed |
| Cells | 1 mm from the back wall | 8 mm further toward the lid, held in two printed frames that rest on the back wall (Figure 11) | Room for the latch; the cells now have a fixing |
| Lid | A plate on the 1.5 mm edges of the tray, with no fixing | Eight screws into press-in nuts in 8 mm flanges folded into the tray's front, over a 1 mm gasket (Figure 3) | A sealing face and something to screw into; the tray is 1 mm shallower so the body stays 80 mm deep |
| Plug, handle, cell frames, battery management board | No fixings | Screws from inside the tray into heat-set inserts, or countersunk from outside so the faces stay flat (Figures 9, 14) | The published faces stay flush |
| Receptacle | Drawn inside the solid shelf, unable to float | Held in a cavity under the shelf pocket by its flange, on a foam pad, free to float 3 mm each way (Figure 23) | The connector needs that float to line up |
| Guides, shelf, catch, controller box, charger | Floating off the back plate or past its edge, or with no fixing | All screwed to the back plate; the plate is 580 mm tall (was 520) to carry the catch and two charger straps (Figures 18, 26) | Each part can be made and replaced on its own |

## 3. Making the components

Make and check each component before the assembly step that needs it. Sizes are in millimetres. "Left" and "right" are as seen standing in front of the pack, looking at its lid; "back" is the face toward the wall; "up" is measured from the connector face, the pack's underside. Workshop tolerance is 0.5 mm unless a step says otherwise; drawings do not carry tolerances before TRL 4.

### 3.1 Pack tray

![Figure 2. Making sketch of the pack tray](../cad/drawings/SWC-DWG-101.png)

*Figure 2. Pack tray making sketch (SWC-DWG-101).*

**What it is and what it is made from.** The aluminium box that is the pack's body: its back, two sides and two ends are the published guide, latch and connector faces. Aluminium sheet 1.5 mm, 5052-H32, folded from one blank. A sheet-metal shop can cut and fold it from the sketch; the steps below are for doing it yourself.

**How to make it.**

1. Lay out the blank: the back, 90 wide x 340 tall, in the middle; a side 76 wide on each long edge; an end 76 deep on each short edge, with a 10 mm tab on each end of it; an 8 mm flange along the free edge of each side and each end. Drill a 3 mm relief hole wherever two fold lines cross.
2. Mark and drill every hole while the blank is flat (the sketch gives every position):
   - back: a pawl slot 37 wide x 25 tall, centred across, 282.5 to 307.5 up; six 4.1 mm rivet holes, 25 each side of centre, 290, 310 and 330 up; four 2.7 mm holder screw holes, 25 right and 37 left of centre, 60 and 240 up;
   - top end: a slot 31 x 5.5 against the back wall, centred across, for the release slider; two 5.5 mm holes 36.5 each side of centre, 32 in from the back face, for the handle screws;
   - connector face: a lead opening 42 x 22, centred across, 21 to 43 in from the back face; four 3.4 mm plug screw holes, two 25 each side of centre 45 in from the back face, one 25 left of centre 19 in, one 9 right of centre 18 in;
   - right side: four 2.7 mm holes 8 and 58 in from the back face, 80 and 260 up, for the battery management board;
   - flanges: eight 4.2 mm holes for the press-in nuts, 5.5 in from the outside of each side wall, 30, 125, 215 and 310 up.
3. Countersink every hole in the back and the right side from the outside so screw and rivet heads sit flush: these are published faces and nothing may stand out of them. Cut the slots by chain drilling and filing square.
4. Fold the flanges inward 90 degrees first, then the sides and ends up 90 degrees, then the tabs onto the sides. Rivet each tab with two 3.2 mm blind rivets and seal each corner seam inside with a bead of neutral-cure silicone.
5. Press the eight M3 press-in nuts into the flanges from inside, in a vice with soft jaws, until flush.
6. Deburr everything. Line the inside of the back, sides and ends with flame-retardant liner sheet, cut clear of every hole.

![Figure 3. Joint 1: lid on the tray flange](05-build-plan/joint-01.png)

*Figure 3. The lid sits on a 1 mm gasket on the 8 mm flange; a countersunk M3 screw goes into the press-in nut.*

**How it fits the parts next to it.** The lid closes the open front over the flanges (Figure 3). The latch housing is riveted inside the back wall (Figure 5), the plug shroud screws under the connector face (Figure 12), the cell frames rest on the inside of the back wall (Figure 11), the battery management board stands on the right side wall, and the handle screws onto the top end (Figure 14).

**Check before moving on.** Outside 90 wide, 80 deep with the lid on, 340 tall, within +0 and -1.5. Every corner square; no rivet or screw head stands proud of the back or sides; the eight nuts take an M3 screw by hand.

### 3.2 Latch housing

![Figure 4. Making sketch of the latch housing](../cad/drawings/SWC-DWG-102.png)

*Figure 4. Latch housing making sketch (SWC-DWG-102).*

**What it is and what it is made from.** A small open steel box riveted inside the back wall that guides the pawl and carries its load into the tray. Zinc-plated steel sheet 1.5 mm.

**How to make it.**

1. Cut a blank for an open box 40 wide, 12.5 deep and 57 tall: a front 40 x 57, two sides 12.5 x 57, a bottom 40 x 12.5, and a 10 mm flange on the back edge of each side.
2. Fold the sides and bottom toward the back, then the flanges outward, square.
3. Drill three 4.1 mm holes in each flange, 5 from the side wall, 8.5, 28.5 and 48.5 up from the bottom.

![Figure 5. Joint 2: the latch, cut through its middle](05-build-plan/joint-02.png)

*Figure 5. The pawl's shoulder rests on the back wall; the slider's ramp sits on the pawl's ramp. Pressing the button pushes the slider down and pulls the pawl in.*

**How it fits the parts next to it.** The flanges lie flat on the inside of the back wall, the bottom 281.5 up, centred across, over the pawl slot; six countersunk blind rivets go in from outside. The housing's top is open and stops just under the tray's top end. The pawl slides inside it with 0.5 mm each side, and its springs push against the housing's front.

**Check before moving on.** The pawl slides in and out of the housing freely by hand.

### 3.3 Latch pawl

![Figure 6. Making sketch of the latch pawl](../cad/drawings/SWC-DWG-103.png)

*Figure 6. Latch pawl making sketch (SWC-DWG-103).*

**What it is and what it is made from.** The steel tooth that stands out of the back face and hooks under the dock's catch. Steel flat bar 40 x 15 mm, 1018 class.

**How to make it.**

1. Cut a block 36 wide, 34 tall and 12.5 deep; square all faces.
2. The lower 24 mm is the tooth, full depth. Its top face is the latching face: keep it flat and square to the back. File a 4 mm x 45 degree lead-in along its outer bottom edge, so the catch pushes it in as the pack drops.
3. The upper 10 mm is the shoulder. Mill or file away its outer 7.5 mm, leaving 5 mm deep, then file its top back edge to a 5 mm x 45 degree ramp.
4. Drill two 6 mm spring holes 8 deep in the inside face, 10 each side of centre, 12 up from the bottom.

**How it fits the parts next to it.** The tooth passes out through the slot in the back wall and stands 6 mm proud of the back face; the shoulder rests on the inside of the wall above the slot, which stops it coming further out. In the dock it sits 1 mm below the catch and overlaps it by 4 mm (Figure 21). Pressing the thumb button pulls it in 5 mm, 1 mm clear of the catch.

**Check before moving on.** It slides in its slot without binding at any point; the latching face is flat.

### 3.4 Release slider and thumb button

![Figure 7. Making sketch of the release slider and thumb button](../cad/drawings/SWC-DWG-104.png)

*Figure 7. Release slider and thumb button making sketch (SWC-DWG-104).*

**What it is and what it is made from.** A steel bar that runs down the inside of the back wall from a button on the top end; its ramped lower end pulls the pawl in. Steel flat bar 35 x 5 mm; button printed in the same plastic as the handle.

**How to make it.**

1. Cut the bar 36 long. File it 34 wide for its lower 25.5 mm and 30 wide for the 10.5 mm above, so the wide part cannot pass up through the slot in the tray top.
2. File the lower end to a 45 degree ramp across the full 5 mm thickness, sloping up toward the lid, to match the pawl's ramp.
3. Drill and tap M3, 6 deep, in the top end.
4. Print the button 30 x 16 x 8 with a 3.4 mm hole through, counterbored from the top for the screw head.

**How it fits the parts next to it.** The slider goes up through the slot in the tray top from inside, flat against the back wall, its ramp on the pawl's ramp (Figure 5). The button screws onto its top and sits 8 mm above the tray, just behind the handle's grip. Pressed 5 mm, the slider wedges between the wall and the pawl and pulls the pawl in 5 mm; the pawl's springs push both back.

**Check before moving on.** With the housing fitted, 5 mm of button travel brings the tooth flush with the back face, and the button returns by itself.

### 3.5 Plug shroud

![Figure 8. Making sketch of the plug shroud](../cad/drawings/SWC-DWG-105.png)

*Figure 8. Plug shroud making sketch (SWC-DWG-105).*

**What it is and what it is made from.** The keyed block under the pack that carries the two power and six signal socket contacts. Printed in flame-retardant PC-ABS or nylon at 100 % infill; the contacts are bought.

**How to make it.**

1. Check the bought contacts' diameters and change the hole sizes on the sketch to suit before printing.
2. Print 56 x 34 x 18 with the key notch, 8 x 8, at its back right corner. Power contact holes 9 mm through, 15 each side of centre, 12 in from the front edge; six signal holes 3 mm through at 7 mm pitch, 26 in from the front edge.
3. Fit four M3 heat-set inserts in the top face, 8 deep, at the four screw positions of the sketch.
4. Crimp the power leads and signal wires to the contacts, then press the contacts in from the top. The INTERLOCK contact is the shortest so it mates last. Pot the six signal contacts with flame-retardant epoxy.

![Figure 9. Joint 4: plug shroud on the connector face](05-build-plan/joint-04.png)

*Figure 9. The shroud's top face sits flat on the connector face; screws come from inside the tray; wires go up through the lead opening.*

**How it fits the parts next to it.** The top face lies flat on the connector face, centred across and 8 mm toward the back from the depth centre line, held by four M3 screws from inside the tray (Figure 9), with a bead of sealant round the lead opening. In the dock it drops into the shelf pocket with 2 mm all round and meets the receptacle face to face (Figure 23).

**Check before moving on.** The key notch is at the back right seen from the lid; every contact is held firm; the wires are labelled.

### 3.6 Cell holder frames and the cell block

![Figure 10. Making sketch of the cell holder frame](../cad/drawings/SWC-DWG-106.png)

*Figure 10. Cell holder frame making sketch (SWC-DWG-106).*

**What it is and what it is made from.** Two printed frames that hold the 26 cells in two rows of 13 and locate the block on the back wall. Flame-retardant PC-ABS, 6 mm thick, printed flat.

**How to make it.**

1. Print two frames 6 thick, 59.5 deep and 300 tall. Each has 26 pockets 21.2 mm across, in two rows 25.5 and 47.5 mm in from the back edge, 13 per row at 22 mm pitch, the first 18 up from the bottom. Print one plain (the left frame) and one with a notch 6.5 deep from the back edge over its top 44.5 mm (the right frame), which clears the latch housing.
2. Fit two M2.5 heat-set inserts in the back edge of each frame, 40 and 220 up from its bottom.
3. Build the block (step 6): push the cells into both frames, all the same way round as the wiring needs, until 1 mm of each cell stands out of each frame.
4. Spot weld nickel strip across each pair to make 13 parallel groups, with a fuse wire from the strip to each cell, then join the groups in series, one group at a time. Never solder to a cell. Wrap the block in fish paper, leaving the sense lead tabs out.

![Figure 11. Joint 6: cell holder frame on the back wall](05-build-plan/joint-06.png)

*Figure 11. Cut level with a screw: the right frame's back edge rests on the tray's back wall; one countersunk M2.5 screw from outside goes into an insert.*

![Figure 12. Wiring at block level](05-build-plan/wiring.png)

*Figure 12. Block-level wiring with wire sizes. No circuit board is laid out at this stage; the battery management board is bought.*

#### 3.6.1 Wiring

Wire the pack and dock as Figure 12, with stranded silicone copper:

1. Cell block positive to the battery management board's cell input: 6 mm² (10 AWG).
2. The board's switched output, through the 40 A main fuse, to the plug's PACK+ contact: 6 mm².
3. Cell block negative to the plug's PACK- contact and the board's ground: 6 mm².
4. Thirteen sense leads, one from each group, and the cell temperature sensors to the board's balance connector, with the board's temperature sensor on the rear row of cells (furthest from the tray): 0.25 mm², connected only at safety stop S3.
5. CAN high and low, WAKE, INTERLOCK and signal ground from the board to the plug: 0.25 mm², CAN as a twisted pair.
6. The wake button to the board's wake input: 0.25 mm².
7. In the dock: the receptacle's PACK+ and PACK- to the controller box's relay and current sensor and on to the charger output: 2.5 mm² (14 AWG); the receptacle's CAN and signal ground to the controller's CAN transceiver: 0.25 mm², twisted, with a 120 Ω termination in the controller. Solder the 10 kΩ coding resistor between the receptacle's INTERLOCK and signal ground pins.

**Check before moving on.** Each group reads within 0.05 V of the others; every fuse wire is intact; no bare metal can touch the tray.

### 3.7 Carry handle

![Figure 13. Making sketch of the carry handle](../cad/drawings/SWC-DWG-107.png)

*Figure 13. Carry handle making sketch (SWC-DWG-107).*

![Figure 14. Joint 7: handle and thumb button on the top end](05-build-plan/joint-07.png)

*Figure 14. Cut through both handle screws: two M5 screws from inside the tray hold the handle; the thumb button sits on the slider behind the grip.*

**What it is and what it is made from.** The loop on the top end that a gloved hand lifts the pack by. Printed PETG or nylon, 60 % infill.

**How to make it.**

1. Print 84 wide, 22 deep and 35 tall as an arch: a grip bar 10 thick over a 62 x 25 opening, on legs 11 wide. Round the grip edges to 3 mm.
2. Fit an M5 heat-set insert, 12 deep, in the bottom of each leg, 36.5 each side of centre.

**How it fits the parts next to it.** The legs sit flat on the top end, centred across and 8 mm toward the back from the depth centre line, held by two M5 screws up from inside the tray (Figure 14). The thumb button sits 3 mm behind the grip.

**Check before moving on.** A gloved hand fits through the opening and the thumb reaches the button.

### 3.8 Pack lid

![Figure 15. Making sketch of the pack lid](../cad/drawings/SWC-DWG-108.png)

*Figure 15. Pack lid making sketch (SWC-DWG-108).*

**What it is and what it is made from.** The front face of the pack, removable for repair. For the prototype, cut from 3 mm UL 94 V-0 polycarbonate sheet. A lid printed in a V-0 grade polymer on a printer with a bed of at least 350 mm, to the same shape, is also allowed.

**How to make it.**

1. Make a flat plate 90 x 340 x 3.
2. Drill eight 3.4 mm holes, countersunk on the outside, 39.5 each side of centre, 30, 125, 215 and 310 up.
3. Drill the wake button hole 13 mm, centred across, 270 up.
4. Fit the sealed wake button with its nut inside.

**How it fits the parts next to it.** It sits on a 1 mm flat gasket over the tray's flanges, held by eight countersunk M3 screws into the press-in nuts, heads flush (Figure 3).

**Check before moving on.** On a trial fit, the gasket squeezes evenly with no gap at the corners, and the wake button body clears the cells.

### 3.9 Dock back plate

![Figure 16. Making sketch of the dock back plate](../cad/drawings/SWC-DWG-109.png)

*Figure 16. Dock back plate making sketch (SWC-DWG-109).*

**What it is and what it is made from.** The plate on the wall that every dock part hangs on. Aluminium plate 12 mm, 6082 or 6061.

**How to make it.**

1. Cut 150 x 580; square, deburr and round the corners to 3 mm. Scribe a centre line; heights below are from the bottom edge.
2. Drill 5.5 mm and countersink from the back (the wall side): four shelf holes 45 each side of centre at 195 and 220 up; four guide holes 52 each side at 270 and 370 up; two catch holes 16 each side at 544 up.
3. Drill and tap from the front: four M5 strap holes 62 each side of centre at 19 and 151 up; two M4 controller holes 15 each side at 160 up.
4. Drill four 6.5 mm wall holes: 30 each side of centre at 10 up, and 62 each side at 568 up.

**How it fits the parts next to it.** Every dock part sits flat on its front face; its back goes flat on the wall.

**Check before moving on.** The countersunk screw heads sit flush or just below the back face.

### 3.10 Cradle shelf

![Figure 17. Making sketch of the cradle shelf](../cad/drawings/SWC-DWG-110.png)

*Figure 17. Cradle shelf making sketch (SWC-DWG-110).*

![Figure 18. Joint 8: shelf and right guide on the back plate](05-build-plan/joint-08.png)

*Figure 18. Countersunk M5 screws from behind the plate into inserts in the guide; the shelf is fixed the same way.*

**What it is and what it is made from.** The block the pack stands on, with the pocket for the plug and the cavity for the receptacle. Printed ASA or PETG, 40 % infill and four walls.

**How to make it.**

1. Print 120 wide, 110 deep and 45 tall.
2. The plug pocket is 60 x 38 and 18 deep from the top, centred across, its back edge 23 from the shelf's back face. The receptacle cavity is 72 x 50, from the bottom up to 27, centred under the pocket; the 6 mm ledge left between them holds the receptacle.
3. Fit four M5 heat-set inserts in the back face, 45 each side of centre, 10 and 35 up; and four M3 inserts in the bottom, 40 each side of centre, 13 and 71 in from the back face.

**How it fits the parts next to it.** The back face sits flat on the back plate, top 60 above the dock datum, held by four M5 countersunk screws from behind the plate (Figure 18). The pack stands on its top face; the plug drops into the pocket.

**Check before moving on.** The plug shroud drops into the pocket with 2 mm all round.

### 3.11 Side guides (make 2, a left and a right)

![Figure 19. Making sketch of the side guide](../cad/drawings/SWC-DWG-111.png)

*Figure 19. Side guide making sketch (SWC-DWG-111).*

**What it is and what it is made from.** Two printed rails either side of the pack that bring the plug within the receptacle's reach. Printed ASA or PETG, 40 % infill.

**How to make it.**

1. Print two, 12 wide, 70 deep and 180 tall, standing up; the left is a mirror image of the right.
2. Leave a 10 mm x 45 degree lead-in along the top inner edge.
3. Fit two M5 heat-set inserts in the back end of each, 40 and 140 up.

**How it fits the parts next to it.** Each back end sits flat on the back plate and its bottom on the shelf; inner faces 92 apart, 1 mm clear of the pack each side; two M5 countersunk screws from behind the plate (Figure 18).

**Check before moving on.** The pack slides between them without rubbing.

### 3.12 Latch catch

![Figure 20. Making sketch of the latch catch](../cad/drawings/SWC-DWG-112.png)

*Figure 20. Latch catch making sketch (SWC-DWG-112).*

![Figure 21. Joint 3: pawl under the catch](05-build-plan/joint-03.png)

*Figure 21. With the pack seated, the tooth sits 1 mm under the catch and overlaps it by 4 mm; pressed in, it clears the catch by 1 mm.*

**What it is and what it is made from.** The steel bar on the plate that the pawl hooks under. Zinc-plated steel flat bar 12 x 8 mm.

**How to make it.**

1. Cut 50 long; square and deburr. The bottom face is the latching face: keep it flat and square.
2. Drill and tap two M5 holes 7 deep in the back face, 16 each side of centre, half way up.

**How it fits the parts next to it.** The back face sits flat on the plate front, centred, 544 up from the plate's bottom, on two M5 countersunk screws from behind. It stands 8 mm out from the plate and ends 2 mm short of the pack's back face. With the pack seated, the pawl sits 1 mm below it and overlaps it by 4 mm (Figure 21).

**Check before moving on.** With the pack in the dock, lifting it by the handle without pressing the button does not bring it out.

### 3.13 Receptacle shroud

![Figure 22. Making sketch of the receptacle shroud](../cad/drawings/SWC-DWG-113.png)

*Figure 22. Receptacle shroud making sketch (SWC-DWG-113).*

![Figure 23. Joint 5: plug in the receptacle](05-build-plan/joint-05.png)

*Figure 23. The plug meets the receptacle face to face; the receptacle's flange sits under the pocket's ledge on the foam pad, free to float.*

**What it is and what it is made from.** The dock half of the connector: a printed body carrying the pins, which floats in the shelf so the plug can find it. Flame-retardant PC-ABS or nylon at 100 % infill; the pins are bought to match the plug's contacts.

**How to make it.**

1. Print a body 58 x 36 x 12 with a 3 mm flange 66 x 44 round its top, and a key post 7 x 7, 16 tall, at the back right corner of the top face.
2. Pin holes through, matched to the plug: power pins 15 each side of centre, 13 in from the front of the body; signal pins at 7 mm pitch, 27 in.
3. Press in the pins: power pins 10 above the face (PACK- 11), signal pins 8, the INTERLOCK pin only 5, so it mates last.
4. Solder the 10 kΩ coding resistor from INTERLOCK to signal ground and the leads to the pin tails.

**How it fits the parts next to it.** It goes up into the shelf cavity from below; its flange stops under the ledge round the plug pocket with 3 mm free each way. The foam pad and retainer plate hold it up (Figure 23).

**Check before moving on.** It moves 3 mm each way by hand and springs back up level.

### 3.14 Receptacle retainer plate

![Figure 24. Making sketch of the receptacle retainer plate](../cad/drawings/SWC-DWG-114.png)

*Figure 24. Retainer plate making sketch (SWC-DWG-114).*

**What it is and what it is made from.** The plate under the shelf that holds the foam pad and receptacle in. Aluminium sheet 3 mm, with a bought 15 mm closed-cell foam pad cut to 66 x 44.

**How to make it.**

1. Cut 88 x 66; deburr.
2. Drill four 4.4 mm holes 40 each side of centre, 4 and 62 from the front edge, and a 16 mm hole for the receptacle wires, centred across, 33 from the front edge, with a grommet.

**How it fits the parts next to it.** It lies flat under the shelf on four M3 screws into the inserts, squeezing the foam pad lightly against the receptacle.

**Check before moving on.** The receptacle's flange touches the ledge with the foam lightly squeezed.

### 3.15 Charger straps (make 2)

![Figure 25. Making sketch of the charger strap](../cad/drawings/SWC-DWG-115.png)

*Figure 25. Charger strap making sketch (SWC-DWG-115).*

![Figure 26. Joint 9: charger strap and controller box](05-build-plan/joint-09.png)

*Figure 26. Each strap's foot takes one M5 screw into a tapped hole; the controller box sits on the plate between the charger and the shelf.*

**What it is and what it is made from.** Two folded strips that hold the bought charger on the plate without drilling it. Aluminium strip 20 x 1.5 mm.

**How to make it.**

1. Measure your charger. The straps here suit one 150 wide, 64 deep and 110 tall: legs equal its depth, the front its height plus 3.
2. Cut two 300 mm lengths and fold each to a hat shape: two feet 20 long, two legs 64, a front 113.
3. Drill a 5.5 mm hole in each foot, 11 from the fold.

**How it fits the parts next to it.** The charger's back sits flat on the plate below the shelf; each strap goes over it 62 each side of centre, feet flat on the plate, one M5 screw into each tapped hole (Figure 26).

**Check before moving on.** The charger does not move when pulled by hand.

### 3.16 Bought components

Buy to specification, not brand. Line numbers are those of the bill of materials.

- **Cells (line 2).** 26 new, matched 21700 lithium-ion cells, 5.0 Ah nominal, 3.6 V, rated 25 A or more continuous, from an authorized distributor with a datasheet.
- **Battery management board (line 3).** Open-source 13-cell board with CAN 2.0B, balancing, 30 A switches on the positive side, pre-charge, a flash log, sleep current 100 µA or less and a wake input on INTERLOCK, about 230 x 58 mm and 10 mm thick or less.
- **Contacts (lines 5 and 9).** Two 40 A power socket contacts and six signal socket contacts for the plug, with matching pins for the receptacle; the INTERLOCK pair shortest.
- **Charger (line 10).** Certified 54.6 V, 5 A constant-current, constant-voltage lithium-ion charger, 100 to 240 V AC input, settable to 53.3 V.
- **Controller (line 11).** ESP32 board with a CAN transceiver, DC relay, current sensor and microSD, in a 50 x 50 x 30 mm box.
- **Fuses and wiring (line 12).** 40 A main fuse and holder, pre-charge resistor, fuse wire, nickel strip, 6 mm² and 0.25 mm² silicone wire, fish paper, thermistors.
- **Seals and fixings (line 13).** 1 mm closed-cell flat gasket, eight M3 press-in nuts and eight M3 x 8 countersunk screws (lid); four M3 x 10 screws and heat-set inserts (plug); two M5 x 12 screws and inserts (handle); four M2.5 x 8 countersunk screws and inserts (cell frames); four 2 mm standoffs and M2.5 countersunk screws (battery management board); six 4 mm countersunk blind rivets (latch housing); 3.2 mm blind rivets (tray tabs); flame-retardant liner sheet.
- **Wake button (line 14).** Sealed momentary switch, IP67 class, 12 mm, panel mounted, no more than 15 mm deep behind the panel.
- **Springs (line 15).** Two compression springs about 5 mm across and 14 mm long.
- **Dock mounting parts (line 17).** 15 mm closed-cell foam, M5 countersunk screws and heat-set inserts, M3 retainer screws, two M4 controller screws, four 6 mm wall screws and anchors.

## 4. Putting it together

In each picture the parts already fitted are grey and the part being fitted is in colour, with an arrow showing the way it goes in.

### Step 1: press-in nuts into the tray flanges

![Step 1](05-build-plan/step-01.png)

Eight M3 nuts from inside, pressed flush in a vice with soft jaws (if not already done in section 3.1).

### Step 2: pawl and release slider into the back wall

![Step 2](05-build-plan/step-02.png)

From inside the tray: put the springs in the pawl's holes and pass the pawl's tooth out through its slot, shoulder up against the wall. Pass the slider's narrow end up through the slot in the top end, ramp down on the pawl's ramp.

### Step 3: latch housing over them

![Step 3](05-build-plan/step-03.png)

Hold the housing over the pawl and slider, flanges flat on the back wall, springs against its front. Six countersunk blind rivets from outside, heads flush.

### Step 4: thumb button onto the slider

![Step 4](05-build-plan/step-04.png)

One M3 screw through the button into the slider's top. Press the button: the tooth must pull in flush with the back face and spring back out.

### Step 5: plug shroud onto the connector face

![Step 5](05-build-plan/step-05.png)

Feed the plug's wires up through the lead opening, seat the shroud with the key notch at the back right, and fit four M3 screws from inside. Run a bead of sealant round the opening.

### Step 6: build the cell block

![Step 6](05-build-plan/step-06.png)

Push the 26 cells into both frames, then strip, fuse-wire and join the groups as section 3.6, one group at a time. **Hold point:** safety stops S1 and S2.

### Step 7: cell block into the tray

![Step 7](05-build-plan/step-07.png)

Lower the wrapped block into the tray with the frames' back edges on the back wall and fit four M2.5 countersunk screws from outside. Check no cell or strip touches the tray or the latch housing.

### Step 8: battery management board onto the right side wall

![Step 8](05-build-plan/step-08.png)

Fit the board on its four standoffs with M2.5 countersunk screws from outside, components toward the wall, and wire it as Figure 12 with the main fuse out. **Hold point:** safety stop S3.

### Step 9: carry handle onto the top end

![Step 9](05-build-plan/step-09.png)

Two M5 screws up from inside the tray into the inserts in the legs.

### Step 10: gasket and lid

![Step 10](05-build-plan/step-10.png)

Stick the gasket on the flanges, fit the main fuse, add the lid and tighten its eight screws in a cross pattern from the middle out. **Hold point:** safety stop S4.

### Step 11: cradle shelf onto the back plate

![Step 11](05-build-plan/step-11.png)

Four M5 countersunk screws from behind the plate into the shelf's inserts.

### Step 12: side guides onto the back plate

![Step 12](05-build-plan/step-12.png)

Each on two M5 countersunk screws from behind, bottom on the shelf, lead-ins at the top inside.

### Step 13: latch catch onto the back plate

![Step 13](05-build-plan/step-13.png)

Two M5 countersunk screws from behind, centred, 544 mm up the plate, latching face down.

### Step 14: receptacle into the shelf

![Step 14](05-build-plan/step-14.png)

Seen from below. Pass the wires down through the retainer's grommet, push the receptacle up into the cavity with its key post at the back right, then the foam pad and the retainer plate on four M3 screws.

### Step 15: controller box, charger and straps

![Step 15](05-build-plan/step-15.png)

The controller box on two M4 screws; the charger with its back on the plate; each strap over it on two M5 screws. Wire the dock as Figure 12 with the charger unplugged.

### Step 16: dock onto the wall

![Step 16](05-build-plan/step-16.png)

Four 6 mm screws into wall anchors in a non-combustible wall, the shelf top 0.8 to 1.2 m above the floor, away from exits. **Hold point:** safety stop S5.

### Step 17: pack into the dock

![Step 17](05-build-plan/step-17.png)

Lower the pack, connector end down, between the guides. It drops onto the shelf, the plug finds the receptacle, and the pawl snaps out under the catch. To remove it, press the thumb button and lift. **Hold point:** safety stop S6.

## 5. First checks

These are the checks a TRL 4 test report would record; this plan only lists them. Requirement numbers are those of SWC-REQ-001.

*Table 2. First checks.*

| Check | Requirement | How | Pass when |
| --- | --- | --- | --- |
| Envelope | R6 | Calipers and a rule on the closed pack | Body 340 x 90 x 80, within +0 and -1.5; 400 mm or less overall (393 expected); no head proud of the back or sides |
| Mass | R5 | Weigh the finished pack | 3.5 kg or less (3.03 kg estimated) |
| Output dead until seated | R11, R13 | Pack out of the dock: meter across PACK+ and PACK-; then a coin across INTERLOCK and signal ground | 0 V in both cases |
| Wake on the coding resistor | R13 | Seat the pack in the dock with the controller off | The board wakes and reports the loop valid; output stays off until a heartbeat |
| Sleep current | R13 | Meter in series with the cell block negative, board asleep | 100 µA or less |
| Handshake and log | R12 | Dock controller on; read the pack's identity and export its log | Identity read; log exported as CSV |
| Charge | R4 | Dock charges the pack from about 3.5 V per cell, attended, inside the fireproof enclosure | 5 A, give or take 0.25 A, in constant current; charging stops at 54.6 V, give or take 0.2 V |
| Cold charge lockout | R11, R14 | Replace one thermistor with a resistor equal to its value at -1 °C | Allowed charge current reads zero; no charge current flows |
| Latch hold | R15 (class D) | Lift the seated pack by the handle without pressing the button; then press and lift | It stays put; with the button pressed it lifts out |
| Swap | R7 | Time a one-handed swap; push the pack in with a spring scale | 10 s or less; 50 N or less |
| Receptacle float | R10 | Move the receptacle by hand with the pack out | 3 mm each way, returns level |
| Lid seal | R8 | Look at the gasket line under a lamp with the lid on | Evenly squeezed, no gaps (the spray test comes later) |

## 6. Safety stops

Stop at each point. Carry on only when everything listed is true.

- **S1. Before the cells come into the workshop.** Cells new, from an authorized distributor, with a datasheet; each between 3.4 and 3.7 V and within 0.05 V of the others; no dents or damaged wraps. A fireproof enclosure ready (a steel cabinet or a purpose-made battery containment box) on a non-combustible surface, with a lithium-rated or Class D extinguisher and a bucket of sand within reach. Insulated tools only.
- **S2. Before the cell block goes into the tray.** Every group voltage measured and within 0.05 V; every strip weld pulled by hand and every fuse wire intact; the block wrapped in fish paper; the tray liner in place; the battery management board not yet connected.
- **S3. Before the balance connector goes on.** Each sense lead measured at the connector, in order, rising by 3.0 to 4.2 V per pin; connected in the order the board's maker gives; the main fuse still out.
- **S4. Before the lid closes.** Main fuse in; with no receptacle, PACK+ to PACK- reads 0 V; a coin across INTERLOCK and signal ground still reads 0 V; no wire pinched or near the flange screws; the pack still inside the fireproof enclosure.
- **S5. Before the charger is plugged in.** Dock on a non-combustible wall, away from exits, with a smoke alarm nearby; charger certified and undamaged, on an RCD-protected socket; receptacle polarity checked with a meter against the plug; the charger's output measured at 54.6 V with no pack in.
- **S6. First charge in the dock.** The pack has completed one attended charge inside the fireproof enclosure. Stay with it the whole time; check the cell temperature every 15 minutes; stop if any cell passes 45 °C or any group passes 4.2 V. Never charge below 0 °C, never bypass the board's protections, and never charge a pack that has been dropped, crushed or wetted.
- **S7. Handling.** The pack weighs about 3 kg: carry it by the handle, never by the lid. Move it between rooms in a rigid, non-conductive container with the plug covered.

## 7. Tools, skills and workspace

**Tools.** Box-and-pan folder taking 1.5 mm aluminium 400 mm wide (or a sheet-metal shop); bench drill; drills 2.5 to 16 mm and a step drill; 90 degree countersink and one to suit the rivet heads; taps M3, M4 and M5 with their drills; hacksaw and bandsaw or jigsaw for 12 mm plate; flat and needle files; deburring tool; scriber, square, steel rule and calipers; bench vice with soft jaws; hand rivet tool for 3.2 and 4 mm rivets; 3D printer with an enclosure that prints ASA and flame-retardant PC-ABS, with a bed of at least 250 x 250 mm and 200 mm tall (350 mm for a printed lid); heat-set insert tip for a soldering iron; capacitor or battery spot welder for nickel strip; soldering iron; crimpers for ferrules, contacts and 6 mm² lugs; insulated hand tools; multimeter; bench power supply with a current limit; spring scale to 100 N; stopwatch; scale to 5 kg.

**Skills.** Basic sheet metal and metalwork (marking out, folding, drilling, tapping, filing, riveting), 3D printing, crimping and soldering, and experience of building lithium-ion packs with spot-welded strip under supervision. The pack works at up to 54.6 V DC and can deliver hundreds of amperes into a short, so treat it as a hazard at every stage. No mains wiring is part of this build: the charger is a certified plug-in unit.

**Workspace.** A bench about 1.5 x 0.7 m with a metalwork corner kept apart from the battery area so chips cannot reach the cells; a ventilated place for the printer; the fireproof enclosure of S1 for every stage from the cell block on; a non-combustible wall for the dock.

**Personal protective equipment.** Safety glasses for cutting, drilling, spot welding and soldering; cut-resistant gloves for sheet and plate edges; hearing protection when sawing; no gloves near a turning drill; no rings, watches or metal bracelets when working on the cells.

## 8. Where the numbers come from

- Model and constructability checks: `cad/src/model.py` (`python cad/src/model.py --check`); STEP and STL exports in `cad/step/` and `cad/stl/`.
- Pictures: `cad/src/build_plan_media.py`, using `.kit/build_views.py`; written to `docs/05-build-plan/` and `cad/drawings/SWC-DWG-101` to `SWC-DWG-115`.
- General arrangement: `cad/drawings/SWC-DWG-002.pdf`, Rev P3.
- Calculations: `docs/04-calcs/01-sizing.md` (SWC-CAL-001 v0.3) and `docs/04-calcs/sizing.py`: mass (section 3), thermal (section 4), latch (section 6), cost (section 8).
- Bill of materials: `bom/bom.csv` and `bom/bom-notes.md`.
- Decisions: `docs/decisions/0003-design-for-construction.md` (SWC-DDR-003), with SWC-DDR-001 and SWC-DDR-002.
- Requirements: `docs/03-requirements.md` (SWC-REQ-001 v0.5). Interface: `docs/02-concept.md` (SWC-PRC-001 v0.5).
