"""Minimal SCPI-over-LAN client (raw socket, no dependencies).

Usage:
    python tools/lab/scpi.py <instrument> "<command>"   # query if it ends with '?'
    python tools/lab/scpi.py <instrument> --idn
    python tools/lab/scpi.py --list

Instruments are defined in tools/lab/instruments.json:
    {"psu": {"host": "192.168.1.50", "port": 5025, "vendor": "siglent", "kind": "psu"}, ...}
Typical raw-socket ports: Keysight/Siglent/R&S 5025, Rigol 5555.
"""
import json
import socket
import sys
from pathlib import Path

CONFIG = Path(__file__).with_name("instruments.json")


def load_instruments():
    return json.loads(CONFIG.read_text())


class Instrument:
    def __init__(self, name, timeout=5.0):
        cfg = load_instruments()
        if name not in cfg:
            raise SystemExit(f"Unknown instrument '{name}'. Known: {', '.join(cfg)}")
        self.name = name
        self.cfg = cfg[name]
        self.sock = socket.create_connection((self.cfg["host"], self.cfg.get("port", 5025)), timeout=timeout)

    def close(self):
        self.sock.close()

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        self.close()

    def write(self, cmd):
        self.sock.sendall((cmd.strip() + "\n").encode())

    def _read_until_newline(self):
        buf = b""
        while not buf.endswith(b"\n"):
            chunk = self.sock.recv(65536)
            if not chunk:
                break
            buf += chunk
        return buf

    def query(self, cmd):
        self.write(cmd)
        return self._read_until_newline().decode(errors="replace").strip()

    def query_float(self, cmd):
        return float(self.query(cmd))

    def query_block(self, cmd):
        """Query that returns an IEEE 488.2 definite-length block (#<n><len><data>)."""
        self.write(cmd)
        head = b""
        while len(head) < 2:
            head += self.sock.recv(2 - len(head))
        if head[:1] != b"#":
            # Not a block: return the raw line.
            return head + self._read_until_newline()
        ndig = int(head[1:2])
        lenstr = b""
        while len(lenstr) < ndig:
            lenstr += self.sock.recv(ndig - len(lenstr))
        length = int(lenstr)
        data = b""
        while len(data) < length:
            chunk = self.sock.recv(min(1 << 20, length - len(data)))
            if not chunk:
                break
            data += chunk
        try:  # drain the trailing newline if there is one
            self.sock.settimeout(0.2)
            self.sock.recv(16)
        except OSError:
            pass
        finally:
            self.sock.settimeout(5.0)
        return data


def main(argv):
    if not argv or argv[0] in ("-h", "--help"):
        print(__doc__)
        return
    if argv[0] == "--list":
        for name, cfg in load_instruments().items():
            print(f"{name:10s} {cfg.get('kind', ''):6s} {cfg.get('vendor', ''):10s} {cfg['host']}:{cfg.get('port', 5025)}")
        return
    name = argv[0]
    cmd = "*IDN?" if len(argv) < 2 or argv[1] == "--idn" else argv[1]
    with Instrument(name) as inst:
        if cmd.rstrip().endswith("?"):
            print(inst.query(cmd))
        else:
            inst.write(cmd)
            print("OK")


if __name__ == "__main__":
    main(sys.argv[1:])
