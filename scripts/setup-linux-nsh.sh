#!/usr/bin/env bash
#
# setup-linux-nsh.sh — NSH app toolchain on Linux: the NSH CLI, the Android SDK
# and emulator, and a wrapper that runs NSH commands with the host display.
# Run after scripts/setup-linux.sh (it needs rustup).
#
# NSH needs GTK >= 4.14 and WebKitGTK 6.0, which Ubuntu 22.04 does not ship, so
# everything that builds NSH runs in an Ubuntu 24.04 Docker image
# (buwiz-nsh-2404) with $HOME mounted. Needs Docker usable without sudo.
#
# What it sets up (idempotent; finished pieces are skipped):
#   - ../nsh checked out at NSH_PINNED_REF (.github/workflows/nsh.yml)
#   - the buwiz-nsh-2404 image (GTK 4, WebKitGTK 6.0, JDK 17, Noto fonts)
#   - the nsh CLI in ~/BuwizNsh/tools/bin, built in the image at the pin
#   - Android: JDK 17, SDK command-line tools, platform-tools, emulator,
#     android-35, build-tools 35.0.1, NDK 27, the API 35 x86_64 image, an AVD
#     named "buwiz", the Rust Android targets and NSH's Android runtime
#   - ~/BuwizNsh/nsh2404.sh <cmd>: runs <cmd> in the image from nsh/ with
#     $DISPLAY (default :0), host networking (`just mock-account` on 127.0.0.1:3008) and
#     the local-test safety variables (baked into Android dev builds)
#
# Usage:
#   scripts/setup-linux-nsh.sh               # everything
#   scripts/setup-linux-nsh.sh --no-android  # desktop NSH only
#   scripts/setup-linux-nsh.sh --check       # verify only, install nothing
#
# Then:
#   just mock-account &
#   ~/BuwizNsh/nsh2404.sh nsh run --target linux
#   emulator -avd buwiz & ~/BuwizNsh/nsh2404.sh nsh run --target android
#
set -euo pipefail

CHECK_ONLY=0
WITH_ANDROID=1
for arg in "$@"; do
    case "$arg" in
        --check)      CHECK_ONLY=1 ;;
        --no-android) WITH_ANDROID=0 ;;
        -h|--help)
            sed -n '2,31p' "$0"
            exit 0
            ;;
        *) echo "Unknown option: $arg (see --help)" >&2; exit 2 ;;
    esac
done

log()  { printf '\033[1;34m==>\033[0m %s\n' "$*"; }
warn() { printf '\033[1;33mwarning:\033[0m %s\n' "$*" >&2; }
die()  { printf '\033[1;31merror:\033[0m %s\n' "$*" >&2; exit 1; }

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO="$(cd "$SCRIPT_DIR/.." && pwd)"
NSH="$(cd "$REPO/.." && pwd)/nsh"
WORK="$HOME/BuwizNsh"
IMAGE="buwiz-nsh-2404"
ANDROID_HOME="${ANDROID_HOME:-$HOME/Android/Sdk}"
CMDLINE_TOOLS_URL="https://dl.google.com/android/repository/commandlinetools-linux-11076708_latest.zip"
NDK_VERSION="27.2.12479018"
SYSTEM_IMAGE="system-images;android-35;google_apis;x86_64"
AVD="buwiz"
JAVA_HOME_IMAGE="/usr/lib/jvm/java-17-openjdk-amd64"

REF="$(sed -n 's/^ *NSH_PINNED_REF: *//p' "$REPO/.github/workflows/nsh.yml" | head -1)"
[ -n "$REF" ] || die "NSH_PINNED_REF not found in .github/workflows/nsh.yml"

SUDO=""
[ "$(id -u)" -ne 0 ] && SUDO="sudo"

# $HOME plus the checkouts when they live outside it, mounted at the same
# paths so builds and the wrapper see the host layout.
outside_home() { case "$1/" in "$HOME"/*) return 1 ;; esac; }
MOUNTS=(-v "$HOME:$HOME")
for dir in "$REPO" "$NSH"; do
    outside_home "$dir" && MOUNTS+=(-v "$dir:$dir")
done
# The SDK is mounted only for Android work, once the host install has created
# it: a missing bind source would be created by Docker, owned by root.
sdk_mount() {
    if [ -d "$ANDROID_HOME" ] && outside_home "$ANDROID_HOME"; then
        printf '%s\n' -v "$ANDROID_HOME:$ANDROID_HOME"
    fi
}

# One-off command in the image as the calling user.
in_image() {  # in_image <workdir> <docker -e args...> -- <cmd...>
    local workdir="$1"; shift
    local envs=()
    while [ "$1" != "--" ]; do envs+=("$1"); shift; done
    shift
    docker run --rm -u "$(id -u):$(id -g)" \
        -e HOME="$HOME" -e PATH="$HOME/.cargo/bin:/usr/local/bin:/usr/bin:/bin" \
        -e CARGO_INCREMENTAL=0 "${envs[@]}" \
        "${MOUNTS[@]}" -w "$workdir" "$IMAGE" "$@"
}

nsh_cli_current() {
    [ -x "$WORK/tools/bin/nsh" ] &&
        in_image "$NSH" -- "$WORK/tools/bin/nsh" --version 2>/dev/null | grep -q "(${REF:0:7})"
}

checkout_nsh() {
    [ -d "$NSH/.git" ] || git clone https://github.com/hexuria/nsh "$NSH"
    if [ "$(git -C "$NSH" rev-parse HEAD)" != "$REF" ]; then
        log "Checking out NSH at ${REF:0:7}"
        git -C "$NSH" fetch origin "$REF"
        git -C "$NSH" checkout --detach "$REF"
    fi
}

build_image() {
    log "Building the $IMAGE image (cached after the first run)"
    mkdir -p "$WORK"
    cat > "$WORK/Dockerfile" <<'DOCKER_EOF'
FROM ubuntu:24.04
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential pkg-config perl python3 ca-certificates curl git \
    clang libclang-dev libgtk-4-dev libwebkitgtk-6.0-dev \
    libgstreamer1.0-dev libgstreamer-plugins-base1.0-dev \
    gstreamer1.0-plugins-base gstreamer1.0-plugins-good \
    libdbus-1-dev libssl-dev \
    xvfb xauth at-spi2-core libxtst6 \
    fonts-noto-core fonts-noto-color-emoji \
    && rm -rf /var/lib/apt/lists/*
# Android builds (javac + d8) for `nsh run --target android`.
RUN apt-get update && apt-get install -y --no-install-recommends openjdk-17-jdk-headless \
    && rm -rf /var/lib/apt/lists/*
DOCKER_EOF
    docker build -q -t "$IMAGE" -f "$WORK/Dockerfile" "$WORK" >/dev/null
}

write_wrapper() {
    cat > "$WORK/nsh2404.sh" <<'NSH_EOF'
#!/usr/bin/env bash
# Runs a command in the buwiz-nsh-2404 image from nsh/, with the host display.
# Written by scripts/setup-linux-nsh.sh.
set -euo pipefail
cd "@REPO@/nsh"
display="${DISPLAY:-:0}"
DISPLAY="$display" xhost +SI:localuser:"$(id -un)" >/dev/null 2>&1 || true
tty=(); [ -t 0 ] && [ -t 1 ] && tty=(-t)
# NSH's CLI sets CC/AR for Android but not RANLIB, which vendored OpenSSL needs.
RANLIB="@ANDROID_HOME@/ndk/@NDK@/toolchains/llvm/prebuilt/linux-x86_64/bin/llvm-ranlib"
# Unset, the NSH app's own workspace builds full debuginfo: a 4 GB dev APK.
# The Android app reads test settings baked in at build time, not from the
# environment it runs in (nsh/src/dev_env.rs).
android=(); case " $* " in *android*) android=(-e CARGO_PROFILE_DEV_DEBUG=0
  -e "BUWIZ_ANDROID_DEV_ENV=EBIR_TEST_ENV=1;BIR_AUTH_BYPASS=1;BUWIZ_NO_KEYCHAIN=1;BIR_SFTP_DRY_RUN=1");; esac
uid="$(id -u)"
NSH_EOF
    local mounts=("${MOUNTS[@]}") sdk
    # Kept on --no-android runs too, so they don't break an existing Android setup.
    mapfile -t sdk < <(sdk_mount); mounts+=("${sdk[@]}")
    printf 'mounts=(%s)\n' "$(printf '%q ' "${mounts[@]}")" >> "$WORK/nsh2404.sh"
    cat >> "$WORK/nsh2404.sh" <<'NSH_EOF'
exec docker run --rm -i "${tty[@]}" "${android[@]}" --network host --security-opt apparmor=unconfined -u "$uid:$(id -g)" \
  -e HOME="$HOME" \
  -e PATH="$HOME/BuwizNsh/tools/bin:$HOME/.cargo/bin:@ANDROID_HOME@/platform-tools:/usr/local/bin:/usr/bin:/bin" \
  -e CARGO_TARGET_DIR="$HOME/BuwizNsh/target-nsh" \
  -e CARGO_INCREMENTAL=0 \
  -e ANDROID_HOME="@ANDROID_HOME@" \
  -e JAVA_HOME=@JAVA_HOME@ \
  -e RANLIB_x86_64_linux_android="$RANLIB" -e RANLIB_aarch64_linux_android="$RANLIB" -e RANLIB_armv7_linux_androideabi="$RANLIB" \
  -e DISPLAY="$display" -e XDG_RUNTIME_DIR="/run/user/$uid" \
  -e DBUS_SESSION_BUS_ADDRESS="unix:path=/run/user/$uid/bus" \
  -e BUWIZ_NO_KEYCHAIN=1 -e EBIR_TEST_ENV=1 -e BIR_AUTH_BYPASS=1 -e BIR_SFTP_DRY_RUN=1 \
  "${mounts[@]}" \
  -v /tmp/.X11-unix:/tmp/.X11-unix \
  -v "/run/user/$uid:/run/user/$uid" \
  -w "@REPO@/nsh" \
  buwiz-nsh-2404 "$@"
NSH_EOF
    sed -i -e "s#@REPO@#$REPO#g" -e "s#@ANDROID_HOME@#$ANDROID_HOME#g" \
        -e "s#@NDK@#$NDK_VERSION#g" -e "s#@JAVA_HOME@#$JAVA_HOME_IMAGE#g" "$WORK/nsh2404.sh"
    chmod +x "$WORK/nsh2404.sh"
}

install_nsh_cli() {
    if nsh_cli_current; then
        log "nsh CLI already at ${REF:0:7}"
        return 0
    fi
    log "Building the nsh CLI at ${REF:0:7} in the image"
    in_image "$NSH" -e CARGO_TARGET_DIR="$WORK/target-nsh" -- \
        cargo install --locked --path crates/nsh-cli --root "$WORK/tools"
    rm -f "$WORK/tools/android/.ref"   # a new CLI needs a matching runtime
}

install_android_sdk() {
    if ! command -v java >/dev/null 2>&1 || ! command -v unzip >/dev/null 2>&1; then
        command -v apt-get >/dev/null 2>&1 || die "install a JDK 17 and unzip, then re-run"
        log "Installing JDK 17 and unzip"
        $SUDO apt-get install -y openjdk-17-jdk-headless unzip
    fi
    local sdkmanager="$ANDROID_HOME/cmdline-tools/latest/bin/sdkmanager"
    if [ ! -x "$sdkmanager" ]; then
        log "Installing Android command-line tools in $ANDROID_HOME"
        local tmp; tmp="$(mktemp -d)"
        curl -fsSL -o "$tmp/cmdline-tools.zip" "$CMDLINE_TOOLS_URL"
        unzip -q "$tmp/cmdline-tools.zip" -d "$tmp"
        mkdir -p "$ANDROID_HOME/cmdline-tools"
        rm -rf "$ANDROID_HOME/cmdline-tools/latest"
        mv "$tmp/cmdline-tools" "$ANDROID_HOME/cmdline-tools/latest"
        rm -rf "$tmp"
    fi
    log "Installing Android SDK packages (NDK $NDK_VERSION, API 35)"
    yes | "$sdkmanager" --licenses >/dev/null 2>&1 || true
    "$sdkmanager" "platform-tools" "emulator" "platforms;android-35" "build-tools;35.0.1" \
        "ndk;$NDK_VERSION" "$SYSTEM_IMAGE" >/dev/null
    if ! "$ANDROID_HOME/emulator/emulator" -list-avds 2>/dev/null | grep -qx "$AVD"; then
        log "Creating the $AVD AVD (Pixel 7, API 35)"
        echo no | "$ANDROID_HOME/cmdline-tools/latest/bin/avdmanager" create avd \
            -n "$AVD" -k "$SYSTEM_IMAGE" -d pixel_7 --force >/dev/null
    fi
    rustup target add aarch64-linux-android armv7-linux-androideabi x86_64-linux-android
}

# NSH's Android runtime (classes.dex + libnsh.so per ABI). xtask reads its own
# target/ dir, so no CARGO_TARGET_DIR; the CLI looks for it next to its bin/.
install_android_runtime() {
    local dest="$WORK/tools/android/bin-dev"
    if [ -d "$dest" ] && [ "$(cat "$WORK/tools/android/.ref" 2>/dev/null)" = "$REF" ]; then
        log "NSH Android runtime already at ${REF:0:7}"
        return 0
    fi
    log "Building NSH's Android runtime in the image"
    local sdk; mapfile -t sdk < <(sdk_mount)
    in_image "$NSH" "${sdk[@]}" -e ANDROID_HOME="$ANDROID_HOME" -e JAVA_HOME="$JAVA_HOME_IMAGE" -- \
        cargo xtask android --dev
    rm -rf "$dest" && mkdir -p "$WORK/tools/android"
    cp -r "$NSH/target/android/debug-dev" "$dest"
    echo "$REF" > "$WORK/tools/android/.ref"
}

check() {
    local ok=1
    report() { printf '  %-22s %s\n' "$1" "$2"; [ "$3" -eq 1 ] || ok=0; }
    if docker info >/dev/null 2>&1; then report docker "$(docker --version)" 1
    else report docker "MISSING or not usable without sudo" 0; fi
    if docker image inspect "$IMAGE" >/dev/null 2>&1; then report "image:$IMAGE" present 1
    else report "image:$IMAGE" MISSING 0; fi
    if [ -d "$NSH/.git" ] && [ "$(git -C "$NSH" rev-parse HEAD)" = "$REF" ]; then report "../nsh" "${REF:0:7}" 1
    else report "../nsh" "MISSING or not at ${REF:0:7}" 0; fi
    if nsh_cli_current; then report "nsh CLI" "${REF:0:7}" 1
    else report "nsh CLI" "MISSING or not at ${REF:0:7}" 0; fi
    # The wrapper embeds the checkout and SDK paths; a move makes it stale.
    if [ -x "$WORK/nsh2404.sh" ] && grep -qxF "cd \"$REPO/nsh\"" "$WORK/nsh2404.sh" &&
        grep -qF -- "-e ANDROID_HOME=\"$ANDROID_HOME\"" "$WORK/nsh2404.sh"; then
        report "nsh2404.sh wrapper" present 1
    else report "nsh2404.sh wrapper" "MISSING or stale" 0; fi
    if [ "$WITH_ANDROID" -eq 1 ]; then
        if [ -d "$ANDROID_HOME/ndk/$NDK_VERSION" ]; then report "android ndk" "$NDK_VERSION" 1
        else report "android ndk" MISSING 0; fi
        if "$ANDROID_HOME/emulator/emulator" -list-avds 2>/dev/null | grep -qx "$AVD"; then report "avd:$AVD" present 1
        else report "avd:$AVD" MISSING 0; fi
        if [ -d "$WORK/tools/android/bin-dev" ]; then report "nsh android runtime" present 1
        else report "nsh android runtime" MISSING 0; fi
    fi
    [ "$ok" -eq 1 ] && log "NSH toolchain ready" || warn "Missing pieces — run scripts/setup-linux-nsh.sh"
    return $((1 - ok))
}

main() {
    if [ "$CHECK_ONLY" -eq 1 ]; then
        check
        exit $?
    fi
    command -v docker >/dev/null 2>&1 || die "Docker is required (NSH builds in an Ubuntu 24.04 image)"
    docker info >/dev/null 2>&1 || die "Docker is not usable as $(id -un); add the user to the docker group"
    # setup-linux.sh may have just installed rustup in another process.
    if ! command -v cargo >/dev/null 2>&1 && [ -f "$HOME/.cargo/env" ]; then
        # shellcheck disable=SC1091
        . "$HOME/.cargo/env"
    fi
    command -v cargo >/dev/null 2>&1 || die "run scripts/setup-linux.sh first (needs rustup)"

    checkout_nsh
    build_image
    install_nsh_cli
    if [ "$WITH_ANDROID" -eq 1 ]; then
        install_android_sdk
        install_android_runtime
    fi
    write_wrapper

    log "Verifying"
    check
    if [ "$WITH_ANDROID" -eq 1 ]; then
        printf '\nAdd to your shell profile:\n  export ANDROID_HOME=%s\n  export ANDROID_SDK_ROOT=%s\n' \
            "$ANDROID_HOME" "$ANDROID_HOME"
    fi
}

main
