#!/bin/sh

set -e
set -v

datagen > file

# Compress with various levels and ensure that their sizes are ordered
zstd --fast=10 file -o file-f10.zst -q
zstd --fast=1 file -o file-f1.zst -q
zstd -1 file -o file-1.zst -q
zstd -19 file -o file-19.zst -q

zstd -t file-f10.zst file-f1.zst file-1.zst file-19.zst

cmp_size -lt file-19.zst file-1.zst
cmp_size -lt file-1.zst file-f1.zst
cmp_size -lt file-f1.zst file-f10.zst

# Test default levels
zstd --fast file -f -q
cmp file.zst file-f1.zst || die "--fast is not level -1"

zstd -0 file -o file-0.zst -q
zstd -f file -q
cmp file.zst file-0.zst || die "Level 0 is not the default level"

# Test level clamping
zstd -99 file -o file-99.zst -q
cmp file-19.zst file-99.zst || die "Level 99 is clamped to 19"
zstd --fast=200000 file -c | zstd -t

zstd -5000000000 -f file       && die "Level too large, must fail" ||:
zstd --fast=5000000000 -f file && die "Level too large, must fail" ||:

# Test setting a level through the environment variable
ZSTD_CLEVEL=-10 zstd file -o file-f10-env.zst -q
ZSTD_CLEVEL=1 zstd file -o file-1-env.zst -q
ZSTD_CLEVEL=+19 zstd file -o file-19-env.zst -q
ZSTD_CLEVEL=+99 zstd file -o file-99-env.zst -q

cmp file-f10.zst file-f10-env.zst || die "Environment variable failed to set level"
cmp file-1.zst file-1-env.zst || die "Environment variable failed to set level"
cmp file-19.zst file-19-env.zst || die "Environment variable failed to set level"
cmp file-99.zst file-99-env.zst || die "Environment variable failed to set level"

# Test invalid environment clevel is the default level
zstd -f file -q
ZSTD_CLEVEL=- zstd -f file -o file-env.zst -q      ; cmp file.zst file-env.zst
ZSTD_CLEVEL=+ zstd -f file -o file-env.zst -q      ; cmp file.zst file-env.zst
ZSTD_CLEVEL=a zstd -f file -o file-env.zst -q      ; cmp file.zst file-env.zst
ZSTD_CLEVEL=-a zstd -f file -o file-env.zst -q     ; cmp file.zst file-env.zst
ZSTD_CLEVEL=+a zstd -f file -o file-env.zst -q     ; cmp file.zst file-env.zst
ZSTD_CLEVEL=3a7 zstd -f file -o file-env.zst -q    ; cmp file.zst file-env.zst
ZSTD_CLEVEL=5000000000 zstd -f file -o file-env.zst -q ; cmp file.zst file-env.zst

# Test environment clevel is overridden by command line
ZSTD_CLEVEL=10 zstd -f file -1 -o file-1-env.zst -q
ZSTD_CLEVEL=10 zstd -f file --fast=1 -o file-f1-env.zst -q

cmp file-1.zst file-1-env.zst  || die "Environment variable not overridden"
cmp file-f1.zst file-f1-env.zst || die "Environment variable not overridden"
