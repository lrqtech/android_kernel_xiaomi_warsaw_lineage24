#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-2.0-only
"""Check the vendor GKI inputs paired with this kernel source set."""

import argparse
import hashlib
import json
from pathlib import Path
import sys


def digest(path):
    with path.open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('vendor', type=Path, help='vendor/xiaomi/warsaw checkout with LFS objects')
    args = parser.parse_args()
    root = (args.vendor / 'boot/gki-no-kunit').resolve(strict=True)
    expected = json.loads(Path(__file__).with_name('vendor-inputs.json').read_text())
    manifest = json.loads((root / 'manifest.json').read_text())
    if manifest['common_commit'] != expected['common_commit']:
        raise ValueError('GKI source revision differs')
    if manifest['kernel_page_size'] != 4096 or manifest['kunit_enabled'] is not False:
        raise ValueError('Expected a 4 KiB GKI with KUnit disabled')
    hashes = manifest['hashes']
    for name, value in hashes.items():
        relative = Path(name)
        if relative.is_absolute() or '..' in relative.parts:
            raise ValueError('Unsafe GKI manifest path: ' + name)
        path = root / relative
        if not path.resolve().is_relative_to(root) or digest(path) != value:
            raise ValueError('GKI hash mismatch: ' + name)
    for name, value in expected['sha256'].items():
        if hashes.get(name) != value or digest(root / name) != value:
            raise ValueError('Source-set input mismatch: ' + name)
    if manifest['image_sha256'] != expected['sha256']['Image']:
        raise ValueError('Image metadata differs from the source set')
    modules = {str(path.relative_to(root)) for path in
               (root / 'system_dlkm/flatten/lib/modules').glob('*.ko')}
    recorded = {name for name in hashes
                if name.startswith('system_dlkm/flatten/lib/modules/') and name.endswith('.ko')}
    if modules != recorded or len(modules) != expected['gki_modules']:
        raise ValueError('GKI module inventory differs')
    if manifest['gki_modules'] != len(modules):
        raise ValueError('GKI module count differs from metadata')
    config = set((root / 'kernel.config').read_text().splitlines())
    if 'CONFIG_ARM64_4K_PAGES=y' not in config or '# CONFIG_KUNIT is not set' not in config:
        raise ValueError('Kernel config does not match the required page size and KUnit setting')
    print(f'PASS: {len(hashes)} GKI hashes, {len(modules)} modules, 4 KiB pages, KUnit disabled')


if __name__ == '__main__':
    try:
        main()
    except (OSError, ValueError, KeyError) as error:
        sys.exit(str(error))
