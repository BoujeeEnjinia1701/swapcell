# BOM notes

Every line in `bom/bom.csv` is priced (TRL 3). Prices are estimates for one-off purchase in 2026 US dollars, with a supplier or supplier type; they are not quotes. Item numbers 1 to 11 match the exploded view (`media/exploded.png`), the components table in SWC-PRC-001 and drawing SWC-DWG-002; the build plan SWC-BLD-001 shows every made item. The totals below are printed by `docs/04-calcs/sizing.py` (SWC-CAL-001).

| Group | Items | Cost |
| --- | --- | --- |
| One pack | 1 to 7, 12 to 16 | USD 449 (cells USD 143) |
| One wall dock | 8 to 11, 17 | USD 170 |
| Total | 1 to 17 | USD 619 |

Value-engineering target: USD 700 (`budget_usd` in `project.yaml`, a hypothetical control target, not a limit). Estimated cost of the constructable design: USD 619 (USD 81 under the target). Changes since TRL 2: cell price raised from USD 4.50 to USD 5.50 for a named-brand high-power cell from an authorized distributor, latch pawl and tray upgraded for the class V1 proof load, and item 14 (wake button, interface v0.3) added. Making the design constructable on 2026-10-01 (SWC-DDR-003) added USD 47: lines 15 (latch housing, release slider and springs), 16 (cell holder frames, moved out of line 12) and 17 (dock mounting parts), a longer back plate on line 8, front flanges on the tray (line 1) and more fixings (line 13). Every line now has geometry in the model except line 12 (wiring) and the label on line 14.

**Shared packs.** By Amish's 2026-09-25 portfolio rule, the SwapCell pack is priced here only. Dependent kits (PowerBox, SunSpoke, StepGen, WaterWalker, CargoMule and others) exclude it from their budgets and cite this BOM.

A second pack for a real swap demonstration would add about USD 449 (total about USD 1,068). Amish decided on 2026-09-25 (SWC-DDR-002) that this build budget is set before any build; it is on hold with TRL 4.

Cells must be new, matched and bought from an authorized distributor. Do not substitute recycled or unknown-grade cells in the reference pack.

Decisions of 2026-10-02 (SWC-DEC-001): the prototype lid (line 4) is cut from 3 mm UL 94 V-0 polycarbonate sheet rather than printed; line 4 now names the sheet, bought cut to size from a plastics distributor, at an estimated USD 25 (was USD 12 for printing filament), which adds USD 13; the large-format printer note is dropped. The state-of-charge light bar is an optional pack feature under line 14 and the dock status light sits under line 11; neither is in the prototype's quantities. No other quantity or price changed.
