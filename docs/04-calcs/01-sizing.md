---
doc_id: SWC-CAL-001
title: SwapCell sizing and interface v0.3 calculations
project: SwapCell
doc_type: Calculation note
version: "0.1"
status: Draft
date: '2026-09-25'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-09-25'
  author: Amish Chadha
  change: First TRL 3 sizing note (electrical, mass, thermal, charge, wake, charge-discharge, latch, connector, CAN, cost)
---

# SwapCell sizing and interface v0.3 calculations

The 13S2P reference pack meets its voltage, charge time, mass, envelope, data and budget requirements on paper, and the three interface v0.3 additions are feasible with large margins. Two requirements stay **at risk**: R3 (cells reach about 51 °C in open air at 20 A but about 63 °C in an enclosed mount, and 20 A cannot be held from 45 °C ambient) and R9 (cycle life). R2 is at risk only at the datasheet minimum cell capacity. No requirement is shown to be not met. Connector, sealing, protections and latch retention (R7, R8, R10, R11, R15) cannot be verified until hardware exists, which is TRL 4 work and on hold by Amish's instruction.

Every number in this note is printed by `docs/04-calcs/sizing.py` (run from the repo root: `python docs/04-calcs/sizing.py`), which also writes `docs/04-calcs/results.csv`. All values are first-principles estimates; nothing here is measured.

## 1. Assumptions

*Table 1. Inputs. All are assumptions for a paper design.*

| Input | Value | Basis |
| --- | --- | --- |
| Cell | 21700, 5.0 Ah nominal, 4.85 Ah minimum, 3.6 V nominal, 3.0 to 4.2 V, 69 g, 12 mΩ DC, 25 A continuous | Typical high-power 5 Ah 21700 class; the model is chosen at supplier selection |
| Cell specific heat | 950 J/(kg K) | Typical for cylindrical NMC cells |
| Configuration | 13S2P, 26 cells | Decided, SWC-DDR-001 item 1 |
| Resistance outside the cells | 32 mΩ | Links, fuse wires, FETs, shunt, main fuse, connector |
| Resistance rise late in discharge and with age | x 1.25 on cell resistance | Sensitivity case |
| Fleet-mode capacity | 90 % of standard | Typical at 4.1 V per cell |
| Tray | 1.5 mm 5052 aluminium, 2.70 g/cm³, 900 J/(kg K) | Decided, SWC-DDR-001 item 2 |
| Lid | 3 mm flame-retardant polymer, 1.20 g/cm³ | PC/ABS class |
| External heat loss | 9 W/(m² K) | Still air, natural convection plus radiation |
| Cell core to tray | 0.10 K/W | Holders and thermal pads |
| Charger | 5 A CC-CV, 90 % efficient; CC to 85 %, then 0.6 h CV | Certified unit (decided) |
| Cell charge efficiency, motor and controller efficiency | 95 %, 80 % | Typical |
| Contact insertion forces | 12 N per power contact, 1.5 N per signal contact, 8 N latch detent | Assumed until the connector family is chosen |
| Vibration and shock for latch class V1 | 8 g peak sine; 25 g, 11 ms half-sine | UN 38.3 test T3 peak for batteries under 12 kg; 25 g is a proposed curb-strike level (SWC-DDR-001 item 19) |
| Receiver design mass | 3.5 kg | R5 limit, not the 2.85 kg pack |
| Sleep current | 100 µA | Target for a BMS asleep with the INTERLOCK comparator armed |
| INTERLOCK sensing | 100 kΩ pull-up from a 3.3 V sleep rail; 10 kΩ coding resistor in the receiver | Interface v0.3 item W |
| Host input capacitance, pre-charge resistor | 1,000 µF, 100 Ω | Typical 48 V controller |
| CAN frame | 135 bits worst case (11-bit ID, 8 data bytes, bit stuffing) | CAN 2.0A frame on a 2.0B-capable bus |
| Use | 2 swaps per day for 5 years | R10 basis |

## 2. Electrical

The pack gives 46.8 V nominal (39.0 to 54.6 V) and 10.0 Ah. At 0.2C the usable energy is about 466 Wh with nominal cells and about 452 Wh with cells at their 4.85 Ah minimum, which still clears the 450 Wh target but gives only 9.7 Ah against the 10 Ah target. In fleet mode (4.1 V per cell) the pack stores about 419 Wh; R2 applies to standard mode.

Pack resistance is about 110 mΩ (13 groups at 6 mΩ plus 32 mΩ). At 20 A each cell carries 10.0 A and the pack sags about 2.2 V; at 35 A each cell carries 17.5 A (rated 25 A) and the pack sags about 3.9 V.

For protections (R11): a bolted short at 54.6 V draws about 496 A, so a 500 µs trip lets through about 123 A²s, which sets the FET and main-fuse coordination. A cell with an internal short draws about 300 A from its parallel neighbour, which is the current the cell fuse wire must interrupt while carrying 17.5 A without damage. A 100 Ω pre-charge resistor charges 1,000 µF of host capacitance with a 100 ms time constant, reaching 99 % in about 460 ms and dissipating about 1.49 J.

## 3. Mass and size

*Table 2. Mass budget.*

| Part | Mass (kg) | Basis |
| --- | --- | --- |
| Cells | 1.79 | 26 x 69 g |
| Tray | 0.40 | 1.5 mm Al, back, two sides, two ends (computed from the envelope) |
| Lid | 0.11 | 3 mm over 340 x 90 mm |
| Interconnects, holders, insulation | 0.18 | Estimate |
| BMS board | 0.12 | Estimate |
| Plug | 0.06 | Estimate |
| Handle and latch pawl | 0.10 | Estimate |
| Seals, fasteners, wake button | 0.08 | Estimate |
| **Total** | **2.85 (6.3 lb)** | R5 limit 3.5 kg |

The body is 340 x 90 x 80 mm (2.45 L), giving about 164 Wh/kg and 191 Wh/L. The handle adds 35 mm and the plug 18 mm, so the overall length is 393 mm against the 400 mm limit. The parametric model (`cad/src/model.py`) reproduces these: pack 90 x 90 x 393 mm including the 10 mm latch pawl, body 90 x 80 x 340 mm with the wake button flush.

## 4. Thermal (R3)

A lumped model with heat loss replaces the TRL 2 adiabatic estimate. The pack heat capacity is about 2.26 kJ/K, the outer area 0.130 m², the loss conductance UA about 1.17 W/K and the thermal time constant about 32 min, close to the 30 min of a full discharge at 20 A. Cell hot-spot temperature is ambient plus the lumped rise, ΔT = (Q/UA)(1 - e^(-t/τ)), plus the core-to-tray drop.

*Table 3. Cell hot spot at the end of a full 20 A discharge.*

| Case | Heat | Open air from 25 °C | Enclosed (adiabatic) from 25 °C | Open air from 45 °C |
| --- | --- | --- | --- | --- |
| Base resistance | 44 W | 51 °C | 63 °C | 71 °C |
| Resistance x 1.25 | 52 W | 56 °C | 70 °C | 76 °C |

R3 is met in open air from 25 °C with 4 to 9 K margin, but fails in an enclosed vehicle mount and from 45 °C ambient. The continuous current that holds 60 °C from 45 °C in open air is about 14.0 A. At a typical e-bike 10 A the pack makes only about 11 W. R3 therefore stays **at risk**. The v0.3 behavior rules already derate PACK_LIMITS with temperature, so a hot pack lowers its own discharge limit. Recommendation (awaiting Amish, SWC-DDR-001 item 20): keep the 20 A rating at 25 °C with that derating, and require vehicle receivers to leave the back and lid faces open to air.

## 5. Charging and energy chain (R4)

At 5 A the CC phase to 85 % takes 1.70 h and the full charge about 2.3 h; 0 to 80 % takes 1.6 h and 20 to 80 % takes 1.2 h. R4 (3 h full, 2 h to 80 %) is met. The dock draws about 303 W from the grid in CC.

Per full cycle: about 547 Wh from grid or solar, 493 Wh out of the charger, 468 Wh stored, 457 Wh at the pack terminals (10 A mean) and about 366 Wh at the wheel. That gives about 38 to 57 km for an e-bike at 12 to 8 Wh/km and about 18 to 30 km for a loaded cargo trike at 25 to 15 Wh/km. Figure 2 of SWC-PRC-001 uses these values.

## 6. Interface v0.3 additions

**Wake without CAN or a wake supply (item W, R13).** In sleep the BMS holds INTERLOCK at 3.3 V through 100 kΩ. A v0.3 receiver loops INTERLOCK to SGND through 10 kΩ, pulling the node to about 0.30 V and drawing about 30 µA from the pack, so the host needs no supply of its own. A bridged short reads 0.00 V and an open loop 3.30 V; both are rejected, so a coin or wet debris across the contacts wakes the BMS but never enables the output. At 100 µA the sleep drain is about 0.72 % of capacity per month, so a half-charged pack takes about 5.7 years to sleep itself flat. R13 is met on paper.

**Charge while discharging (item C, R14).** A PowerBox station host with 200 W of solar in and a 20 W router load puts a net 3.8 A into the pack, inside the 5.0 A (0.5C) standard charge limit. StepGen-type regeneration of 5 to 10 W is far smaller. R14 is met on paper.

**Latch class V1 (item V, R15).** For a 3.5 kg pack, 8 g gives about 275 N and 25 g about 858 N along any axis. With a safety factor of 2, the latch proof load is about 1,717 N (1.72 kN). A steel pawl 36 mm wide with a 4 mm tooth sees about 12 MPa in shear and 36 MPa in bending at that load. Six 4 mm blind rivets in the 1.5 mm tray put about 48 MPa of bearing stress on the aluminium, a margin of about 4.2 against a conservative 200 MPa allowable, so a doubler is prudent but not essential. To stop the pack chattering on its contacts at 8 g, a vehicle receiver preloads the pack against its end stop with at least 1.2 x 275 = 330 N, which needs an over-centre lever ratio of at least 6.6 for a 50 N hand force. These are paper sizings; R15 is **not verifiable at TRL 3**.

## 7. Connector, CAN and log (R7, R10, R12)

With the assumed contact forces, insertion needs about 41 N, inside the 50 N limit of R7, but the forces depend on the connector family that is not yet chosen. Two swaps a day for five years is 3,650 mating cycles, so a 5,000-cycle rating gives a margin of about 1.37.

The v0.3 message set sends about 34.1 frames per second per pack, a bus load of about 1.8 % at 250 kbit/s, or about 3.1 % with two packs on one host. The 2,000-record log is 64,000 bytes (62.5 KiB); at half the bus it transfers in about 10 s. R12 is met on paper; CSV export is dock software, not verified.

## 8. Cost (R16)

*Table 4. Cost summary from `bom/bom.csv`.*

| Group | Items | Cost (USD) |
| --- | --- | --- |
| One pack | 1 to 7, 12 to 14 | 414 |
| One wall dock | 8 to 11 | 145 |
| **Total** | 1 to 14 | **559** |

The total is within the $700 budget with about $141 margin. Cells are about $143, or $0.31 per Wh. Per the portfolio rule (SWC-DDR-001), this is the only place a SwapCell pack is priced.

## 9. Results against requirements

*Table 5. Requirement status. Not met: none. Items at risk and not verifiable are listed first.*

| ID | Value (SWC-CAL-001) | Target | Status |
| --- | --- | --- | --- |
| R3 | 51 °C open air, 56 °C with higher resistance; 63 °C enclosed; 17.5 A per cell at 35 A | Cells below 60 °C from 25 °C at 20 A; 35 A for 10 s | At risk |
| R9 | 300 to 500 cycles typical for the cell class; 4.1 V fleet mode adopted | 500 cycles to 80 %; SoH within 5 % | At risk |
| R2 | 10.0 Ah and 466 Wh nominal; 9.7 Ah and 452 Wh at cell minimum | 10 Ah and 450 Wh at 0.2C | At risk |
| R7 | About 41 N insertion with assumed contact forces | 10 s, one hand, 50 N or less | Not verifiable at TRL 3 |
| R8 | Gasketed lid, potted pack-side contacts (design review only) | Pack IP65, dock IP54 | Not verifiable at TRL 3 |
| R10 | 3,650 cycles in 5 years, margin 1.37; family not chosen | 5,000 cycles, ±3 mm, ±2°, 40 A | Not verifiable at TRL 3 |
| R11 | Short circuit 496 A, 123 A²s in 500 µs; pre-charge 460 ms; functions specified | Protections listed in R11 | Not verifiable at TRL 3 |
| R15 | Proof load 1.72 kN; rivet bearing margin 4.2; lever ratio 6.6 | Class V1 vibration and shock, no release | Not verifiable at TRL 3 |
| R1 | 46.8 V nominal, 39.0 to 54.6 V | 46.8 V; 39.0 to 54.6 V | Met |
| R4 | 2.3 h full; 1.6 h to 80 % | 3 h full; 2 h to 80 % | Met |
| R5 | 2.85 kg | 3.5 kg or less | Met |
| R6 | 340 x 90 x 80 mm; 393 mm overall | 400 mm or less overall | Met |
| R12 | Bus load 1.8 %; log 62.5 KiB in about 10 s | CAN 250 kbit/s, 2,000 records, CSV export | Met (on paper) |
| R13 | Sleep drain 0.72 % per month; coded INTERLOCK at 0.30 V | Wake with no host supply; 1 % per month or less | Met (on paper) |
| R14 | Net 3.8 A charge in the PowerBox case, within 5.0 A | Charge-discharge mode within limits | Met (on paper) |
| R16 | $559 for one pack and one dock | $700 | Met |

## 10. Checks against earlier documents

The TRL 2 figures in SWC-PRC-001 v0.2 were checked against this script and corrected in v0.3: mass 2.8 to 2.85 kg, grid energy 550 to 547 Wh, terminal energy 454 to 457 Wh, pack parts $370 to $414 (cell price raised from $4.50 to $5.50 and a wake button added), adiabatic rise 36 to 35 K with a better heat capacity, and 0 to 80 % charge time stated as 1.6 h. The log size is 64,000 bytes (62.5 KiB), not "64 kB" of binary kilobytes.

> **Safety:** These calculations concern a 468 Wh lithium-ion pack that can deliver about 500 A into a short. They are paper estimates and do not replace protection design review or testing. No pack may be built or charged from this note; building and testing are TRL 4 work and on hold.
