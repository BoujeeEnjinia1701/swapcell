"""SwapCell sizing calculations for SWC-CAL-001 v0.2 (TRL 3).

Run from the repo root:  python docs/04-calcs/sizing.py
Prints every number quoted in docs/04-calcs/01-sizing.md and writes
docs/04-calcs/results.csv with the requirement status table.

First-principles estimates on paper. Every input is an assumption stated below;
none of it is measured.
"""
import csv
import math
from pathlib import Path

G = 9.81

# ---------------------------------------------------------------- assumptions
CELL = dict(
    ah_nom=5.0,        # Ah, nominal, high-power 5 Ah 21700 class
    ah_min=4.85,       # Ah, typical datasheet minimum for the same class (assumption)
    v_nom=3.6, v_max=4.2, v_min=3.0, v_fleet=4.1,
    mass_kg=0.069,
    r_dc=0.012,        # ohm, DC internal resistance at 25 C, mid state of charge
    i_cont=25.0,       # A, continuous rating
    cp=950.0,          # J/(kg K), specific heat of a cylindrical NMC cell
    price=5.50,        # USD, small-quantity price from an authorized distributor (estimate)
)
S, P = 13, 2
R_EXTRA = 0.032        # ohm: links, fuse wires, FETs, shunt, connector, main fuse
R_END_FACTOR = 1.25    # resistance rise late in discharge and from ageing (assumption)
FLEET_CAPACITY_FACTOR = 0.90   # capacity at a 4.1 V per cell charge limit (typical, assumption)

# Housing (massing model, SWC-DWG-002)
BODY = dict(L=340.0, W=90.0, D=80.0)   # mm
TRAY_T = 1.5                           # mm aluminium
RHO_AL = 2.70e-3                       # g/mm^3
LID_T, RHO_LID = 3.0, 1.20e-3          # mm, g/mm^3 (flame-retardant PC/ABS class)
CP_AL = 900.0
HANDLE_ABOVE, PLUG_BELOW = 35.0, 18.0  # mm

MASS_OTHER = {  # kg, estimates for parts not computed from geometry
    "Interconnects, holders and insulation": 0.18,
    "BMS board": 0.12,
    "Blind-mate plug": 0.06,
    "Handle and latch pawl": 0.10,
    "Seals, fasteners, wake button": 0.08,
}

# Thermal
T_AMB = 25.0
H_EXT = 9.0          # W/(m^2 K), still air, natural convection plus radiation
R_INT = 0.10         # K/W, cell core to tray, through holders and pads (assumption)
T_LIMIT = 60.0

# Charging
I_CHG = 5.0
CC_FRACTION = 0.85   # state of charge at the end of the constant-current phase
CV_HOURS = 0.6       # typical CV tail at 0.25C per cell to a C/20 cut-off (assumption)
CHARGER_EFF = 0.90

# Energy chain (Figure 2 of SWC-PRC-001)
ETA_CELL_CHARGE = 0.95
ETA_MOTOR = 0.80

# Connector and latch
POWER_CONTACT_N, SIGNAL_CONTACT_N, LATCH_DETENT_N = 12.0, 1.5, 8.0   # N, assumptions until contact parts are chosen
R5_MASS_LIMIT = 3.5          # kg, receivers design for this
VIB_G, SHOCK_G, LATCH_SF = 8.0, 25.0, 2.0
LEVER_FORCE_MAX = 50.0
PAWL = dict(width=36.0, tooth=4.0, root=4.0)   # mm, steel pawl
RIVETS, RIVET_D = 6, 4.0                       # blind rivets through the tray back face
AL_BEARING_ALLOW = 200.0                       # MPa, 5052-H32 bearing, conservative

# Sleep and wake (interface v0.3 item W)
I_SLEEP = 100e-6     # A, BMS asleep, INTERLOCK comparator armed
INTERLOCK_R = 10_000.0  # ohm coding resistor in every receiver
PULLUP_R = 100_000.0     # ohm, pack-side pull-up from a 3.3 V sleep rail
V_SLEEP_RAIL = 3.3

# CAN
BITRATE = 250_000
FRAME_BITS = 135     # 11-bit ID, 8 data bytes, worst-case bit stuffing
MSG_RATES = {"PACK_STATUS": 10, "PACK_LIMITS": 10, "CELL_SUMMARY": 1, "TEMPERATURES": 1,
             "FAULTS": 1, "STATE_OF_HEALTH": 0.1, "HOST_HEARTBEAT": 10, "CHARGER_STATUS": 1}
LOG_RECORDS, LOG_RECORD_BYTES = 2000, 32
LOG_BUS_SHARE = 0.5

# Use
SWAPS_PER_DAY, YEARS = 2, 5
CONNECTOR_CYCLES = 5000
HOST_CAP = 1000e-6   # F, typical 48 V controller input capacitance
PRECHARGE_R = 100.0  # ohm

# Pass-through example (PowerBox station host)
SOLAR_W, LOAD_W = 200.0, 20.0

BOM = Path(__file__).resolve().parents[2] / "bom" / "bom.csv"
BUDGET = 700.0


def main():
    out = {}
    def say(key, value, fmt="{:.2f}", unit=""):
        out[key] = value
        print(f"{key:44s} {fmt.format(value)} {unit}")

    # ---------------- electrical
    n = S * P
    v_nom, v_max, v_min = S * CELL["v_nom"], S * CELL["v_max"], S * CELL["v_min"]
    ah, ah_min = P * CELL["ah_nom"], P * CELL["ah_min"]
    r_pack = S * CELL["r_dc"] / P + R_EXTRA
    print("== Electrical")
    say("cells", n, "{:.0f}")
    say("V nominal", v_nom, unit="V"); say("V max", v_max, unit="V"); say("V min", v_min, unit="V")
    say("capacity nominal", ah, unit="Ah"); say("capacity at cell minimum", ah_min, unit="Ah")
    e_02c = ah * (v_nom - 0.2 * ah * r_pack)
    e_02c_min = ah_min * (v_nom - 0.2 * ah * r_pack)
    say("energy at 0.2C, nominal cells", e_02c, "{:.0f}", "Wh")
    say("energy at 0.2C, minimum cells", e_02c_min, "{:.0f}", "Wh")
    say("energy in fleet mode (4.1 V)", e_02c * FLEET_CAPACITY_FACTOR, "{:.0f}", "Wh")
    say("pack resistance", r_pack * 1000, "{:.0f}", "mOhm")
    for i in (20, 35):
        say(f"cell current at {i} A", i / P, "{:.1f}", "A")
        say(f"sag at {i} A", i * r_pack, "{:.1f}", "V")
    i_sc = v_max / r_pack
    say("short-circuit current, bolted", i_sc, "{:.0f}", "A")
    say("I2t in 500 us trip", i_sc ** 2 * 500e-6, "{:.0f}", "A2s")
    say("parallel neighbour fault current", CELL["v_nom"] / CELL["r_dc"], "{:.0f}", "A")
    tau = PRECHARGE_R * HOST_CAP
    say("pre-charge time constant", tau * 1000, "{:.0f}", "ms")
    say("pre-charge to 99 % (4.6 tau)", 4.6 * tau * 1000, "{:.0f}", "ms")
    say("pre-charge resistor energy", 0.5 * HOST_CAP * v_max ** 2, "{:.2f}", "J")

    # ---------------- mass
    print("== Mass")
    L, W, D = BODY["L"], BODY["W"], BODY["D"]
    tray_area = W * L + 2 * D * L + 2 * W * D          # open front, lid closes it
    m_tray = tray_area * TRAY_T * RHO_AL / 1000
    m_lid = W * L * LID_T * RHO_LID / 1000
    m_cells = n * CELL["mass_kg"]
    mass = m_cells + m_tray + m_lid + sum(MASS_OTHER.values())
    say("cells", m_cells, unit="kg"); say("tray (1.5 mm Al)", m_tray, unit="kg"); say("lid", m_lid, unit="kg")
    say("pack total", mass, unit="kg")
    say("pack total (lb)", mass / 0.4536, "{:.1f}", "lb")
    vol_l = L * W * D / 1e6
    say("body volume", vol_l, unit="L")
    say("gravimetric energy", ah * v_nom / mass, "{:.0f}", "Wh/kg")
    say("volumetric energy", ah * v_nom / vol_l, "{:.0f}", "Wh/L")
    say("overall length", L + HANDLE_ABOVE + PLUG_BELOW, "{:.0f}", "mm")

    # ---------------- thermal (lumped, with and without heat loss)
    print("== Thermal, 20 A full discharge")
    C = m_cells * CELL["cp"] + m_tray * CP_AL + 0.15 * 1300   # + BMS, lid share
    area = 2 * (L * W + L * D + W * D) / 1e6
    UA = H_EXT * area
    t = ah / 20.0 * 3600
    tau_th = C / UA
    say("heat capacity", C / 1000, "{:.2f}", "kJ/K")
    say("outer area", area, "{:.3f}", "m2"); say("UA", UA, "{:.2f}", "W/K")
    say("thermal time constant", tau_th / 60, "{:.0f}", "min")
    rows_th = []
    for label, rf in (("base", 1.0), ("end-of-discharge R", R_END_FACTOR)):
        q = 20.0 ** 2 * (S * CELL["r_dc"] / P * rf + R_EXTRA)
        q_cells = 20.0 ** 2 * S * CELL["r_dc"] / P * rf
        adiab = q * t / C
        rise = q / UA * (1 - math.exp(-t / tau_th))
        hot = T_AMB + rise + q_cells * R_INT
        say(f"heat, {label}", q, "{:.0f}", "W")
        say(f"adiabatic rise, {label}", adiab, "{:.0f}", "K")
        say(f"cell hot spot from 25 C with loss, {label}", hot, "{:.0f}", "C")
        say(f"cell hot spot enclosed (adiabatic), {label}", T_AMB + adiab + q_cells * R_INT, "{:.0f}", "C")
        say(f"cell hot spot from 45 C with loss, {label}", hot + 20, "{:.0f}", "C")
        rows_th.append(hot)
    # continuous current that holds 60 C from 45 C with loss (base R)
    lo, hi = 1.0, 20.0
    for _ in range(60):
        mid = (lo + hi) / 2
        q = mid ** 2 * r_pack; qc = mid ** 2 * S * CELL["r_dc"] / P
        tt = ah / mid * 3600
        hot = 45 + q / UA * (1 - math.exp(-tt / tau_th)) + qc * R_INT
        lo, hi = (mid, hi) if hot < T_LIMIT else (lo, mid)
    say("current that holds 60 C from 45 C ambient", lo, "{:.1f}", "A")
    i_hot45 = lo
    # continuous current that holds 60 C in an enclosed (adiabatic) mount from 25 C, full discharge
    lo, hi = 1.0, 20.0
    for _ in range(60):
        mid = (lo + hi) / 2
        q = mid ** 2 * r_pack; qc = mid ** 2 * S * CELL["r_dc"] / P
        hot = T_AMB + q * (ah / mid * 3600) / C + qc * R_INT
        lo, hi = (mid, hi) if hot < T_LIMIT else (lo, mid)
    say("current that holds 60 C enclosed from 25 C", lo, "{:.1f}", "A")
    i_enclosed = lo
    say("heat at 10 A (e-bike)", 10.0 ** 2 * r_pack, "{:.0f}", "W")

    # ---------------- charging
    print("== Charging")
    t_cc = CC_FRACTION * ah / I_CHG
    say("CC phase to 85 %", t_cc, unit="h")
    say("full charge", t_cc + CV_HOURS, unit="h")
    say("0 to 80 %", 0.8 * ah / I_CHG, unit="h")
    say("20 to 80 %", 0.6 * ah / I_CHG, unit="h")
    p_in = v_max * I_CHG / CHARGER_EFF
    say("dock input power in CC", p_in, "{:.0f}", "W")
    e_store = ah * v_nom
    e_chg_out = e_store / ETA_CELL_CHARGE
    e_grid = e_chg_out / CHARGER_EFF
    e_term = ah * (v_nom - 10.0 * r_pack)   # at a 10 A average discharge
    say("energy from grid per cycle", e_grid, "{:.0f}", "Wh")
    say("energy out of charger", e_chg_out, "{:.0f}", "Wh")
    say("energy stored", e_store, "{:.0f}", "Wh")
    say("energy at terminals (10 A mean)", e_term, "{:.0f}", "Wh")
    say("energy at wheel", e_term * ETA_MOTOR, "{:.0f}", "Wh")
    say("range e-bike low (12 Wh/km)", e_term / 12, "{:.0f}", "km")
    say("range e-bike high (8 Wh/km)", e_term / 8, "{:.0f}", "km")
    say("range trike low (25 Wh/km)", e_term / 25, "{:.0f}", "km")
    say("range trike high (15 Wh/km)", e_term / 15, "{:.0f}", "km")

    # ---------------- pass-through (v0.3 item C)
    print("== Charge while discharging (station host example)")
    i_net = (SOLAR_W - LOAD_W) / v_nom
    say("net charge current, 200 W in, 20 W out", i_net, "{:.1f}", "A")
    say("charge limit, standard (0.5C)", 0.5 * ah, "{:.1f}", "A")

    # ---------------- sleep and wake (v0.3 item W)
    print("== Sleep and wake")
    month = 30 * 24
    say("sleep drain per month", I_SLEEP * month / ah * 100, "{:.2f}", "% of capacity")
    say("sleep to empty from 50 %", 0.5 * ah / I_SLEEP / 24 / 365, "{:.1f}", "years")
    v_node = V_SLEEP_RAIL * INTERLOCK_R / (INTERLOCK_R + PULLUP_R)
    say("INTERLOCK node, receiver present", v_node, "{:.2f}", "V")
    say("INTERLOCK node, bridged short", 0.0, "{:.2f}", "V")
    say("INTERLOCK node, open", V_SLEEP_RAIL, "{:.2f}", "V")
    say("INTERLOCK sense current", V_SLEEP_RAIL / (INTERLOCK_R + PULLUP_R) * 1e6, "{:.0f}", "uA")

    # ---------------- latch (v0.3 item V)
    print("== Latch, vehicle class V1")
    f_vib = R5_MASS_LIMIT * VIB_G * G
    f_shock = R5_MASS_LIMIT * SHOCK_G * G
    f_proof = f_shock * LATCH_SF
    preload = 1.2 * f_vib
    say("inertial force at 8 g", f_vib, "{:.0f}", "N")
    say("inertial force at 25 g", f_shock, "{:.0f}", "N")
    say("latch proof load (SF 2)", f_proof, "{:.0f}", "N")
    say("receiver preload (1.2 x 8 g)", preload, "{:.0f}", "N")
    say("lever ratio for 50 N hand force", preload / LEVER_FORCE_MAX, "{:.1f}", "")
    tau_pawl = f_proof / (PAWL["width"] * PAWL["tooth"])
    sigma_pawl = f_proof * PAWL["tooth"] / 2 / (PAWL["width"] * PAWL["root"] ** 2 / 6)
    bearing = f_proof / (RIVETS * RIVET_D * TRAY_T)
    say("pawl tooth shear stress", tau_pawl, "{:.0f}", "MPa")
    say("pawl tooth bending stress", sigma_pawl, "{:.0f}", "MPa")
    say("tray bearing stress at rivets", bearing, "{:.0f}", "MPa")
    say("tray bearing margin", AL_BEARING_ALLOW / bearing, "{:.1f}", "x")

    # ---------------- connector
    print("== Connector")
    f_ins = 2 * POWER_CONTACT_N + 6 * SIGNAL_CONTACT_N + LATCH_DETENT_N
    say("insertion force estimate", f_ins, "{:.0f}", "N")
    cycles = SWAPS_PER_DAY * 365 * YEARS
    say("mating cycles in 5 years", cycles, "{:.0f}", "")
    say("connector cycle margin", CONNECTOR_CYCLES / cycles, "{:.2f}", "x")

    # ---------------- CAN
    print("== CAN")
    fps = sum(MSG_RATES.values())
    load = fps * FRAME_BITS / BITRATE
    say("frames per second, one pack", fps, "{:.1f}", "")
    say("bus load, one pack", load * 100, "{:.1f}", "%")
    say("bus load, two packs", (fps * 2 - MSG_RATES["HOST_HEARTBEAT"]) * FRAME_BITS / BITRATE * 100, "{:.1f}", "%")
    log_bytes = LOG_RECORDS * LOG_RECORD_BYTES
    frames = math.ceil(log_bytes / 7)
    say("log size", log_bytes / 1024, "{:.1f}", "KiB")
    say("log transfer time", frames * FRAME_BITS / (BITRATE * LOG_BUS_SHARE), "{:.0f}", "s")

    # ---------------- BOM
    print("== BOM")
    rows = list(csv.DictReader(BOM.open()))
    total = sum(float(r["qty"]) * float(r["unit_cost_usd"]) for r in rows)
    def group(nums):
        return sum(float(r["qty"]) * float(r["unit_cost_usd"]) for r in rows if int(r["item"].split()[0]) in nums)
    pack = group({1, 2, 3, 4, 5, 6, 7, 12, 13, 14})
    dock = group({8, 9, 10, 11})
    say("pack parts", pack, "{:.0f}", "USD"); say("dock parts", dock, "{:.0f}", "USD")
    say("BOM total", total, "{:.0f}", "USD"); say("budget margin", BUDGET - total, "{:.0f}", "USD")
    say("cell cost", n * CELL["price"], "{:.0f}", "USD")
    say("cell cost per Wh", n * CELL["price"] / (ah * v_nom), "{:.2f}", "USD/Wh")

    # ---------------- requirement status
    st = lambda ok: "Met" if ok else "Not met"
    req = [
        ("R1", f"{v_nom:.1f} V nominal, {v_min:.1f} to {v_max:.1f} V", "46.8 V; 39.0 to 54.6 V", st(True)),
        ("R2", f"{ah:.1f} Ah and {e_02c:.0f} Wh nominal; {ah_min:.1f} Ah and {e_02c_min:.0f} Wh at cell minimum",
         "10 Ah and 450 Wh at 0.2C", "At risk"),
        ("R3", f"{rows_th[0]:.0f} C base, {rows_th[1]:.0f} C with end-of-discharge R in open air; derates to "
               f"{i_enclosed:.1f} A enclosed and {i_hot45:.1f} A from 45 C; 17.5 A per cell at 35 A",
         "Below 60 C from 25 C at 20 A in an open-air mount; derate elsewhere; 35 A for 10 s",
         st(max(rows_th) < T_LIMIT) + " (on paper)"),
        ("R4", f"{t_cc + CV_HOURS:.1f} h full; {0.8 * ah / I_CHG:.1f} h to 80 %", "3 h full; 2 h to 80 %",
         st(t_cc + CV_HOURS <= 3 and 0.8 * ah / I_CHG <= 2)),
        ("R5", f"{mass:.2f} kg", "3.5 kg or less", st(mass <= 3.5)),
        ("R6", f"340 x 90 x 80 mm; {L + HANDLE_ABOVE + PLUG_BELOW:.0f} mm overall", "400 mm or less overall",
         st(L + HANDLE_ABOVE + PLUG_BELOW <= 400)),
        ("R7", f"insertion about {f_ins:.0f} N (assumed contact forces)", "10 s, one hand, 50 N or less",
         "Not verifiable at TRL 3"),
        ("R8", "Gasketed lid, potted pack-side contacts (design review only)", "Pack IP65, dock IP54",
         "Not verifiable at TRL 3"),
        ("R9", "300 to 500 cycles typical; 4.1 V fleet mode adopted", "500 cycles to 80 %; SoH within 5 %", "At risk"),
        ("R10", f"{cycles:.0f} cycles in 5 years, margin {CONNECTOR_CYCLES / cycles:.2f}x; custom keyed shroud, contacts not yet chosen",
         "5,000 cycles, +/-3 mm, +/-2 deg, 40 A", "Not verifiable at TRL 3"),
        ("R11", f"Short circuit {i_sc:.0f} A; pre-charge {4.6 * tau * 1000:.0f} ms; functions specified",
         "Protections listed in R11", "Not verifiable at TRL 3"),
        ("R12", f"Bus load {load * 100:.1f} %; log {log_bytes / 1024:.1f} KiB, {frames * FRAME_BITS / (BITRATE * LOG_BUS_SHARE):.0f} s",
         "CAN 250 kbit/s, 2,000 records, CSV export", "Met (on paper)"),
        ("R13", f"Sleep drain {I_SLEEP * month / ah * 100:.2f} %/month; coded INTERLOCK {v_node:.2f} V window",
         "Wake with no host supply; 1 %/month or less",
         st(I_SLEEP * month / ah * 100 <= 1.0) + " (on paper)"),
        ("R14", f"Net {i_net:.1f} A charge in the PowerBox case, within {0.5 * ah:.1f} A", "Charge-discharge mode within limits",
         st(i_net <= 0.5 * ah) + " (on paper)"),
        ("R15", f"Proof {f_proof:.0f} N; bearing margin {AL_BEARING_ALLOW / bearing:.1f}x; lever ratio {preload / LEVER_FORCE_MAX:.1f}",
         "Class V1 vibration and shock, no release", "Not verifiable at TRL 3"),
        ("R16", f"Pack and dock parts {total:.0f} USD", "700 USD for one pack and one dock", st(total <= BUDGET)),
    ]
    res = Path(__file__).with_name("results.csv")
    with res.open("w", newline="") as f:
        w = csv.writer(f); w.writerow(["id", "value", "target", "status"]); w.writerows(req)
    print("== Requirement status (also in results.csv)")
    for r in req:
        print(f"{r[0]:4s} {r[3]:24s} {r[1]}")
    return out


if __name__ == "__main__":
    main()
