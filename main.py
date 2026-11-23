#!/usr/bin/env python3
"""Copy the bundled broadsheet to the output path the kit expects.

The entry is a pre-rendered PNG: draw.py builds it deterministically from
the story data in this repository (same input, same bytes, every run). This
program only places the finished image where the harness looks for it.
No network, no clock reads, no randomness — two runs write identical bytes.
"""
import os
import shutil
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SOURCE = HERE / "entry.png"
DEFAULT_OUTPUT = Path("/output/entry.png")


def main(argv):
    # Local runs may pass an output path (argv) or set MAKEFUN_OUTPUT; the
    # harness itself runs with no arguments, so /output/entry.png is default.
    target = Path(argv[1]) if len(argv) > 1 else Path(
        os.environ.get("MAKEFUN_OUTPUT", str(DEFAULT_OUTPUT)))
    if not SOURCE.exists():
        raise SystemExit(f"bundled image missing: {SOURCE}")
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(SOURCE, target)
    print(f"wrote {target} ({target.stat().st_size} bytes)")


if __name__ == "__main__":
    main(sys.argv)
