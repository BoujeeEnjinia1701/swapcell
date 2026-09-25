---
doc_id: SWC-PRB-001
title: SwapCell problem statement
project: SwapCell
doc_type: Problem statement
version: "0.3"
status: Draft
date: '2026-09-25'
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
  change: Populate to TRL 2 (users, context, constraints, out of scope, prior work)
- version: "0.3"
  date: '2026-09-25'
  author: Amish Chadha
  change: TRL 3. Record Amish's 2026-09-25 decisions (SWC-DDR-001); dependents and needs updated for interface v0.3; budget scope
---

# SwapCell problem statement

Light electric vehicles run on batteries that only fit one brand, often one model, so a fleet with three vehicle types keeps three sets of packs and chargers, a flat pack cannot be swapped between vehicles, and a pack with one weak cell group is scrapped because nobody outside the brand can read its data or open it.

## The problem

E-bikes, e-scooters and cargo trikes mostly use 36 V or 48 V lithium-ion packs of 300 to 700 Wh. The cells inside are commodity 18650 or 21700 cells, but the housing, connector, mounting and battery management system (BMS) protocol are proprietary. The consequences are practical:

- **Fleets cannot share.** A delivery or rental operator with mixed vehicles must stock a separate pack and charger family for each, and cannot move charged packs to whichever vehicle is working.
- **Downtime is charge time.** Without a swappable pack, a vehicle stands still for 3 to 6 hours while it charges. Swapping takes seconds.
- **Packs die early and blind.** Without access to state-of-health (SoH) data, operators replace packs on a schedule or after failure. A pack that could be rebalanced, repaired or moved to a lighter duty is recycled instead.
- **Repair is locked out.** Independent repair shops cannot diagnose a pack whose BMS speaks a closed protocol, and a replacement from the original brand may cost more than the vehicle is worth.
- **Small builders have no target.** An open vehicle design (for example the SunSpoke e-bike kit or the WaterWalker assist in this portfolio) has no common pack to design around, so each project reinvents the battery.

SwapCell proposes an open, documented interface: one pack envelope, one blind-mate connector with a published pinout, one CAN message set, and a wall dock that charges and reads any conforming pack. The interface definition matters more than any single pack build, because other designs in the portfolio (PowerBox, SunSpoke, StepGen, WaterWalker, CargoMule, FieldCell and others) plan to use it. Their TRL 2 reviews raised three needs the v0.2 interface did not meet: waking a pack from a host that has no CAN or no wake supply, running loads while charging, and holding a pack in a vehicle under vibration. Amish approved adding all three on 2026-09-25; they are SwapCell interface v0.3 (SWC-PRC-001 v0.3, SWC-DDR-001).

## Users and context

| User | Need | Context |
| --- | --- | --- |
| Fleet operator (delivery, rental, campus or municipal) | Share packs and docks across vehicle types; swap in seconds; see which packs are ageing | Depot with a row of wall docks; 1 to 3 swaps per vehicle per day |
| Rural e-bike or cargo-trike user | Carry a spare pack; charge from a small solar system or a shared village dock; repair locally | Unreliable grid, long distances, heat and dust |
| Repair shop or community workshop | Read pack history, find a weak cell group, replace cells and return the pack to service | Workbench with a dock and a laptop |
| Open hardware builder | A pack and interface to design a vehicle or power product around | Makerspace or small workshop |
| Portfolio integrator (PowerBox, SunSpoke, StepGen, WaterWalker, CargoMule, FieldCell) | A stable mechanical envelope, pinout and message set to design to now, including wake without CAN, charge while discharging, and a vehicle latch rating | Paper design at TRL 2 and 3 |

## Constraints

- Garage-buildable prototype of one pack and one dock for about $700 USD (budget in `project.yaml`, kept by Amish on 2026-09-25), using commodity cells, an open-source BMS and off-the-shelf connectors and chargers. A SwapCell pack is priced once, in this repo, and excluded from the budgets of dependent kits.
- Lithium-ion cells are hazardous. Assembly needs a spot welder, cells from a reputable distributor (no recycled or unknown-grade cells for the reference pack), and a fire-safe space for building, charging and testing.
- The prototype uses a certified off-the-shelf mains charger. No custom mains-voltage electronics are built.
- Electrically compatible with common 48 V light-vehicle motor controllers (typical low-voltage cutoff 39 to 42 V, maximum input about 60 V).
- One-hand carry and swap, including by users with limited grip strength.
- Outdoor use: rain, dust, vibration and temperatures from about -10 °C to 45 °C during use.
- The interface documents must be publishable under the portfolio licenses, so the design cannot depend on a specification that users must buy or sign to read.

## Out of scope

- Automated or robotic swap stations, payment, booking and user accounts.
- A cloud fleet platform. The dock exports logs locally; any server is the operator's choice.
- Motor controllers and vehicle frames, beyond the mount that receives the pack.
- Fast charging above 1C and battery chemistries other than lithium-ion NMC or NCA cells in the reference pack (an LFP variant is an open question).
- Certification testing. Relevant standards are listed as future targets, not claims.

## Prior work

- **Proprietary swapping networks.** Scooter swapping networks in Taiwan and India, and battery-sharing services in Europe, show that swapping works at scale, but each network uses its own pack and closed data.
- **Industry consortia.** Several large motorcycle makers formed a consortium to agree a common swappable pack for small electric motorcycles, and at least one maker sells a swappable pack family used across its own products. These are designed for 50 cc to 125 cc class vehicles, larger than the e-bike and cargo-trike packs targeted here, and their documents are not open.
- **EnergyBus (CAN in Automation profile 454).** An existing CANopen-based standard for light electric vehicle batteries, chargers and connectors. It is the closest precedent for the SwapCell message set. Its adoption in the e-bike market has been limited, and the specification is distributed through a membership organization.
- **E-bike integrated packs.** Mainstream e-bike drive systems use proprietary down-tube or rack packs with keyed connectors and closed BMS protocols.
- **DIY down-tube cases.** Generic "down-tube" pack cases for 13S packs are widely sold for hobby e-bikes and act as an informal mechanical standard, but they have no defined connector or data interface.
- **Open-source BMS projects.** Several open BMS designs for 12S to 18S packs with CAN exist and can serve as the starting point for the SwapCell BMS.
- **Regulation.** The EU Batteries Regulation (2023/1542) covers batteries for light means of transport and expects state-of-health information to be available from the BMS, which supports the SwapCell SoH logging requirement.

## Open questions

- Which user group to design with first: a delivery fleet, a rural e-bike cooperative, or a repair workshop? Still open: the portfolio picks co-design partners per area later. Proposed, awaiting Amish.
- Message set: decided by Amish, 2026-09-25: an open SwapCell profile with an EnergyBus gateway study (SWC-DDR-001 item 4).
