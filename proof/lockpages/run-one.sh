#!/usr/bin/env bash
# Run the lockpages recipe once against a freshly launched debug app. Input is only gpui-agent recipe steps;
# the platform recorder only observes the run.
set -euo pipefail
TARGET="$1"   # macos or ios
DEVICE="$2"   # macos, or a Simulator UDID
THEME="$3"    # light or dark
OUT="$4"
ROOT=/Users/devin/lockpages-job/buwiz-forms
CLI=/Users/devin/lockpages-job/proof-driver/gpui-agent
RECIPE="${RECIPE:-$ROOT/agent-recipes/lockpages/lockpages.wants}"
mkdir -p "$OUT/shots"
db="/Users/devin/lockpages-job/scratch/lockpages-$TARGET-$THEME.db"
mkdir -p "$(dirname "$db")"
rm -f "$db" "$db-shm" "$db-wal"
export PATH="/Users/devin/.rustup/toolchains/1.99.0-aarch64-apple-darwin/bin:/Users/devin/BuwizNsh/tools/bin:$PATH"
export CARGO_TARGET_DIR=/Users/devin/lockpages-job/build-target CARGO_INCREMENTAL=0
export BUWIZ_NO_KEYCHAIN=1 EBIR_TEST_ENV=1 BIR_AUTH_BYPASS=1 BIR_SFTP_DRY_RUN=1
export BIR_LOG_DIR=/Users/devin/lockpages-job/logs
unset BIR_SFTP_LIVE BIR_SFTP_HOST BIR_SFTP_PORT BIR_SFTP_USERNAME BIR_SFTP_PASSWORD BIR_SFTP_ACCEPT_ANY_HOST_KEY BIR_RELAY_URL BUWIZ_RELAY_SEND
if [ -z "${GPUI_AGENT_TOKEN:-}" ]; then
  token_file=/Users/devin/lockpages-job/scratch/gpui-agent-token
  mkdir -p "$(dirname "$token_file")"
  if [ ! -f "$token_file" ]; then (umask 077; openssl rand -hex 16 >"$token_file"); fi
  GPUI_AGENT_TOKEN="$(cat "$token_file")"
fi
export GPUI_AGENT_TOKEN GPUI_AGENT_ADDR=127.0.0.1:17421
route="view=lockdebug;theme=$THEME;wrong=1"
entry="$ROOT/nsh/lockpages-proof-entry.tsx"
cat >"$entry" <<EOF2
// Proof harness only: mounts the real Shell with the debug start route because NSH's process.env capability
// does not expose BIR_SHELL_START to the shipping App entry. Not part of the pull request.
import { mount, View } from "nsh";
import "./theme/fonts";
import { Shell } from "./shell/Shell";

function ProofEntry() {
  return (
    <View class="flex-1">
      <Shell start="$route" polling={false} watchQueued={false} firstRun agent />
    </View>
  );
}

mount(ProofEntry);
EOF2
if [ "$TARGET" = ios ]; then
  pkill -f 'agent/ios-handoff.sh token' >/dev/null 2>&1 || true
  pkill -f 'nsh run --target ios' >/dev/null 2>&1 || true
  xcrun simctl boot "$DEVICE" >/dev/null 2>&1 || true
  xcrun simctl terminate "$DEVICE" com.longbridge.nsh.host >/dev/null 2>&1 || true
  token_container="$(xcrun simctl get_app_container "$DEVICE" com.longbridge.nsh.host data 2>/dev/null || true)"
  [ -z "$token_container" ] || rm -f "$token_container/Library/Caches/gpui-agent-token"
  args=(--device "$DEVICE")
else
  args=()
fi
(
  cd "$ROOT"
  if [ "$TARGET" = ios ]; then
    just nsh-run-agent "$TARGET" "" "${args[@]}" lockpages-proof-entry.tsx
  else
    just nsh-run-agent "$TARGET" "$db" "${args[@]}" lockpages-proof-entry.tsx
  fi
) >"$OUT/app.log" 2>&1 &
launcher=$!
recpid=''
cleanup() {
  [ "${KEEP:-}" = 1 ] && return 0
  [ -z "$recpid" ] || kill -INT "$recpid" 2>/dev/null || true
  kill -INT "$launcher" 2>/dev/null || kill "$launcher" 2>/dev/null || true
  for pid in $(lsof -tiTCP:17421 -sTCP:LISTEN 2>/dev/null || true); do kill -INT "$pid" 2>/dev/null || kill "$pid" 2>/dev/null || true; done
  if [ "$TARGET" = ios ]; then
    xcrun simctl terminate "$DEVICE" com.longbridge.nsh.host >/dev/null 2>&1 || true
    pkill -f 'agent/ios-handoff.sh token' >/dev/null 2>&1 || true
    pkill -f 'nsh run --target ios' >/dev/null 2>&1 || true
  fi
  rm -f "$db" "$db-shm" "$db-wal"
  rm -f "$entry"
}
trap cleanup EXIT
for _ in $(seq 1 900); do
  if nc -z 127.0.0.1 17421 >/dev/null 2>&1; then break; fi
  if ! kill -0 "$launcher" >/dev/null 2>&1; then echo "launcher exited; see $OUT/app.log" >&2; exit 1; fi
  sleep 2
done
nc -z 127.0.0.1 17421 >/dev/null 2>&1 || { echo "agent port did not open" >&2; exit 1; }
"$CLI" hello --addr 127.0.0.1:17421 >"$OUT/hello.json"
shotdir="$OUT/shots"
if [ "$TARGET" = ios ]; then
  container="$(xcrun simctl get_app_container "$DEVICE" dev.goldcoders.bir data 2>/dev/null || true)"
  if [ -n "$container" ]; then
    shotdir="$container/Library/Caches/gpui-agent"
    mkdir -p "$shotdir"
    rm -f "$shotdir"/*.png 2>/dev/null || true
  fi
  xcrun simctl io "$DEVICE" recordVideo "$OUT/recording.mov" >"$OUT/recorder.log" 2>&1 &
  recpid=$!
else
  mkdir -p "$OUT/frames"
  rm -f "$OUT/frames"/*.png
  (
    n=0
    while :; do
      n=$((n + 1))
      frame="$(printf '%s/frames/frame-%04d.png' "$OUT" "$n")"
      "$CLI" screenshot --inline --addr 127.0.0.1:17421 --out "$frame" >/dev/null 2>&1 || rm -f "$frame"
      sleep 0.25
    done
  ) >"$OUT/frames.log" 2>&1 &
  recpid=$!
fi
sleep 1
set +e
"$CLI" recipe run "$RECIPE" --addr 127.0.0.1:17421 --receipt-out "$OUT/receipt.json" --screenshot-dir "$shotdir" --screenshot-flagged >"$OUT/receipt.stdout.json" 2>"$OUT/recipe.stderr"
code=$?
set -e
if [ "$TARGET" = ios ]; then
  kill -INT "$recpid" 2>/dev/null || true
  wait "$recpid" 2>/dev/null || true
  if [ "$shotdir" != "$OUT/shots" ]; then
    cp "$shotdir"/*.png "$OUT/shots"/ 2>/dev/null || true
  fi
else
  kill -9 "$recpid" 2>/dev/null || true
  wait "$recpid" 2>/dev/null || true
  count="$(find "$OUT/frames" -name 'frame-*.png' | wc -l | tr -d ' ')"
  echo "frames: $count" >"$OUT/recorder.log"
  if [ "$count" -ge 8 ]; then
    ffmpeg -y -loglevel error -framerate 1 -i "$OUT/frames/frame-%04d.png" -vf 'scale=trunc(iw/2)*2:trunc(ih/2)*2' -pix_fmt yuv420p "$OUT/recording.mp4" >>"$OUT/recorder.log" 2>&1 || true
  fi
fi
recpid=''
exit "$code"
