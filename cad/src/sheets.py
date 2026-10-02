"""SwapCell general arrangement drawing SWC-DWG-002 (Rev P3).

Run from the repo root:  python cad/src/sheets.py
Builds cad/drawings/SWC-DWG-002.svg, .pdf and .png from the parametric model.
"""
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / ".kit"))
sys.path.insert(0, str(Path(__file__).resolve().parent))
from drawing import Sheet, project_views  # noqa: E402
from model import PARAMS as P, assemblies  # noqa: E402

pack, dock, asm = assemblies()
work = ROOT / "cad/drawings/_views"
views = project_views(asm, work)

s = Sheet(project="SwapCell", title="General arrangement, pack in wall dock", dwg_no="SWC-DWG-002",
          rev="P3", author="Amish Chadha", date="2026-10-01", concept=True,
          material="Pack: 1.5 mm 5052 Al tray, FR polymer lid; dock: 12 mm Al plate, printed shelf and guides. See bom/bom.csv",
          revisions=[("P1", "Preliminary GA, interface v0.3 (SWC-CAL-001)", "2026-09-25", "AC"),
                     ("P2", "Notes: connector family, R3 derating (SWC-DDR-002)", "2026-09-25", "AC"),
                     ("P3", "Constructable design: latch, fixings, dock (SWC-DDR-003)", "2026-10-01", "AC")])
s.add_ortho(views, ["front", "top", "right"])
s.add_svg(views["iso"], 276, 40, 140, 62, label="Isometric view", sublabel="Not to scale")
s.add_notes("Interface v0.3 key dimensions (mm)", [
    f"Pack body {P['pack_l']:.0f} x {P['pack_w']:.0f} x {P['pack_d']:.0f}, tolerance +0 / -1.5",
    f"Overall length {P['pack_l'] + P['handle_h'] + P['plug_h']:.0f} (handle {P['handle_h']:.0f}, plug {P['plug_h']:.0f})",
    "Datum A: connector face; insertion along Z, connector first",
    f"Plug centred in width, {P['plug_offset_y']:.0f} toward back face from depth centre",
    f"Guide faces 340 x 80, {P['pack_w']:.0f} apart; receiver clearance {P['guide_clear']:.0f} per side",
    f"Latch pawl {P['latch_w']:.0f} wide, {P['latch_from_top']:.0f} below top end, back face,",
    f"  {P['latch_proud']:.0f} proud, hooks 4 under the catch; thumb release {P['latch_travel']:.0f}",
    f"Handle zone {P['handle_w']:.0f} x {P['handle_d']:.0f}, up to {P['handle_h']:.0f} above top end",
    "Latch class V1: proof 1.72 kN along insertion axis",
    "Vehicle receiver preload 330 N via over-centre lever",
    "Contacts: P1 PACK+, P2 PACK-, S1 SGND, S2/S3 CAN,",
    "  S4 WAKE, S5 AUX, S6 INTERLOCK (10 kOhm coded)",
    "Connector: custom keyed shroud, commercial contacts",
    "R3: 20 A open-air mount; derate 50 to 60 C cell temp",
    "Flush wake button on lid face (interface v0.3)",
    "Pack mass about 3.0 kg; 13S2P, 46.8 V, 468 Wh",
    "PRELIMINARY, NOT FOR FABRICATION",
], x=276, y=114, width=140)
s.save(ROOT / "cad/drawings/SWC-DWG-002")
shutil.rmtree(work, ignore_errors=True)
print("wrote cad/drawings/SWC-DWG-002.svg, .pdf, .png")
