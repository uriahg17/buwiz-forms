#!/bin/bash
BIN=/Users/devin/moneybox-7d491c57/proof/ios-money-box-7d491c57/hunt/bin
LOG=/Users/devin/moneybox-7d491c57/proof/ios-money-box-7d491c57/logs
python3 "$BIN/lifecycle_a_fast.py" iphone > "$LOG/lifecycle-a-iphone.log" 2>&1
python3 "$BIN/lifecycle_b_fast.py" iphone 10 > "$LOG/lifecycle-b-iphone.log" 2>&1
python3 "$BIN/lifecycle_c_fast.py" iphone > "$LOG/lifecycle-c-iphone.log" 2>&1
python3 "$BIN/lifecycle_a_fast.py" ipad > "$LOG/lifecycle-a-ipad.log" 2>&1
python3 "$BIN/lifecycle_b_fast.py" ipad 10 > "$LOG/lifecycle-b-ipad.log" 2>&1
python3 "$BIN/lifecycle_c_fast.py" ipad > "$LOG/lifecycle-c-ipad.log" 2>&1
