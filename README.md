# Xiaomi Warsaw GKI source for LineageOS 24

Full Google Android common kernel source at
`c4127a25dcf3c8923daffa62632816f6acf0e135`, with Warsaw's no-KUnit GKI
integration. The source baseline is Linux 6.6.118 / Android 15 GKI generation 8,
used with the Android 17 Warsaw userspace. This is a fresh snapshot with no
imported Git history, not a claim of official LineageOS acceptance.

## Changes from upstream

- `warsaw/no_kunit_defconfig` disables KUnit.
- The dedicated Kleaf target selects 78 production GKI modules, excluding
  the 18 KUnit framework/test modules and 34 KUnit interfaces.
- The production KMI list and protected exports preserve the retained OEM
  module ABI. Two conditional structure layouts keep their original fields
  even with KUnit disabled. The exact header change is recorded in
  `warsaw/preserve-production-kmi-layout.patch` and is already applied.
- `warsaw/workspace.xml` pins the common source snapshot and its complete
  toolchain/build dependency workspace. The original Google manifest is
  retained as `warsaw/manifest_15863337.xml` for provenance.

KUnit source files remain in the upstream source tree; they are disabled in
the selected build, not deleted from Linux. The 538 OEM vendor drivers are
not implemented in this GKI repository; their unchanged OTA modules are in
the companion vendor repository.

## Build

Use a separate Linux Kleaf workspace with Git, Repo and access to this private
repository. The pinned manifest links `common/warsaw` to the workspace root.

```sh
git clone --branch lineage-24.0 https://github.com/lrqtech/android_kernel_xiaomi_warsaw_lineage24.git "$HOME/warsaw-kernel-source"
mkdir -p "$HOME/android/kernel-warsaw"
cd "$HOME/android/kernel-warsaw"
repo init --standalone-manifest -u "file://$HOME/warsaw-kernel-source/warsaw/workspace.xml"
repo sync -c -j4
tools/bazel run --jobs=32 --config=stamp --lto=default //warsaw:kernel_aarch64_dist -- --destdir="$PWD/dist"
```

The target uses the pinned r510928 toolchain and 4 KiB pages. Preserve strict
KMI checking. This source publication has not rerun the full kernel build;
it restores the original pinned source and recorded integration inputs.

## Android integration

The [device repository](https://github.com/lrqtech/android_device_xiaomi_warsaw_lineage24)
consumes the paired input under
`vendor/xiaomi/warsaw/boot/gki-no-kunit`, supplied by the
[vendor repository](https://github.com/lrqtech/android_vendor_xiaomi_warsaw_lineage24).
Build GKI separately, then integrate its Image, all 78 signed production
modules and regenerated dependency indexes as one unit. Preserve the OEM
modules, firmware and load ordering. A partial replacement can prevent boot.

The archived paired Image has SHA-256
`b6ef8d3fc7122e02a66f21337c6adde61e3350ebeaf6862713aaeba234d3a512`.
New root Git metadata, timestamps and generated module-signing keys may
change rebuilt binary hashes. Source/KMI correspondence is not a promise
of byte-identical output. Private signing keys are intentionally absent.

## Provenance and license

Upstream: https://android.googlesource.com/kernel/common

`warsaw/upstream-source.json` records the upstream commit, archive digest and
local header patch digest. Linux COPYING, LICENSES, SPDX identifiers and
file-level notices are retained. Consult them for the applicable license.
