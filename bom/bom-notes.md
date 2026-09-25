# BOM notes

Every line in `bom/bom.csv` is priced (TRL 3). Prices are estimates for one-off purchase in 2026 US dollars, with a supplier or supplier type; they are not quotes. Item numbers match the exploded view (`media/exploded.png`), the components table in SWC-PRC-001 and drawing SWC-DWG-002; items 12 to 14 are not modelled. The totals below are printed by `docs/04-calcs/sizing.py` (SWC-CAL-001).

| Group | Items | Cost |
| --- | --- | --- |
| One pack | 1 to 7, 12 to 14 | $414 (cells $143) |
| One wall dock | 8 to 11 | $145 |
| Total | 1 to 14 | $559 |

Against the $700 budget in `project.yaml` (kept by Amish on 2026-09-25 for one pack and one dock), the margin is about $141. Changes since TRL 2: cell price raised from $4.50 to $5.50 for a named-brand high-power cell from an authorized distributor, latch pawl and tray upgraded for the class V1 proof load, and item 14 (wake button, interface v0.3) added.

**Shared packs.** By Amish's 2026-09-25 portfolio rule, the SwapCell pack is priced here only. Dependent kits (PowerBox, SunSpoke, StepGen, WaterWalker, CargoMule and others) exclude it from their budgets and cite this BOM.

A second pack for a real swap demonstration would add about $414 (total about $973). That build budget is open and awaiting Amish, and only matters once TRL 4 is lifted.

Cells must be new, matched and bought from an authorized distributor. Do not substitute recycled or unknown-grade cells in the reference pack.
