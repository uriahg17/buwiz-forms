#!/bin/bash
BIN=/Users/devin/moneybox-7d491c57/proof/ios-money-box-7d491c57/hunt/bin
LOG=/Users/devin/moneybox-7d491c57/proof/ios-money-box-7d491c57/logs
while pgrep -f 'lifecycle_a_fast.py ipad' >/dev/null; do sleep 5; done
python3 "$BIN/lifecycle_b_fast.py" ipad 10 > "$LOG/lifecycle-b-ipad-rerun.log" 2>&1
python3 "$BIN/lifecycle_c_fast.py" ipad > "$LOG/lifecycle-c-ipad-rerun.log" 2>&1
