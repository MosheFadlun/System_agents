"""Safe bench-PSU wrapper. Enforces hard limits and logs every state change.

    python tools/lab/psu.py status [--ch 1]
    python tools/lab/psu.py set --v 3.0 --i 0.05 [--ch 1] [--log boards/x/09-bringup/log.md]
    python tools/lab/psu.py on  [--ch 1] [--log ...]
    python tools/lab/psu.py off [--ch 1] [--log ...]
    python tools/lab/psu.py watch --seconds 10 --i-max 0.03 [--ch 1] [--log ...]   # trips OFF on overcurrent

Hard limits come from instruments.json ("max_voltage"/"max_current" on the psu entry).
Uses standard SCPI (APPLy / OUTPut / MEASure), which works on Siglent SPD, Rigol DP8xx and
Keysight E36xx. Check the command set for your model and adjust CMDS if needed.
"""
import argparse
import datetime as dt
import time

from scpi import Instrument

CMDS = {
    "set_v": "CH{ch}:VOLTage {v}",
    "set_i": "CH{ch}:CURRent {i}",
    "out": "OUTPut CH{ch},{state}",
    "meas_v": "MEASure:VOLTage? CH{ch}",
    "meas_i": "MEASure:CURRent? CH{ch}",
}
VENDOR_CMDS = {
    "rigol": {"set_v": ":SOUR{ch}:VOLT {v}", "set_i": ":SOUR{ch}:CURR {i}", "out": ":OUTP CH{ch},{state}",
              "meas_v": ":MEAS:VOLT? CH{ch}", "meas_i": ":MEAS:CURR? CH{ch}"},
    "keysight": {"set_v": "VOLT {v},(@{ch})", "set_i": "CURR {i},(@{ch})", "out": "OUTP {state},(@{ch})",
                 "meas_v": "MEAS:VOLT? (@{ch})", "meas_i": "MEAS:CURR? (@{ch})"},
}


def log(path, msg):
    line = f"- {dt.datetime.now().isoformat(timespec='seconds')} PSU: {msg}"
    print(line)
    if path:
        with open(path, "a", encoding="utf-8") as f:
            f.write(line + "\n")


def main():
    p = argparse.ArgumentParser()
    p.add_argument("action", choices=["status", "set", "on", "off", "watch"])
    p.add_argument("--name", default="psu")
    p.add_argument("--ch", type=int, default=1)
    p.add_argument("--v", type=float)
    p.add_argument("--i", type=float)
    p.add_argument("--seconds", type=float, default=10)
    p.add_argument("--i-max", type=float)
    p.add_argument("--log")
    a = p.parse_args()

    with Instrument(a.name) as psu:
        cmds = {**CMDS, **VENDOR_CMDS.get(psu.cfg.get("vendor", ""), {})}
        fmt = lambda k, **kw: cmds[k].format(ch=a.ch, **kw)
        meas = lambda: (psu.query_float(fmt("meas_v")), psu.query_float(fmt("meas_i")))

        if a.action == "status":
            v, i = meas()
            print(f"CH{a.ch}: {v:.4f} V  {i * 1000:.3f} mA")
        elif a.action == "set":
            if a.v is None or a.i is None:
                raise SystemExit("set needs --v and --i")
            if a.v > psu.cfg["max_voltage"] or a.i > psu.cfg["max_current"]:
                raise SystemExit(f"Refused: exceeds hard limit {psu.cfg['max_voltage']} V / {psu.cfg['max_current']} A")
            psu.write(fmt("set_i", i=a.i))
            psu.write(fmt("set_v", v=a.v))
            log(a.log, f"CH{a.ch} set {a.v} V, limit {a.i * 1000:.1f} mA")
        elif a.action == "on":
            psu.write(fmt("out", state="ON"))
            time.sleep(0.3)
            v, i = meas()
            log(a.log, f"CH{a.ch} ON -> {v:.3f} V {i * 1000:.2f} mA")
        elif a.action == "off":
            psu.write(fmt("out", state="OFF"))
            log(a.log, f"CH{a.ch} OFF")
        elif a.action == "watch":
            if a.i_max is None:
                raise SystemExit("watch needs --i-max")
            end = time.time() + a.seconds
            peak = 0.0
            while time.time() < end:
                v, i = meas()
                peak = max(peak, i)
                if i > a.i_max:
                    psu.write(fmt("out", state="OFF"))
                    log(a.log, f"CH{a.ch} TRIPPED OFF: {i * 1000:.2f} mA > {a.i_max * 1000:.2f} mA at {v:.3f} V")
                    raise SystemExit(2)
                time.sleep(0.2)
            log(a.log, f"CH{a.ch} watch {a.seconds}s OK, peak {peak * 1000:.2f} mA")


if __name__ == "__main__":
    main()
