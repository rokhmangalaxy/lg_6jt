#!/usr/bin/env sh
# Build APK Cut Grid Images tanpa GitHub Actions.
#
# Syarat: JDK 17 dan Android SDK (platform 35 + build-tools 35.0.0), Gradle 8.9.
# Pemakaian:
#   ./build-apk.sh                 # debug APK
#   ./build-apk.sh release         # release APK (tanpa signing config -> unsigned)
set -eu

MODE="${1:-debug}"
SCRIPT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
cd "$SCRIPT_DIR"

if [ -z "${JAVA_HOME:-}" ] && ! command -v java >/dev/null 2>&1; then
    echo "JDK 17 tidak ditemukan. Set JAVA_HOME ke instalasi JDK 17." >&2
    exit 1
fi

if [ -z "${ANDROID_HOME:-}" ] && [ -z "${ANDROID_SDK_ROOT:-}" ]; then
    for candidate in "$HOME/Android/Sdk" "$HOME/Library/Android/sdk" "$LOCALAPPDATA/Android/Sdk"; do
        if [ -d "$candidate" ]; then
            ANDROID_HOME="$candidate"
            export ANDROID_HOME
            break
        fi
    done
fi

if [ -z "${ANDROID_HOME:-}" ] && [ -z "${ANDROID_SDK_ROOT:-}" ]; then
    echo "Android SDK tidak ditemukan. Set ANDROID_HOME ke folder SDK (butuh platforms;android-35)." >&2
    exit 1
fi

if ! command -v gradle >/dev/null 2>&1; then
    echo "Gradle tidak ditemukan di PATH. Pasang Gradle 8.9 atau buka folder ini di Android Studio." >&2
    exit 1
fi

case "$MODE" in
    debug)
        gradle --no-daemon testDebugUnitTest assembleDebug
        echo "APK: $SCRIPT_DIR/app/build/outputs/apk/debug/app-debug.apk"
        ;;
    release)
        gradle --no-daemon assembleRelease
        echo "APK: $SCRIPT_DIR/app/build/outputs/apk/release/app-release-unsigned.apk"
        echo "Release belum ditandatangani; tanda tangani dengan apksigner sebelum dipasang."
        ;;
    *)
        echo "Mode tidak dikenal: $MODE (pakai 'debug' atau 'release')" >&2
        exit 2
        ;;
esac
