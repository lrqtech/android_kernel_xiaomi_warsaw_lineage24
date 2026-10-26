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

The `warsaw-20261027` tag pairs this source with the matching device and vendor
trees. It includes the protected-export input repair used for the October 25 GKI
rebuild. Image, all 78 signed GKI modules and the public certificate are supplied
together by the vendor repository. Earlier source tags remain available.

## Build

Use a separate Linux Kleaf workspace with Git, Repo and access to this
repository. The manifest selects the toolchain and build dependencies and
links `common/warsaw` into the workspace root.

```sh
git clone --branch warsaw-20261027 https://github.com/lrqtech/android_kernel_xiaomi_warsaw_lineage24.git "$HOME/warsaw-kernel-source"
mkdir -p "$HOME/android/kernel-warsaw"
cd "$HOME/android/kernel-warsaw"
repo init --standalone-manifest -u "file://$HOME/warsaw-kernel-source/warsaw/workspace.xml"
repo sync -c -j4
tools/bazel run --jobs=32 --config=stamp --lto=default //warsaw:kernel_aarch64_dist -- --destdir="$PWD/dist"
```

Keep strict KMI checking enabled. A complete stamped Kleaf build from the pinned
workspace passed on 25 October 2026 with the protected-export input fix applied.
The Image contains all 475 selected protected exports; all 78 module signatures
and the OEM import CRC comparisons passed. Hardware boot remains untested.

## Use with LineageOS

The [device tree](https://github.com/lrqtech/android_device_xiaomi_warsaw_lineage24)
uses `vendor/xiaomi/warsaw/boot/gki-no-kunit` from the vendor repository.
To replace that kernel, install the new Image and all 78 signed GKI modules
together, then regenerate the module indexes. Keep the OEM modules, firmware
and load order intact. Mixing kernel and module builds can prevent boot.

The supplied Image has SHA-256:

```text
df170a396bae78b5d77aa5c03ff205d91d6216f67b714382024a5fb465ccdf8a
```

Rebuilds can differ because of Git metadata, timestamps and generated signing
keys. The original private signing key is not included, so identical binary
hashes are not guaranteed.

The clean full Android build from `warsaw-20261027` completed on October 27.
Its final boot image contains the Image above, and all 78 GKI modules in the
system_dlkm image match the paired vendor input. This Android build reused the
complete October 25 GKI output; it did not rebuild the kernel. See the device
[build results](https://github.com/lrqtech/android_device_xiaomi_warsaw_lineage24/blob/lineage-24.0/docs/BUILD_RESULT_20261027.txt).
Physical-device boot and module behavior remain untested.

## Check the paired vendor inputs

After retrieving the vendor repository's LFS objects, run:

```sh
python3 warsaw/check-vendor.py /path/to/vendor/xiaomi/warsaw
```

This checks the recorded GKI hashes, the 78-module set, 4 KiB configuration,
disabled KUnit, and the expected Image and certificate. It does not rebuild
the kernel or establish that OEM modules will work on a phone. Keep strict KMI
checking enabled when rebuilding. Never publish the generated private module
signing key.

Normal boot and recovery SELinux modes are selected by the device tree; the
current source defaults to enforcing in both boot modes. Upstream userdebug
domain exceptions are documented by the device tree. See the
[device status](https://github.com/lrqtech/android_device_xiaomi_warsaw_lineage24/blob/lineage-24.0/docs/STATUS.md)
for runtime validation still needed.

The Vega/SenseTime userspace libraries and their dependent features are retired
in the matching device/vendor source set. Those SDKs are not part of this kernel.
See the vendor README for the retained Qti FD path and disabled camera features.

## Source and license

Upstream: [Google Android common kernel](https://android.googlesource.com/kernel/common).

[upstream-source.json](warsaw/upstream-source.json) records the source commit,
archive hash and local header patch hash.
[manifest_15863337.xml](warsaw/manifest_15863337.xml) is the original Google
workspace manifest; [workspace.xml](warsaw/workspace.xml) selects the
dependencies used here.

See `COPYING`, `LICENSES` and the notices in individual files for license
terms.
