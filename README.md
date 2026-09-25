# SwapCell

![TRL 3](https://img.shields.io/badge/TRL-3%20of%209-0F766E) ![Hardware: CERN-OHL-S-2.0](https://img.shields.io/badge/hardware-CERN--OHL--S--2.0-111827) ![Software: MIT](https://img.shields.io/badge/software-MIT-111827)

**Area:** Mobility and Logistics · **TRL:** 3 of 9 (proof of concept on paper) · **Prototype budget:** about $700 USD · **Difficulty:** 4 of 5

Open-standard swappable battery pack and wall dock for e-bikes, scooters and cargo trikes, with a defined connector, CAN-based BMS protocol and state-of-health logging.

![SwapCell concept](media/hero.png)

[Interactive 3D model](media/viewer.html) · [Concept blueprint (PDF)](media/concept-blueprint.pdf) · [Review note](docs/REVIEW.md)

## Problem

Every light electric vehicle brand uses its own battery, so fleets cannot share packs or chargers and batteries are scrapped early.

## Concept

Open-standard swappable battery pack and wall dock for e-bikes, scooters and cargo trikes, with a defined connector, CAN-based BMS protocol and state-of-health logging.

The core deliverable is the open **SwapCell interface v0.3**: envelope, blind-mate pinout with a coded interlock, CAN message set with a full bit layout, wake for hosts without CAN, a charge-while-discharging mode and a vehicle latch rating. Other portfolio designs build to it.

Full design precis: [docs/02-concept.md](docs/02-concept.md) · Sizing note: [docs/04-calcs/01-sizing.md](docs/04-calcs/01-sizing.md) · General arrangement: [cad/drawings/SWC-DWG-002.pdf](cad/drawings/SWC-DWG-002.pdf)

## Key components

- 26 x 21700 cells in 13S2P: 46.8 V, 10 Ah, about 468 Wh, about 2.85 kg
- Open-source BMS with CAN
- Folded aluminium tray with a printed flame-retardant lid
- Blind-mate power and signal connector with a coded interlock
- Certified 5 A dock charger
- Latch pawl rated for vehicle class V1
- ESP32 dock controller

The priced bill of materials is in [bom/bom.csv](bom/bom.csv): about $559 for one pack and one dock, within the $700 budget.

## Safety

> Contains a 468 Wh lithium-ion battery pack at up to 54.6 V DC. Use a BMS with cell-level protection, fuse the pack, and charge on a non-combustible surface. Build and test packs only inside a fireproof enclosure, never unattended. This is a paper design at TRL 3; nothing here is certified.

## Repository layout

| Folder | Contents |
| --- | --- |
| `docs/` | Problem, concept, requirements, calculations and design decisions |
| `cad/src/` | build123d Python source, the source of truth for all geometry |
| `cad/step/`, `cad/stl/` | Exported models for FreeCAD, other CAD tools and printing |
| `cad/drawings/` | 2D sketches and dimensioned drawings |
| `bom/` | Bill of materials |
| `electronics/` | KiCad schematics and PCB layouts |
| `firmware/` | Microcontroller code |
| `media/` | Renders, perspectives and photos |
| `build-log/` | Dated prototyping notes |

## Documentation

Controlled documents follow the portfolio [documentation standard](.kit/STANDARDS.md). Each carries a document ID (SWC-PRC-001 for the precis), a version and a revision history. Branded PDFs are built with `python .kit/render.py` and attached to GitHub Releases when a document is tagged, for example `SWC-PRC-001/v1.0`.

## Licenses

- **Hardware** (CAD, drawings, BOM, electronics): [CERN-OHL-S v2](LICENSE)
- **Software** (firmware, scripts, notebooks): [MIT](LICENSE-SOFTWARE)

Part of the open hardware portfolio at [amishchadha.com](https://amishchadha.com).
