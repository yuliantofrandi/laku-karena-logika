#!/bin/bash
# Tangkap area halaman (viewport) jendela Google Chrome pengguna jadi PNG — screenshot ASLI dari layar.
# Khusus macOS (memakai `screencapture`). Aplikasi Claude/terminal butuh izin
# System Settings → Privacy & Security → Screen Recording.
#
# Pakai:
#   tangkap_layar.sh <out.png> <x> <y> <lebar> <tinggi>
# Nilai x/y/lebar/tinggi diambil dari tab aplikasi lewat javascript_tool:
#   ({x: screenX, y: screenY + (outerHeight - innerHeight), w: innerWidth, h: innerHeight})
# Syarat: zoom browser 100%, jendela Chrome tidak tertutup jendela lain, tidak ada popup/devtools.
set -euo pipefail
[ $# -eq 5 ] || { echo "pakai: $0 <out.png> <x> <y> <lebar> <tinggi>" >&2; exit 1; }
out="$1"; x="$2"; y="$3"; w="$4"; h="$5"
command -v screencapture >/dev/null || { echo "screencapture tidak ada — skrip ini khusus macOS" >&2; exit 1; }
mkdir -p "$(dirname "$out")"
osascript -e 'tell application "Google Chrome" to activate' >/dev/null 2>&1 || true
sleep 0.6
screencapture -x -R"${x},${y},${w},${h}" "$out"
echo "OK $out"
