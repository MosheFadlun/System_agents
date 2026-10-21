# One-time setup

Already on this machine: KiCad 10, nRF Connect SDK v2.9.3 (`C:/ncs`), SEGGER J-Link, nrfutil, Java, Python 3.14.

Still needed:

1. **SKiDL** (schematic as code):
   ```
   python -m pip install skidl      # done 2026-10-18 (SKiDL 3.0)
   setx KICAD10_SYMBOL_DIR "C:\Program Files\KiCad\10.0\share\kicad\symbols"
   setx KICAD10_FOOTPRINT_DIR "C:\Program Files\KiCad\10.0\share\kicad\footprints"
   ```
   (Optional: the board scripts set these themselves. SKiDL 3 uses `KICAD10_*` with `set_default_tool(KICAD10)`.)
2. **Freerouting** (autorouter): download the latest release jar from
   https://github.com/freerouting/freerouting/releases to `tools/bin/freerouting.jar`.
   Headless run: `java -jar tools/bin/freerouting.jar -de board.dsn -do board.ses -mp 20`
3. **nRF54 support:** check that NCS v2.9.3 has the exact nRF54 part you pick
   (`C:/ncs/v2.9.3/zephyr/boards/nordic/`). Install a newer NCS
   (nRF Connect for Desktop → Toolchain Manager) if needed. If `modules/` is missing under `C:/ncs/v2.9.3`, run `tools/fw/ncs.sh west update`.
4. **Lab instruments:** set the real IP, port and vendor of each instrument in `tools/lab/instruments.json`,
   then test with `python tools/lab/scpi.py --list` and `python tools/lab/scpi.py psu --idn`.
   Set `max_voltage` / `max_current` on the PSU to the hard ceiling for your boards.
