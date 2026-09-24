# SwapCell

**Area:** Mobility and Logistics · **Status:** Concept · **Prototype budget:** about $700 USD · **Difficulty:** 4 of 5

Open-standard swappable battery pack and wall dock for e-bikes, scooters and cargo trikes, with a defined connector, CAN-based BMS protocol and state-of-health logging.

## Problem

Every light electric vehicle brand uses its own battery, so fleets cannot share packs or chargers and batteries are scrapped early.

## Concept

Open-standard swappable battery pack and wall dock for e-bikes, scooters and cargo trikes, with a defined connector, CAN-based BMS protocol and state-of-health logging.

Full design precis: [docs/02-concept.md](docs/02-concept.md)

## Key components

- 18650 or 21700 cells in a 48 V 10 Ah configuration
- Open-source BMS with CAN
- Printed or molded pack housing
- Blind-mate power connector
- Dock charger 5 A
- Latch mechanism
- ESP32 dock controller

The working bill of materials is in [bom/bom.csv](bom/bom.csv).

## Safety

> Contains a lithium battery pack. Use a BMS with cell-level protection, fuse the pack, and charge on a non-combustible surface. Build and test packs inside a fireproof enclosure.

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

## Licenses

- **Hardware** (CAD, drawings, BOM, electronics): [CERN-OHL-S v2](LICENSE)
- **Software** (firmware, scripts, notebooks): [MIT](LICENSE-SOFTWARE)

Part of the open hardware portfolio at [amishchadha.com](https://amishchadha.com).
