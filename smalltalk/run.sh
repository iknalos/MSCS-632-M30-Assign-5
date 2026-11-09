#!/usr/bin/env bash
# Runs the Smalltalk version: gst RideSharing.st main.st
# Uses the gst on PATH if there is one; otherwise GNU Smalltalk 3.2.5 unpacked
# without root under $GST_HOME (default ~/tools/gst/usr; see README).
set -euo pipefail
cd "$(dirname "$0")"
if command -v gst >/dev/null 2>&1; then
    exec gst RideSharing.st main.st
fi
G=${GST_HOME:-$HOME/tools/gst/usr}
LD_LIBRARY_PATH="$G/lib${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}" exec "$G/bin/gst" \
    --kernel-directory "$G/share/gnu-smalltalk/kernel" \
    -I "$G/lib/gnu-smalltalk/gst.im" \
    RideSharing.st main.st
