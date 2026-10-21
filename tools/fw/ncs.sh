#!/usr/bin/env bash
# Run a command inside the nRF Connect SDK v2.9.3 toolchain (Git Bash), no nrfutil needed.
#   tools/fw/ncs.sh west build -b nrf54l15dk/nrf54l15/cpuapp boards/<b>/08-firmware/app -d <builddir>
#   tools/fw/ncs.sh west flash -d <builddir>
set -e
NCS=${NCS:-/c/ncs/v2.9.3}
TC=${NCS_TOOLCHAIN:-/c/ncs/toolchains/b620d30767}
export PATH="$TC/opt/bin:$TC/opt/bin/Scripts:$TC/opt/zephyr-sdk/arm-zephyr-eabi/bin:$TC/mingw64/bin:$TC/bin:$PATH"
export ZEPHYR_BASE="$NCS/zephyr"
export ZEPHYR_TOOLCHAIN_VARIANT=zephyr
export ZEPHYR_SDK_INSTALL_DIR="$TC/opt/zephyr-sdk"
export PYTHONPATH="$TC/opt/bin/Lib/site-packages"
# west must run from inside the workspace to find the manifest
export ZEPHYR_WEST_TOPDIR="$NCS"

cd "$NCS"
case "$1" in
  west) shift; exec west "$@" ;;
  *) exec "$@" ;;
esac
