#!/bin/bash
BIN=/Users/devin/moneybox-7d491c57/proof/ios-money-box-7d491c57/hunt/bin
LOG=/Users/devin/moneybox-7d491c57/proof/ios-money-box-7d491c57/logs
python3 "$BIN/lifecycle_a_fast.py" iphone > "$LOG/lifecycle-a-iphone-rerun.log" 2>&1
python3 "$BIN/lifecycle_a_fast.py" ipad > "$LOG/lifecycle-a-ipad-rerun.log" 2>&1
