#!/usr/bin/env bash
# Usage: check_orion.sh <stage_name> [n_lines]
set -euo pipefail
ssh -o BatchMode=yes orion "tail -${2:-20} /tmp/$1.log 2>/dev/null; echo '--- running:'; pgrep -fc $1 || echo none"
