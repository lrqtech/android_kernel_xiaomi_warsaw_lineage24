# Xiaomi warsaw kernel

Android common kernel for LineageOS 24 on Xiaomi warsaw.

| Setting | Value |
| --- | --- |
| Upstream commit | `c4127a25dcf3c8923daffa62632816f6acf0e135` |
| Linux version | 6.6.118 |
| GKI | Android 15, generation 8 |
| Page size | 4 KiB |
| Toolchain | r510928 |
| Userspace | Android 17 |

## Warsaw configuration

`warsaw/no_kunit_defconfig` disables KUnit. The Kleaf target builds 78
production GKI modules, leaving out the 18 KUnit modules and 34 KUnit
interfaces. KUnit source files remain in the upstream tree.

The production KMI list and protected exports preserve the ABI used by the
OEM modules. Two conditional structure layouts retain their original fields
when KUnit is disabled. The header changes are already applied and are
recorded in [preserve-production-kmi-layout.patch](warsaw/preserve-production-kmi-layout.patch).

The 538 OEM driver modules are supplied as OTA binaries by the
[vendor repository](https://github.com/lrqtech/android_vendor_xiaomi_warsaw_lineage24).
Their sources are not part of this kernel tree.

## Build

Use a separate Linux Kleaf workspace with Git, Repo and access to this
repository. The manifest selects the toolchain and build dependencies and
links `common/warsaw` into the workspace root.

```sh
git clone --branch lineage-24.0 https://github.com/lrqtech/android_kernel_xiaomi_warsaw_lineage24.git "$HOME/warsaw-kernel-source"
mkdir -p "$HOME/android/kernel-warsaw"
cd "$HOME/android/kernel-warsaw"
repo init --standalone-manifest -u "file://$HOME/warsaw-kernel-source/warsaw/workspace.xml"
repo sync -c -j4
tools/bazel run --jobs=32 --config=stamp --lto=default //warsaw:kernel_aarch64_dist -- --destdir="$PWD/dist"
```

Keep strict KMI checking enabled. The full Kleaf build has not yet been rerun
from this repository checkout.

## Use with LineageOS

The [device tree](https://github.com/lrqtech/android_device_xiaomi_warsaw_lineage24)
uses `vendor/xiaomi/warsaw/boot/gki-no-kunit` from the vendor repository.
To replace that kernel, install the new Image and all 78 signed GKI modules
together, then regenerate the module indexes. Keep the OEM modules, firmware
and load order intact. Mixing kernel and module builds can prevent boot.

The supplied Image has SHA-256:

```text
b6ef8d3fc7122e02a66f21337c6adde61e3350ebeaf6862713aaeba234d3a512
```

Rebuilds can differ because of Git metadata, timestamps and generated signing
keys. The original private signing key is not included, so identical binary
hashes are not guaranteed.

## Source and license

Upstream: [Google Android common kernel](https://android.googlesource.com/kernel/common).

[upstream-source.json](warsaw/upstream-source.json) records the source commit,
archive hash and local header patch hash.
[manifest_15863337.xml](warsaw/manifest_15863337.xml) is the original Google
workspace manifest; [workspace.xml](warsaw/workspace.xml) selects the
dependencies used here.

See `COPYING`, `LICENSES` and the notices in individual files for license
terms.
