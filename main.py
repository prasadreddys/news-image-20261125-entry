#!/usr/bin/env python3
"""news-image-20261125 entry: copy the bundled front page to the output.

The picture lives in this repository as entry.png. This program checks
that it is a complete, well-formed PNG inside the contest limits, then
writes its exact bytes to /output/entry.png (or $MAKEFUN_OUTPUT_DIR).
It reads nothing else, uses no network, no clock and no randomness, so
two runs produce identical output.
"""
import os
import struct
import sys
import zlib
from pathlib import Path

HERE = Path(__file__).resolve().parent
SOURCE = HERE / "entry.png"
MAX_BYTES = 1_048_576
MAX_SIDE = 1024
PNG_MAGIC = b"\x89PNG\r\n\x1a\n"


def fail(message):
    print(f"error: {message}", file=sys.stderr)
    raise SystemExit(1)


def check_png(data):
    if len(data) > MAX_BYTES:
        fail(f"entry.png is {len(data)} bytes, over the 1048576 byte limit")
    if data[:8] != PNG_MAGIC:
        fail("entry.png does not start with the PNG signature")
    pos = 8
    width = height = None
    seen_end = False
    while pos < len(data):
        if pos + 8 > len(data):
            fail("truncated PNG chunk header")
        size, kind = struct.unpack(">I4s", data[pos:pos + 8])
        end = pos + 12 + size
        if end > len(data):
            fail(f"truncated PNG chunk {kind!r}")
        body = data[pos + 8:pos + 8 + size]
        want = zlib.crc32(kind)
        want = zlib.crc32(body, want) & 0xFFFFFFFF
        (have,) = struct.unpack(">I", data[pos + 8 + size:end])
        if have != want:
            fail(f"PNG chunk {kind!r} has a bad checksum")
        if kind == b"IHDR":
            if size != 13:
                fail("IHDR chunk is not 13 bytes")
            width, height = struct.unpack(">II", body[:8])
            if width > MAX_SIDE or height > MAX_SIDE:
                fail(f"image is {width}x{height}, over the 1024x1024 limit")
        if kind == b"IEND":
            seen_end = True
            if end != len(data):
                fail("bytes follow the PNG IEND chunk")
            break
        pos = end
    if width is None:
        fail("no IHDR chunk found")
    if not seen_end:
        fail("no IEND chunk found")
    return width, height


def main():
    if not SOURCE.is_file():
        fail(f"bundled image not found: {SOURCE}")
    data = SOURCE.read_bytes()
    width, height = check_png(data)
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    out_dir.mkdir(parents=True, exist_ok=True)
    target = out_dir / "entry.png"
    target.write_bytes(data)
    print(f"wrote {target} ({width}x{height}, {len(data)} bytes)")


if __name__ == "__main__":
    main()
