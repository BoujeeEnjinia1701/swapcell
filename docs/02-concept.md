---
doc_id: SWC-PRC-001
title: SwapCell design precis
project: SwapCell
doc_type: Design precis
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
  change: Populate to TRL 2 (architecture, interface definition, first-order numbers, safety, media)
---

# SwapCell design precis

SwapCell is a 48 V, 10 Ah lithium-ion pack of 26 cells in a 340 x 90 x 80 mm body that drops, connector first, into a wall dock or a vehicle mount, mates through a floating blind-mate connector, and talks to whatever it is plugged into over CAN. The pack carries its own state-of-health log, so any dock can read its history. First-order numbers suggest a 13S2P pack of 21700 cells gives about 470 Wh at about 2.8 kg, charges in about 2.3 h on a 5 A dock, and costs about $370 in prototype parts, with the dock adding about $145.

The interface (envelope, pinout and message set) is the core deliverable of this precis. The SunSpoke, PowerBox, FieldCell and WaterWalker designs plan to build to it.

![Hero render](../media/hero.png)

*Figure 1. Pack seated in the wall dock, with a hand on the carry handle for scale. Massing model.*

## How it works

1. **Dock.** The pack hangs connector end down in a wall cradle. Side guides bring it within the connector's capture range, gravity seats it, and a spring latch on the back face clicks into a catch on the cradle.
2. **Mate.** The blind-mate connector makes contact in sequence: ground first, then power and CAN, and a short interlock pin last. Until the interlock closes, the pack output is dead.
3. **Handshake.** The dock controller (ESP32 with a CAN transceiver) sends a heartbeat. The pack answers with its identity, limits and state of health. If the pack reports no fault and a charge limit of at least 5 A, the dock switches its certified 54.6 V, 5 A charger onto the pack.
4. **Charge and log.** The BMS balances cells, limits charge by temperature and records each cycle. The dock copies new cycle records to its SD card and exports them as CSV.
5. **Swap.** The rider lifts the pack by the handle, releases the latch with the same hand, and slides it into the vehicle mount, which mirrors the dock cradle. The vehicle controller runs the same handshake, and the pack enables its output.

![System and energy flow](../media/flow.png)

*Figure 2. Energy per full charge and discharge, grid or solar to wheel. All values are estimates.*

## Main components

| # | Component | Proposed choice | Notes |
| --- | --- | --- | --- |
| 1 | Pack housing tray | Folded 1.5 mm aluminium, open front, flame-retardant liner | Carries the latch and handle loads; spreads heat. Proposed, awaiting Amish |
| 2 | Cell block | 26 x 21700 cells, 13S2P, about 5.0 Ah and 3.6 V nominal each, 20 A or more continuous rating | Cells in holders with fuse-wire links |
| 3 | BMS board | Open-source 13S BMS with CAN, balancing, 30 A continuous FETs, pre-charge and flash log | Stands beside the cells on its long edge |
| 4 | Pack lid | Flame-retardant polymer (UL 94 V-0 grade), gasketed | Removable for repair |
| 5 | Blind-mate plug, pack side | 2 power contacts (40 A) plus 6 signal contacts in a keyed shroud | Fixed to the pack; see the interface section |
| 6 | Carry handle | Moulded loop over the top end, 25 mm grip clearance | Sized for a gloved hand |
| 7 | Latch pawl | Spring-loaded pawl on the back face, thumb release under the handle | Same catch geometry on dock and vehicle |
| 8 | Wall dock cradle | Back plate, cradle shelf with connector pocket, side guides and latch catch | Wall-mounted at 0.8 to 1.2 m |
| 9 | Blind-mate receptacle, dock side | Mating half on a floating mount (±3 mm, ±2°) | Replaceable wear part |
| 10 | Dock charger | Certified 54.6 V, 5 A CC-CV lithium-ion charger | Off-the-shelf; no custom mains electronics |
| 11 | Dock controller | ESP32 with CAN transceiver, charger relay, current sensor and SD card | Runs the handshake and exports logs |

Items 12 (fuses, pre-charge and wiring) and 13 (seals, foam and fasteners) are in the BOM but not modelled. Numbers match `bom/bom.csv` and Figure 4.

## First-order numbers

All values are estimates for concept review and will be checked at TRL 3. Assumptions: 21700 cell at 5.0 Ah, 3.6 V nominal, 4.2 V maximum, 3.0 V minimum, about 69 g, about 12 mΩ DC internal resistance and a 25 A continuous rating (a common high-power 5 Ah class); cell price about $4.50 in small quantity.

| Quantity | Estimate | Basis | Requirement |
| --- | --- | --- | --- |
| Configuration | 13S2P, 26 cells | 13 in series for the 48 V class; 2 in parallel for 10 Ah | |
| Voltage | 46.8 V nominal, 39.0 to 54.6 V | 13 x 3.6 V; 13 x 3.0 to 4.2 V | R1 met |
| Capacity and energy | 10.0 Ah, about 468 Wh | 2 x 5.0 Ah x 46.8 V | R2 met |
| Pack resistance | about 110 mΩ | 13 groups x 6 mΩ, plus about 32 mΩ for links, fuse wires, FETs, shunt and connector | |
| Cell current | 10 A continuous, 17.5 A peak | 20 A and 35 A shared by 2 cells; cells rated 25 A | R3 electrically met |
| Heat at 20 A | about 44 W; about 36 K rise over a full 30 min discharge | I²R at 110 mΩ; adiabatic, about 2.2 kJ/K for cells and tray | R3 thermally **at risk**: about 61 °C from 25 °C |
| Heat at 10 A (typical e-bike) | about 11 W; about 18 K rise over 1 h | Same basis | |
| Voltage sag | about 2.2 V at 20 A, 3.9 V at 35 A | I x 110 mΩ | |
| Mass | about 2.8 kg (6.2 lb) | Cells 1.79 kg, interconnects and insulation 0.18, BMS 0.12, tray 0.39, lid 0.11, connector 0.06, handle and latch 0.10, seals and fasteners 0.08 | R5 met (3.5 kg) |
| Body and overall size | 340 x 90 x 80 mm; about 393 mm long with handle and plug | Cell block 286 x 44 x 70 mm plus BMS, walls and clearance | R6 met |
| Energy density | about 167 Wh/kg, about 190 Wh/L | 468 Wh over 2.8 kg and 2.45 L | |
| Charge time at 5 A | about 2.3 h to full; about 1.2 h for 20 to 80 % | CC to about 85 % in 1.7 h, then about 0.6 h CV | R4 met |
| Dock input power | about 300 W while in CC | 54.6 V x 5 A at about 90 % charger efficiency | |
| Energy per cycle | about 550 Wh from grid or solar, about 454 Wh at the pack terminals | Figure 2: charger 90 %, cell charge 95 %, pack resistance 97 % | |
| Range | about 40 to 55 km (e-bike), 18 to 30 km (loaded cargo trike) | 454 Wh at 8 to 12 Wh/km and 15 to 25 Wh/km | |
| Cell cost | about $117, about $0.25/Wh | 26 x $4.50 | |
| Parts cost | about $370 per pack, about $145 per dock | Indicative prices, see `bom/bom.csv` | Within $700 for one of each |
| Cycle life | about 300 to 500 cycles to 80 % | Typical for 5 Ah 21700 cells at 0.5C; higher with a 4.1 V charge limit | R9 **at risk** |

![Cutaway](../media/cutaway.png)

*Figure 3. Section through the docked pack: cells (2) with their axes across the width, BMS board (3) beside them, plug (5) in the dock pocket.*

## Interface definition

This section is the SwapCell interface, version 0.2 (draft). Every value is proposed, awaiting Amish. Other portfolio designs should build to it and flag any conflict rather than change it locally.

### Mechanical envelope

| Feature | Value (proposed) | Notes |
| --- | --- | --- |
| Body | 340 x 90 x 80 mm, +0 / -1.5 mm | Length along the insertion axis |
| Datum | Connector face (pack underside); insertion along the long axis, connector first | Same in dock and vehicle mount |
| Connector position | Centred across the 90 mm width, 8 mm toward the back face from the depth centre line | Keeps the plug clear of the lid seam |
| Guide faces | The two 340 x 80 mm side faces, 90 mm apart | Receiver guides with 1 mm clearance per side and a 10 mm lead-in |
| Latch | Pawl on the back face, 45 mm below the top end, 36 mm wide; engages a catch on the receiver | Holds the pack against 3 g vertical shock (target, to confirm) |
| Handle zone | Up to 35 mm above the top end, 84 x 22 mm footprint | Receivers leave this zone clear |
| Orientation | Any; the latch, not gravity, retains the pack in a vehicle | Dock uses gravity to seat |
| Mass limit for receivers | 3.5 kg pack | R5 |

### Connector pinout

Two power contacts and six signal contacts in a keyed shroud that only mates one way round. Mating order is set by contact length.

| Pin | Signal | Rating | Mates | Function |
| --- | --- | --- | --- | --- |
| P1 | PACK+ | 40 A continuous | 2nd | Pack positive, behind the BMS FETs; dead until enabled |
| P2 | PACK- | 40 A continuous | 1st | Pack negative |
| S1 | SGND | 1 A | 1st | Signal ground and CAN reference, joined to PACK- inside the pack |
| S2 | CAN_H | Signal | 2nd | CAN 2.0B, 250 kbit/s; 120 Ω termination in the host, not the pack |
| S3 | CAN_L | Signal | 2nd | As above |
| S4 | WAKE | 5 to 15 V, 10 mA | 2nd | Host drives high to wake the BMS from sleep |
| S5 | AUX | 12 V, 1 A (reserved) | 2nd | Proposed low-power output for lights or a dock display; off by default |
| S6 | INTERLOCK | Signal | 3rd (last) | Loops to SGND in the receiver; the pack enables nothing until it closes and opens its output first on removal |

### CAN message set (outline)

CAN 2.0B, 250 kbit/s, 11-bit identifiers. Each pack has a node number n from 0 to 7 (default 0) so a vehicle can carry two packs; identifiers below are base values plus n. Little-endian signals, scaled integers. The full bit layout is TRL 3 work.

| ID (base) | Message | Direction | Rate | Content |
| --- | --- | --- | --- | --- |
| 0x100 | PACK_STATUS | Pack to host | 10 Hz | Voltage (10 mV), current (100 mA, signed), state of charge (0.5 %), state (sleep, standby, discharge, charge, fault) |
| 0x110 | PACK_LIMITS | Pack to host | 10 Hz | Allowed discharge current, allowed charge current, maximum charge voltage, minimum voltage, all derated for temperature and state of charge |
| 0x120 | CELL_SUMMARY | Pack to host | 1 Hz | Minimum and maximum cell voltage with group index, imbalance |
| 0x130 | TEMPERATURES | Pack to host | 1 Hz | Minimum and maximum cell temperature, FET and connector temperature |
| 0x140 | FAULTS | Pack to host | On change and 1 Hz | Fault and warning bits, seconds until the pack will disconnect |
| 0x150 | STATE_OF_HEALTH | Pack to host | 0.1 Hz | SoH (%), full-charge capacity, cycle count, lifetime Ah throughput, resistance estimate |
| 0x160 | IDENTITY | Pack to host | On request | Protocol version, serial number, chemistry, configuration (13S2P), rated Ah, firmware version |
| 0x180 | HOST_HEARTBEAT | Host to pack | 10 Hz | Host type (vehicle, dock, tester), requested mode (discharge, charge, sleep), host current limit, rolling counter |
| 0x190 | CHARGER_STATUS | Dock to pack | 1 Hz | Charger capability, measured output voltage and current |
| 0x1F0 / 0x1F8 | LOG_REQUEST / LOG_DATA | Dock to pack / pack to dock | On request | Segmented transfer of stored cycle records (ISO 15765-2 style) |

**Behavior rules (proposed).** The pack enables discharge only with INTERLOCK closed and a valid heartbeat requesting discharge, and charge only with a dock heartbeat requesting charge. For a non-fatal fault it first warns and ramps its current limit down over about 5 s, so a rider is not left without power mid-junction; it opens immediately only for short circuit, cell overvoltage or over-temperature beyond the hard limit.

**State-of-health log.** One 32-byte record per charge or discharge event: dock timestamp, Ah in and out, minimum and maximum temperature, peak current, minimum cell voltage, capacity and resistance estimates. 2,000 records need 64 kB, which fits in the BMS microcontroller flash or a small SPI flash (R12).

## Key design choices

- **13S2P of 5 Ah 21700 cells.** Meets 10 Ah with 26 cells and 52 welds. Alternatives: 13S3P of 3.4 Ah 18650 cells (same capacity, 39 cells, about 0.3 kg heavier, more welds) or 13S4P of 21700 cells (about 19 Ah and 900 Wh, but about 5 kg, beyond one-hand carry). Recommendation: 13S2P as the reference pack, with a 13S4P "double" pack as a later variant in a longer envelope. Proposed, awaiting Amish.
- **Aluminium tray with a polymer lid.** Metal spreads heat, resists a cell fire longer than a printed shell and carries latch loads. An all-printed housing is cheaper and faster to iterate. Recommendation: aluminium tray, printed flame-retardant lid and caps. Proposed, awaiting Amish.
- **Floating blind-mate connector with a dead pack output.** Sequenced contacts and a last-mate interlock let the pack keep its output off until it is fully seated and has a host, which avoids arcing on insertion and live contacts on a loose pack. Proposed, awaiting Amish.
- **Own open message set, not EnergyBus, for the first release.** A short, published SwapCell profile is easy to implement on an ESP32 or a hobby motor controller and can be released under the portfolio licenses. Option: adopt EnergyBus (CiA 454) directly, which is more complete and already recognized, but is CANopen-based, heavier to implement and distributed through a membership organization. Recommendation: SwapCell profile now, with a gateway study at TRL 3. Proposed, awaiting Amish.
- **Legacy mode for vehicles without CAN.** If INTERLOCK closes and no heartbeat arrives within 2 s, the pack enables discharge only, limited to 15 A, and never charges. This lets the pack drive existing hub-motor kits. Option: no legacy mode, CAN always required (safer, less compatible). Recommendation: legacy mode on, fixed at 15 A. Proposed, awaiting Amish.
- **The log lives in the pack.** Any dock, anywhere, can read a pack's history without a shared server, which suits rural users and repair shops. Proposed, awaiting Amish.
- **Certified charger, switched by the dock.** The dock controller only switches the DC output of a certified charger; it builds no mains electronics. The cost is that the charge current is fixed at 5 A, so a cold or hot pack that allows less simply waits. Proposed, awaiting Amish.

![Exploded view](../media/exploded.png)

*Figure 4. Exploded view with callouts numbered as in the components table and `bom/bom.csv`.*

## Safety

> **Safety:** SwapCell is a 470 Wh lithium-ion pack. A cell in thermal runaway vents flammable, toxic gas and can ignite its neighbours; a pack fire is hard to extinguish and can re-ignite hours later. Treat every pack as a fire hazard at all stages.

- **Thermal runaway.** Use new cells from a reputable distributor, with matched capacity and resistance. Space cells in holders (about 1 mm gaps) and consider a mica or intumescent barrier between groups; line the tray with a flame-retardant sheet; give the housing a vent path that directs gas away from the handle and the user. Propagation resistance is a TRL 3 question.
- **Cell-level fusing.** Each cell connects to its bus through a fuse wire or fusible link sized to carry 17.5 A peak without damage but to open on the fault current of an internally shorted neighbour. A 40 A main fuse sits in series with PACK+.
- **BMS protections (R11).** Cell overvoltage and undervoltage, charge and discharge overcurrent, short-circuit trip within 500 µs, over-temperature, no charging below 0 °C, pre-charge of the host's input capacitors, and an output that stays off until the interlock closes. Exposed pack contacts are at up to 54.6 V DC and can deliver hundreds of amperes into a short, so the dead-output rule is a safety requirement, not a convenience.
- **Loss of power while riding.** A pack that cuts out suddenly can cause a fall. The warn-then-derate rule in the message set applies to every fault except the hard ones.
- **Dock location.** Mount docks on a non-combustible wall, away from exits and escape routes, with a smoke alarm nearby. Do not charge packs that have been dropped, crushed or wetted until they have been inspected.
- **Transport rules.** At about 468 Wh the pack is well above 100 Wh, so it ships as Class 9 dangerous goods (UN 3480 alone, UN 3481 in or with equipment), needs a UN 38.3 test summary before commercial shipping, cannot travel in passenger air baggage, and by air generally has to ship at 30 % state of charge or less. Moving prototype packs by road between workshops still needs terminal protection and a rigid, non-conductive container.
- **Building and testing.** Build, charge and test prototype packs only inside a fireproof enclosure (a steel cabinet or a purpose-made battery containment box) on a non-combustible surface, with a Class D or lithium-rated extinguisher and a sand bucket at hand, and never unattended. Use insulated tools, cover exposed bus bars, and build the pack one series group at a time with the BMS disconnected until wiring is checked.
- **Standards.** EN 50604-1 and UL 2271 (light-vehicle batteries), UL 2849 (e-bike electrical systems) and IEC 62133-2 are future compliance targets. Nothing here is certified.

## Open questions for TRL 3

- Thermal: does R3 hold at 20 A from 45 °C ambient, or should the continuous rating fall to about 15 A? A lumped thermal model is the first TRL 3 calculation.
- Cell choice: which 5 Ah 21700 cell balances cycle life (R9) against current rating, and should a fleet mode charge to 4.1 V per cell (about 53.3 V) for longer life at about 10 % less capacity? Proposed: offer both modes, set by the dock. Awaiting Amish.
- An LFP variant (16S of 32700 or 26650 cells, about 51 V nominal, up to 58.4 V) would be safer and longer lived but heavier. Can it share the envelope and message set? The limits message already allows a different voltage window.
- Connector: which commercial blind-mate family meets R10 at this cost, or does the prototype need a custom shroud around standard spring contacts?
- Latch retention in a vehicle: what shock and vibration loads should the latch meet (3 g is a placeholder)?
- Should the dock also accept a 48 V DC solar input (via PowerBox) as well as mains? Proposed: yes, as a second dock variant after the mains dock. Awaiting Amish.
- Governance of the interface: who approves changes once SunSpoke, PowerBox, FieldCell and WaterWalker build to it? Proposed: a versioned interface document under this repo, changes approved by Amish. Awaiting Amish.

Concept media: [blueprint sheet](../media/concept-blueprint.pdf), [interactive 3D model](../media/viewer.html).
